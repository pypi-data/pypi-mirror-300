import functools
from itertools import chain
import logging
import os
from os import environ
from os import getpid
from threading import RLock
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import TypeVar
from typing import Union

from ddtrace import _hooks
from ddtrace import config
from ddtrace._trace.context import Context
from ddtrace._trace.processor import SpanAggregator
from ddtrace._trace.processor import SpanProcessor
from ddtrace._trace.processor import TopLevelSpanProcessor
from ddtrace._trace.processor import TraceProcessor
from ddtrace._trace.processor import TraceSamplingProcessor
from ddtrace._trace.processor import TraceTagsProcessor
from ddtrace._trace.provider import DefaultContextProvider
from ddtrace._trace.span import Span
from ddtrace.appsec._constants import APPSEC
from ddtrace.constants import ENV_KEY
from ddtrace.constants import HOSTNAME_KEY
from ddtrace.constants import PID
from ddtrace.constants import VERSION_KEY
from ddtrace.filters import TraceFilter
from ddtrace.internal import agent
from ddtrace.internal import atexit
from ddtrace.internal import compat
from ddtrace.internal import debug
from ddtrace.internal import forksafe
from ddtrace.internal import hostname
from ddtrace.internal.atexit import register_on_exit_signal
from ddtrace.internal.constants import SAMPLING_DECISION_TRACE_TAG_KEY
from ddtrace.internal.constants import SPAN_API_DATADOG
from ddtrace.internal.dogstatsd import get_dogstatsd_client
from ddtrace.internal.logger import get_logger
from ddtrace.internal.peer_service.processor import PeerServiceProcessor
from ddtrace.internal.processor.endpoint_call_counter import EndpointCallCounterProcessor
from ddtrace.internal.runtime import get_runtime_id
from ddtrace.internal.sampling import SpanSamplingRule
from ddtrace.internal.sampling import get_span_sampling_rules
from ddtrace.internal.schema.processor import BaseServiceProcessor
from ddtrace.internal.serverless import has_aws_lambda_agent_extension
from ddtrace.internal.serverless import in_aws_lambda
from ddtrace.internal.serverless import in_azure_function
from ddtrace.internal.serverless import in_gcp_function
from ddtrace.internal.serverless.mini_agent import maybe_start_serverless_mini_agent
from ddtrace.internal.service import ServiceStatusError
from ddtrace.internal.utils import _get_metas_to_propagate
from ddtrace.internal.utils.deprecations import DDTraceDeprecationWarning
from ddtrace.internal.utils.formats import format_trace_id
from ddtrace.internal.utils.http import verify_url
from ddtrace.internal.writer import AgentResponse
from ddtrace.internal.writer import AgentWriter
from ddtrace.internal.writer import LogWriter
from ddtrace.internal.writer import TraceWriter
from ddtrace.sampler import BasePrioritySampler
from ddtrace.sampler import BaseSampler
from ddtrace.sampler import DatadogSampler
from ddtrace.settings import Config
from ddtrace.settings.asm import config as asm_config
from ddtrace.settings.peer_service import _ps_config
from ddtrace.vendor.debtcollector import deprecate


log = get_logger(__name__)


_INTERNAL_APPLICATION_SPAN_TYPES = {"custom", "template", "web", "worker"}


AnyCallable = TypeVar("AnyCallable", bound=Callable)


def _start_appsec_processor() -> Optional[Any]:
    # FIXME: type should be AppsecSpanProcessor but we have a cyclic import here
    try:
        from ddtrace.appsec._processor import AppSecSpanProcessor

        return AppSecSpanProcessor()
    except Exception as e:
        # DDAS-001-01
        log.error(
            "[DDAS-001-01] "
            "AppSec could not start because of an unexpected error. No security activities will "
            "be collected. "
            "Please contact support at https://docs.datadoghq.com/help/ for help. Error details: "
            "\n%s",
            repr(e),
        )
        if config._raise:
            raise
    return None


def _default_span_processors_factory(
    trace_filters: List[TraceFilter],
    trace_writer: TraceWriter,
    partial_flush_enabled: bool,
    partial_flush_min_spans: int,
    appsec_enabled: bool,
    iast_enabled: bool,
    compute_stats_enabled: bool,
    single_span_sampling_rules: List[SpanSamplingRule],
    agent_url: str,
    trace_sampler: BaseSampler,
    profiling_span_processor: EndpointCallCounterProcessor,
    apm_opt_out: bool = False,
) -> Tuple[List[SpanProcessor], Optional[Any], List[SpanProcessor]]:
    # FIXME: type should be AppsecSpanProcessor but we have a cyclic import here
    """Construct the default list of span processors to use."""
    trace_processors: List[TraceProcessor] = []
    trace_processors += [
        PeerServiceProcessor(_ps_config),
        BaseServiceProcessor(),
        TraceSamplingProcessor(compute_stats_enabled, trace_sampler, single_span_sampling_rules, apm_opt_out),
        TraceTagsProcessor(),
    ]
    trace_processors += trace_filters

    span_processors: List[SpanProcessor] = []
    span_processors += [TopLevelSpanProcessor()]

    if asm_config._asm_libddwaf_available:
        if appsec_enabled:
            if asm_config._api_security_enabled:
                from ddtrace.appsec._api_security.api_manager import APIManager

                APIManager.enable()

            appsec_processor = _start_appsec_processor()
            if appsec_processor:
                span_processors.append(appsec_processor)
        else:
            # api_security_active will keep track of the service status of APIManager
            # we don't want to import the module if it was not started before due to
            # one click activation of ASM via Remote Config
            if asm_config._api_security_active:
                from ddtrace.appsec._api_security.api_manager import APIManager

                APIManager.disable()

            appsec_processor = None
    else:
        appsec_processor = None

    if iast_enabled:
        from ddtrace.appsec._iast.processor import AppSecIastSpanProcessor

        span_processors.append(AppSecIastSpanProcessor())

    if compute_stats_enabled:
        # Inline the import to avoid pulling in ddsketch or protobuf
        # when importing ddtrace.
        from ddtrace.internal.processor.stats import SpanStatsProcessorV06

        span_processors.append(
            SpanStatsProcessorV06(
                agent_url,
            ),
        )

    span_processors.append(profiling_span_processor)

    # These need to run after all the other processors
    deferred_processors: List[SpanProcessor] = [
        SpanAggregator(
            partial_flush_enabled=partial_flush_enabled,
            partial_flush_min_spans=partial_flush_min_spans,
            trace_processors=trace_processors,
            writer=trace_writer,
        )
    ]
    return span_processors, appsec_processor, deferred_processors


class Tracer(object):
    """
    Tracer is used to create, sample and submit spans that measure the
    execution time of sections of code.

    If you're running an application that will serve a single trace per thread,
    you can use the global tracer instance::

        from ddtrace import tracer
        trace = tracer.trace('app.request', 'web-server').finish()
    """

    SHUTDOWN_TIMEOUT = 5

    def __init__(
        self,
        url: Optional[str] = None,
        dogstatsd_url: Optional[str] = None,
        context_provider: Optional[DefaultContextProvider] = None,
    ) -> None:
        """
        Create a new ``Tracer`` instance. A global tracer is already initialized
        for common usage, so there is no need to initialize your own ``Tracer``.

        :param url: The Datadog agent URL.
        :param dogstatsd_url: The DogStatsD URL.
        """

        maybe_start_serverless_mini_agent()

        self._filters: List[TraceFilter] = []

        # globally set tags
        self._tags = config.tags.copy()

        # collection of services seen, used for runtime metrics tags
        # a buffer for service info so we don't perpetually send the same things
        self._services: Set[str] = set()
        if config.service:
            self._services.add(config.service)

        # Runtime id used for associating data collected during runtime to
        # traces
        self._pid = getpid()

        self.enabled = config._tracing_enabled
        self.context_provider = context_provider or DefaultContextProvider()
        # _user_sampler is the backup in case we need to revert from remote config to local
        self._user_sampler: Optional[BaseSampler] = DatadogSampler()
        self._asm_enabled = asm_config._asm_enabled
        self._appsec_standalone_enabled = asm_config._appsec_standalone_enabled
        self._sampler: BaseSampler = DatadogSampler()
        self._maybe_opt_out()
        self._dogstatsd_url = agent.get_stats_url() if dogstatsd_url is None else dogstatsd_url
        self._compute_stats = config._trace_compute_stats
        self._agent_url: str = agent.get_trace_url() if url is None else url
        verify_url(self._agent_url)

        if self._use_log_writer() and url is None:
            writer: TraceWriter = LogWriter()
        else:
            writer = AgentWriter(
                agent_url=self._agent_url,
                dogstatsd=get_dogstatsd_client(self._dogstatsd_url),
                sync_mode=self._use_sync_mode(),
                headers={"Datadog-Client-Computed-Stats": "yes"} if (self._compute_stats or self._apm_opt_out) else {},
                report_metrics=not self._apm_opt_out,
                response_callback=self._agent_response_callback,
            )
        self._single_span_sampling_rules: List[SpanSamplingRule] = get_span_sampling_rules()
        self._writer: TraceWriter = writer
        self._partial_flush_enabled = config._partial_flush_enabled
        self._partial_flush_min_spans = config._partial_flush_min_spans
        # Direct link to the appsec processor
        self._appsec_processor = None
        self._iast_enabled = asm_config._iast_enabled
        self._endpoint_call_counter_span_processor = EndpointCallCounterProcessor()
        self._span_processors, self._appsec_processor, self._deferred_processors = _default_span_processors_factory(
            self._filters,
            self._writer,
            self._partial_flush_enabled,
            self._partial_flush_min_spans,
            self._asm_enabled,
            self._iast_enabled,
            self._compute_stats,
            self._single_span_sampling_rules,
            self._agent_url,
            self._sampler,
            self._endpoint_call_counter_span_processor,
            self._apm_opt_out,
        )
        if config._data_streams_enabled:
            # Inline the import to avoid pulling in ddsketch or protobuf
            # when importing ddtrace.
            from ddtrace.internal.datastreams.processor import DataStreamsProcessor

            self.data_streams_processor = DataStreamsProcessor(self._agent_url)
            register_on_exit_signal(self._atexit)

        self._hooks = _hooks.Hooks()
        atexit.register(self._atexit)
        forksafe.register_before_fork(self._sample_before_fork)
        forksafe.register(self._child_after_fork)

        self._shutdown_lock = RLock()

        self._new_process = False
        config._subscribe(["_trace_sample_rate", "_trace_sampling_rules"], self._on_global_config_update)
        config._subscribe(["logs_injection"], self._on_global_config_update)
        config._subscribe(["tags"], self._on_global_config_update)
        config._subscribe(["_tracing_enabled"], self._on_global_config_update)

    def _maybe_opt_out(self):
        self._apm_opt_out = self._asm_enabled and self._appsec_standalone_enabled
        if self._apm_opt_out:
            # If ASM is enabled but tracing is disabled,
            # we need to set the rate limiting to 1 trace per minute
            # for the backend to consider the service as alive.
            from ddtrace.internal.rate_limiter import RateLimiter

            self._sampler.limiter = RateLimiter(rate_limit=1, time_window=60e9)  # 1 trace per minute
            # Disable compute stats (neither agent or tracer should compute them)
            config._trace_compute_stats = False
            self.enabled = False

    def _atexit(self) -> None:
        key = "ctrl-break" if os.name == "nt" else "ctrl-c"
        log.debug(
            "Waiting %d seconds for tracer to finish. Hit %s to quit.",
            self.SHUTDOWN_TIMEOUT,
            key,
        )
        self.shutdown(timeout=self.SHUTDOWN_TIMEOUT)

    def sample(self, span):
        if self._sampler is not None:
            self._sampler.sample(span)
        else:
            log.error("No sampler available to sample span")

    @property
    def sampler(self):
        deprecate(
            "tracer.sampler is deprecated and will be removed.",
            message="To manually sample call tracer.sample(span) instead.",
            category=DDTraceDeprecationWarning,
        )
        return self._sampler

    @sampler.setter
    def sampler(self, value):
        deprecate(
            "Setting a custom sampler is deprecated and will be removed.",
            message="""Please use DD_TRACE_SAMPLING_RULES to configure the sampler instead:
    https://ddtrace.readthedocs.io/en/stable/configuration.html#DD_TRACE_SAMPLING_RULES""",
            category=DDTraceDeprecationWarning,
        )
        if self._apm_opt_out:
            log.warning("Cannot set a custom sampler with Standalone ASM mode")
            return
        self._sampler = value

    def on_start_span(self, func: Callable) -> Callable:
        """Register a function to execute when a span start.

        Can be used as a decorator.

        :param func: The function to call when starting a span.
                     The started span will be passed as argument.
        """
        self._hooks.register(self.__class__.start_span, func)
        return func

    def deregister_on_start_span(self, func: Callable) -> Callable:
        """Unregister a function registered to execute when a span starts.

        Can be used as a decorator.

        :param func: The function to stop calling when starting a span.
        """

        self._hooks.deregister(self.__class__.start_span, func)
        return func

    def _sample_before_fork(self) -> None:
        span = self.current_root_span()
        if span is not None and span.context.sampling_priority is None:
            self.sample(span)

    @property
    def _sampler(self):
        return self._sampler_current

    @_sampler.setter
    def _sampler(self, value):
        self._sampler_current = value
        # we need to update the processor that uses the sampler
        if getattr(self, "_deferred_processors", None):
            for aggregator in self._deferred_processors:
                if type(aggregator) == SpanAggregator:
                    for processor in aggregator._trace_processors:
                        if type(processor) == TraceSamplingProcessor:
                            processor.sampler = value
                            break
            else:
                log.debug("No TraceSamplingProcessor available to update sampling rate")

    @property
    def debug_logging(self):
        return log.isEnabledFor(logging.DEBUG)

    def current_trace_context(self, *args, **kwargs) -> Optional[Context]:
        """Return the context for the current trace.

        If there is no active trace then None is returned.
        """
        active = self.context_provider.active()
        if isinstance(active, Context):
            return active
        elif isinstance(active, Span):
            return active.context
        return None

    def get_log_correlation_context(self, active: Optional[Union[Context, Span]] = None) -> Dict[str, str]:
        """Retrieves the data used to correlate a log with the current active trace.
        Generates a dictionary for custom logging instrumentation including the trace id and
        span id of the current active span, as well as the configured service, version, and environment names.
        If there is no active span, a dictionary with an empty string for each value will be returned.
        """
        if active is None and (self.enabled or self._apm_opt_out):
            active = self.context_provider.active()

        if isinstance(active, Span) and active.service:
            service = active.service
        else:
            service = config.service

        span_id = "0"
        trace_id = "0"
        if active:
            span_id = str(active.span_id) if active.span_id else span_id
            trace_id = format_trace_id(active.trace_id) if active.trace_id else trace_id

        return {
            "trace_id": trace_id,
            "span_id": span_id,
            "service": service or "",
            "version": config.version or "",
            "env": config.env or "",
        }

    # TODO: deprecate this method and make sure users create a new tracer if they need different parameters
    def configure(
        self,
        enabled: Optional[bool] = None,
        hostname: Optional[str] = None,
        port: Optional[int] = None,
        uds_path: Optional[str] = None,
        https: Optional[bool] = None,
        sampler: Optional[BaseSampler] = None,
        context_provider: Optional[DefaultContextProvider] = None,
        wrap_executor: Optional[Callable] = None,
        priority_sampling: Optional[bool] = None,
        settings: Optional[Dict[str, Any]] = None,
        dogstatsd_url: Optional[str] = None,
        writer: Optional[TraceWriter] = None,
        partial_flush_enabled: Optional[bool] = None,
        partial_flush_min_spans: Optional[int] = None,
        api_version: Optional[str] = None,
        compute_stats_enabled: Optional[bool] = None,
        appsec_enabled: Optional[bool] = None,
        iast_enabled: Optional[bool] = None,
        appsec_standalone_enabled: Optional[bool] = None,
    ) -> None:
        """Configure a Tracer.

        :param bool enabled: If True, finished traces will be submitted to the API, else they'll be dropped.
        :param str hostname: Hostname running the Trace Agent
        :param int port: Port of the Trace Agent
        :param str uds_path: The Unix Domain Socket path of the agent.
        :param bool https: Whether to use HTTPS or HTTP.
        :param object sampler: A custom Sampler instance, locally deciding to totally drop the trace or not.
        :param object context_provider: The ``ContextProvider`` that will be used to retrieve
            automatically the current call context. This is an advanced option that usually
            doesn't need to be changed from the default value
        :param object wrap_executor: callable that is used when a function is decorated with
            ``Tracer.wrap()``. This is an advanced option that usually doesn't need to be changed
            from the default value
        :param priority_sampling: This argument is deprecated and will be removed in a future version.
        :param str dogstatsd_url: URL for UDP or Unix socket connection to DogStatsD
        """
        if enabled is not None:
            self.enabled = enabled

        if priority_sampling is not None:
            deprecate(
                "Configuring priority sampling on tracing clients is deprecated",
                version="3.0.0",
                category=DDTraceDeprecationWarning,
            )

        if settings is not None:
            self._filters = settings.get("FILTERS") or self._filters

        if partial_flush_enabled is not None:
            self._partial_flush_enabled = partial_flush_enabled

        if partial_flush_min_spans is not None:
            self._partial_flush_min_spans = partial_flush_min_spans

        if appsec_enabled is not None:
            self._asm_enabled = asm_config._asm_enabled = appsec_enabled

        if iast_enabled is not None:
            self._iast_enabled = asm_config._iast_enabled = iast_enabled

        if appsec_standalone_enabled is not None:
            self._appsec_standalone_enabled = asm_config._appsec_standalone_enabled = appsec_standalone_enabled

        if sampler is not None:
            self._sampler = sampler
            self._user_sampler = self._sampler

        self._maybe_opt_out()

        self._dogstatsd_url = dogstatsd_url or self._dogstatsd_url

        if any(x is not None for x in [hostname, port, uds_path, https]):
            # If any of the parts of the URL have updated, merge them with
            # the previous writer values.
            prev_url_parsed = compat.parse.urlparse(self._agent_url)

            if uds_path is not None:
                if hostname is None and prev_url_parsed.scheme == "unix":
                    hostname = prev_url_parsed.hostname
                new_url = "unix://%s%s" % (hostname or "", uds_path)
            else:
                if https is None:
                    https = prev_url_parsed.scheme == "https"
                if hostname is None:
                    hostname = prev_url_parsed.hostname or ""
                if port is None:
                    port = prev_url_parsed.port
                scheme = "https" if https else "http"
                new_url = "%s://%s:%s" % (scheme, hostname, port)
            verify_url(new_url)
            self._agent_url = new_url
        else:
            new_url = None

        if compute_stats_enabled is not None:
            self._compute_stats = compute_stats_enabled

        try:
            self._writer.stop()
        except ServiceStatusError:
            # It's possible the writer never got started
            pass

        if writer is not None:
            self._writer = writer
        elif any(x is not None for x in [new_url, api_version, sampler, dogstatsd_url, appsec_enabled]):
            if self._asm_enabled:
                api_version = "v0.4"
            self._writer = AgentWriter(
                self._agent_url,
                dogstatsd=get_dogstatsd_client(self._dogstatsd_url),
                sync_mode=self._use_sync_mode(),
                api_version=api_version,
                # if apm opt out, neither agent or tracer should compute the stats
                headers=(
                    {"Datadog-Client-Computed-Stats": "yes"} if (compute_stats_enabled or self._apm_opt_out) else {}
                ),
                report_metrics=not self._apm_opt_out,
                response_callback=self._agent_response_callback,
            )
        elif writer is None and isinstance(self._writer, LogWriter):
            # No need to do anything for the LogWriter.
            pass
        if isinstance(self._writer, AgentWriter):
            self._writer.dogstatsd = get_dogstatsd_client(self._dogstatsd_url)

        if any(
            x is not None
            for x in [
                partial_flush_min_spans,
                partial_flush_enabled,
                writer,
                dogstatsd_url,
                hostname,
                port,
                https,
                uds_path,
                api_version,
                sampler,
                settings.get("FILTERS") if settings is not None else None,
                compute_stats_enabled,
                appsec_enabled,
                iast_enabled,
            ]
        ):
            self._span_processors, self._appsec_processor, self._deferred_processors = _default_span_processors_factory(
                self._filters,
                self._writer,
                self._partial_flush_enabled,
                self._partial_flush_min_spans,
                self._asm_enabled,
                self._iast_enabled,
                self._compute_stats,
                self._single_span_sampling_rules,
                self._agent_url,
                self._sampler,
                self._endpoint_call_counter_span_processor,
                self._apm_opt_out,
            )

        if context_provider is not None:
            self.context_provider = context_provider

        if wrap_executor is not None:
            self._wrap_executor = wrap_executor

        self._generate_diagnostic_logs()

    def _agent_response_callback(self, resp: AgentResponse) -> None:
        """Handle the response from the agent.

        The agent can return updated sample rates for the priority sampler.
        """
        try:
            if isinstance(self._sampler, BasePrioritySampler):
                self._sampler.update_rate_by_service_sample_rates(
                    resp.rate_by_service,
                )
        except ValueError:
            log.error("sample_rate is negative, cannot update the rate samplers")

    def _generate_diagnostic_logs(self):
        if config._debug_mode or config._startup_logs_enabled:
            try:
                info = debug.collect(self)
            except Exception as e:
                msg = "Failed to collect start-up logs: %s" % e
                self._log_compat(logging.WARNING, "- DATADOG TRACER DIAGNOSTIC - %s" % msg)
            else:
                if log.isEnabledFor(logging.INFO):
                    msg = "- DATADOG TRACER CONFIGURATION - %s" % info
                    self._log_compat(logging.INFO, msg)

                # Always log errors since we're either in debug_mode or start up logs
                # are enabled.
                agent_error = info.get("agent_error")
                if agent_error:
                    msg = "- DATADOG TRACER DIAGNOSTIC - %s" % agent_error
                    self._log_compat(logging.WARNING, msg)

    def _child_after_fork(self):
        self._pid = getpid()

        # Assume that the services of the child are not necessarily a subset of those
        # of the parent.
        self._services = set()
        if config.service:
            self._services.add(config.service)

        # Re-create the background writer thread
        self._writer = self._writer.recreate()
        self._span_processors, self._appsec_processor, self._deferred_processors = _default_span_processors_factory(
            self._filters,
            self._writer,
            self._partial_flush_enabled,
            self._partial_flush_min_spans,
            self._asm_enabled,
            self._iast_enabled,
            self._compute_stats,
            self._single_span_sampling_rules,
            self._agent_url,
            self._sampler,
            self._endpoint_call_counter_span_processor,
            self._apm_opt_out,
        )

        self._new_process = True

    def _start_span_after_shutdown(
        self,
        name: str,
        child_of: Optional[Union[Span, Context]] = None,
        service: Optional[str] = None,
        resource: Optional[str] = None,
        span_type: Optional[str] = None,
        activate: bool = False,
        span_api: str = SPAN_API_DATADOG,
    ) -> Span:
        log.warning("Spans started after the tracer has been shut down will not be sent to the Datadog Agent.")
        return self._start_span(name, child_of, service, resource, span_type, activate, span_api)

    def _start_span(
        self,
        name: str,
        child_of: Optional[Union[Span, Context]] = None,
        service: Optional[str] = None,
        resource: Optional[str] = None,
        span_type: Optional[str] = None,
        activate: bool = False,
        span_api: str = SPAN_API_DATADOG,
    ) -> Span:
        """Return a span that represents an operation called ``name``.

        Note that the :meth:`.trace` method will almost always be preferred
        over this method as it provides automatic span parenting. This method
        should only be used if manual parenting is desired.

        :param str name: the name of the operation being traced.
        :param object child_of: a ``Span`` or a ``Context`` instance representing the parent for this span.
        :param str service: the name of the service being traced.
        :param str resource: an optional name of the resource being tracked.
        :param str span_type: an optional operation type.
        :param activate: activate the span once it is created.

        To start a new root span::

            span = tracer.start_span("web.request")

        To create a child for a root span::

            root_span = tracer.start_span("web.request")
            span = tracer.start_span("web.decoder", child_of=root_span)

        Spans from ``start_span`` are not activated by default::

            with tracer.start_span("parent") as parent:
                assert tracer.current_span() is None
                with tracer.start_span("child", child_of=parent):
                    assert tracer.current_span() is None

            new_parent = tracer.start_span("new_parent", activate=True)
            assert tracer.current_span() is new_parent

        Note: be sure to finish all spans to avoid memory leaks and incorrect
        parenting of spans.
        """
        if self._new_process:
            self._new_process = False

            # The spans remaining in the context can not and will not be
            # finished in this new process. So to avoid memory leaks the
            # strong span reference (which will never be finished) is replaced
            # with a context representing the span.
            if isinstance(child_of, Span):
                new_ctx = Context(
                    sampling_priority=child_of.context.sampling_priority,
                    span_id=child_of.span_id,
                    trace_id=child_of.trace_id,
                    is_remote=False,
                )

                # If the child_of span was active then activate the new context
                # containing it so that the strong span referenced is removed
                # from the execution.
                if self.context_provider.active() is child_of:
                    self.context_provider.activate(new_ctx)
                child_of = new_ctx

        parent: Optional[Span] = None
        if child_of is not None:
            if isinstance(child_of, Context):
                context = child_of
            else:
                context = child_of.context
                parent = child_of
        else:
            context = Context(is_remote=False)

        trace_id = context.trace_id
        parent_id = context.span_id

        # The following precedence is used for a new span's service:
        # 1. Explicitly provided service name
        #     a. User provided or integration provided service name
        # 2. Parent's service name (if defined)
        # 3. Globally configured service name
        #     a. `config.service`/`DD_SERVICE`/`DD_TAGS`
        if service is None:
            if parent:
                service = parent.service
            else:
                service = config.service

        # Update the service name based on any mapping
        service = config.service_mapping.get(service, service)

        links = context._span_links if not parent else []

        if trace_id:
            # child_of a non-empty context, so either a local child span or from a remote context
            span = Span(
                name=name,
                context=context,
                trace_id=trace_id,
                parent_id=parent_id,
                service=service,
                resource=resource,
                span_type=span_type,
                span_api=span_api,
                links=links,
                on_finish=[self._on_span_finish],
            )

            # Extra attributes when from a local parent
            if parent:
                span._parent = parent
                span._local_root = parent._local_root

            for k, v in _get_metas_to_propagate(context):
                # We do not want to propagate AppSec propagation headers
                # to children spans, only across distributed spans
                if k not in (SAMPLING_DECISION_TRACE_TAG_KEY, APPSEC.PROPAGATION_HEADER):
                    span._meta[k] = v
        else:
            # this is the root span of a new trace
            span = Span(
                name=name,
                context=context,
                service=service,
                resource=resource,
                span_type=span_type,
                span_api=span_api,
                on_finish=[self._on_span_finish],
            )
            if config.report_hostname:
                span.set_tag_str(HOSTNAME_KEY, hostname.get_hostname())

        if not span._parent:
            span.set_tag_str("runtime-id", get_runtime_id())
            span._metrics[PID] = self._pid

        # Apply default global tags.
        if self._tags:
            span.set_tags(self._tags)

        if config.env:
            span.set_tag_str(ENV_KEY, config.env)

        # Only set the version tag on internal spans.
        if config.version:
            root_span = self.current_root_span()
            # if: 1. the span is the root span and the span's service matches the global config; or
            #     2. the span is not the root, but the root span's service matches the span's service
            #        and the root span has a version tag
            # then the span belongs to the user application and so set the version tag
            if (root_span is None and service == config.service) or (
                root_span and root_span.service == service and root_span.get_tag(VERSION_KEY) is not None
            ):
                span.set_tag_str(VERSION_KEY, config.version)

        if activate:
            self.context_provider.activate(span)

        # update set of services handled by tracer
        if service and service not in self._services and self._is_span_internal(span):
            self._services.add(service)

        # Only call span processors if the tracer is enabled (even if APM opted out)
        if self.enabled or self._apm_opt_out:
            for p in chain(self._span_processors, SpanProcessor.__processors__, self._deferred_processors):
                p.on_span_start(span)
        self._hooks.emit(self.__class__.start_span, span)

        return span

    start_span = _start_span

    def _on_span_finish(self, span: Span) -> None:
        active = self.current_span()
        # Debug check: if the finishing span has a parent and its parent
        # is not the next active span then this is an error in synchronous tracing.
        if span._parent is not None and active is not span._parent:
            log.debug("span %r closing after its parent %r, this is an error when not using async", span, span._parent)

        # Only call span processors if the tracer is enabled (even if APM opted out)
        if self.enabled or self._apm_opt_out:
            for p in chain(self._span_processors, SpanProcessor.__processors__, self._deferred_processors):
                p.on_span_finish(span)

        if log.isEnabledFor(logging.DEBUG):
            log.debug("finishing span %s (enabled:%s)", span._pprint(), self.enabled)

    def _log_compat(self, level, msg):
        """Logs a message for the given level.

        Instead, something like this will be printed to stderr:
            No handlers could be found for logger "ddtrace.tracer"

        Since the global tracer is configured on import and it is recommended
        to import the tracer as early as possible, it will likely be the case
        that there are no handlers installed yet.
        """
        log.log(level, msg)

    def trace(
        self,
        name: str,
        service: Optional[str] = None,
        resource: Optional[str] = None,
        span_type: Optional[str] = None,
        span_api: str = SPAN_API_DATADOG,
    ) -> Span:
        """Activate and return a new span that inherits from the current active span.

        :param str name: the name of the operation being traced
        :param str service: the name of the service being traced. If not set,
                            it will inherit the service from its parent.
        :param str resource: an optional name of the resource being tracked.
        :param str span_type: an optional operation type.

        The returned span *must* be ``finish``'d or it will remain in memory
        indefinitely::

            >>> span = tracer.trace("web.request")
                try:
                    # do something
                finally:
                    span.finish()

            >>> with tracer.trace("web.request") as span:
                    # do something

        Example of the automatic parenting::

            parent = tracer.trace("parent")     # has no parent span
            assert tracer.current_span() is parent

            child  = tracer.trace("child")
            assert child.parent_id == parent.span_id
            assert tracer.current_span() is child
            child.finish()

            # parent is now the active span again
            assert tracer.current_span() is parent
            parent.finish()

            assert tracer.current_span() is None

            parent2 = tracer.trace("parent2")
            assert parent2.parent_id is None
            parent2.finish()
        """
        return self.start_span(
            name,
            child_of=self.context_provider.active(),
            service=service,
            resource=resource,
            span_type=span_type,
            activate=True,
            span_api=span_api,
        )

    def current_root_span(self) -> Optional[Span]:
        """Returns the root span of the current execution.

        This is useful for attaching information related to the trace as a
        whole without needing to add to child spans.

        For example::

            # get the root span
            root_span = tracer.current_root_span()
            # set the host just once on the root span
            if root_span:
                root_span.set_tag('host', '127.0.0.1')
        """
        span = self.current_span()
        if span is None:
            return None
        return span._local_root

    def current_span(self) -> Optional[Span]:
        """Return the active span in the current execution context.

        Note that there may be an active span represented by a context object
        (like from a distributed trace) which will not be returned by this
        method.
        """
        active = self.context_provider.active()
        return active if isinstance(active, Span) else None

    @property
    def agent_trace_url(self) -> Optional[str]:
        """Trace agent url"""
        if isinstance(self._writer, AgentWriter):
            return self._writer.agent_url

        return None

    def flush(self):
        """Flush the buffer of the trace writer. This does nothing if an unbuffered trace writer is used."""
        self._writer.flush_queue()

    def wrap(
        self,
        name: Optional[str] = None,
        service: Optional[str] = None,
        resource: Optional[str] = None,
        span_type: Optional[str] = None,
    ) -> Callable[[AnyCallable], AnyCallable]:
        """
        A decorator used to trace an entire function. If the traced function
        is a coroutine, it traces the coroutine execution when is awaited.
        If a ``wrap_executor`` callable has been provided in the ``Tracer.configure()``
        method, it will be called instead of the default one when the function
        decorator is invoked.

        :param str name: the name of the operation being traced. If not set,
                         defaults to the fully qualified function name.
        :param str service: the name of the service being traced. If not set,
                            it will inherit the service from it's parent.
        :param str resource: an optional name of the resource being tracked.
        :param str span_type: an optional operation type.

        >>> @tracer.wrap('my.wrapped.function', service='my.service')
            def run():
                return 'run'

        >>> # name will default to 'execute' if unset
            @tracer.wrap()
            def execute():
                return 'executed'

        >>> # or use it in asyncio coroutines
            @tracer.wrap()
            async def coroutine():
                return 'executed'

        >>> @tracer.wrap()
            @asyncio.coroutine
            def coroutine():
                return 'executed'

        You can access the current span using `tracer.current_span()` to set
        tags:

        >>> @tracer.wrap()
            def execute():
                span = tracer.current_span()
                span.set_tag('a', 'b')
        """

        def wrap_decorator(f: AnyCallable) -> AnyCallable:
            # FIXME[matt] include the class name for methods.
            span_name = name if name else "%s.%s" % (f.__module__, f.__name__)

            # detect if the the given function is a coroutine to use the
            # right decorator; this initial check ensures that the
            # evaluation is done only once for each @tracer.wrap
            if compat.iscoroutinefunction(f):
                # call the async factory that creates a tracing decorator capable
                # to await the coroutine execution before finishing the span. This
                # code is used for compatibility reasons to prevent Syntax errors
                # in Python 2
                func_wrapper = compat.make_async_decorator(
                    self,
                    f,
                    span_name,
                    service=service,
                    resource=resource,
                    span_type=span_type,
                )
            else:

                @functools.wraps(f)
                def func_wrapper(*args, **kwargs):
                    # if a wrap executor has been configured, it is used instead
                    # of the default tracing function
                    if getattr(self, "_wrap_executor", None):
                        return self._wrap_executor(
                            self,
                            f,
                            args,
                            kwargs,
                            span_name,
                            service=service,
                            resource=resource,
                            span_type=span_type,
                        )

                    # otherwise fallback to a default tracing
                    with self.trace(span_name, service=service, resource=resource, span_type=span_type):
                        return f(*args, **kwargs)

            return func_wrapper

        return wrap_decorator

    def set_tags(self, tags: Dict[str, str]) -> None:
        """Set some tags at the tracer level.
        This will append those tags to each span created by the tracer.

        :param dict tags: dict of tags to set at tracer level
        """
        self._tags.update(tags)

    def shutdown(self, timeout: Optional[float] = None) -> None:
        """Shutdown the tracer and flush finished traces. Avoid calling shutdown multiple times.

        :param timeout: How long in seconds to wait for the background worker to flush traces
            before exiting or :obj:`None` to block until flushing has successfully completed (default: :obj:`None`)
        :type timeout: :obj:`int` | :obj:`float` | :obj:`None`
        """
        with self._shutdown_lock:
            # Thread safety: Ensures tracer is shutdown synchronously
            span_processors = self._span_processors
            deferred_processors = self._deferred_processors
            self._span_processors = []
            self._deferred_processors = []

            for processor in chain(span_processors, SpanProcessor.__processors__, deferred_processors):
                if hasattr(processor, "shutdown"):
                    processor.shutdown(timeout)

            atexit.unregister(self._atexit)
            forksafe.unregister(self._child_after_fork)
            forksafe.unregister_before_fork(self._sample_before_fork)

        self.start_span = self._start_span_after_shutdown  # type: ignore[assignment]

    @staticmethod
    def _use_log_writer() -> bool:
        """Returns whether the LogWriter should be used in the environment by
        default.

        The LogWriter required by default in AWS Lambdas when the Datadog Agent extension
        is not available in the Lambda.
        """
        if (
            environ.get("DD_AGENT_HOST")
            or environ.get("DATADOG_TRACE_AGENT_HOSTNAME")
            or environ.get("DD_TRACE_AGENT_URL")
        ):
            # If one of these variables are set, we definitely have an agent
            return False
        elif in_aws_lambda() and has_aws_lambda_agent_extension():
            # If the Agent Lambda extension is available then an AgentWriter is used.
            return False
        elif in_gcp_function() or in_azure_function():
            return False
        else:
            return in_aws_lambda()

    @staticmethod
    def _use_sync_mode() -> bool:
        """Returns, if an `AgentWriter` is to be used, whether it should be run
         in synchronous mode by default.

        There are only two cases in which this is desirable:

        - AWS Lambdas can have the Datadog agent installed via an extension.
          When it's available traces must be sent synchronously to ensure all
          are received before the Lambda terminates.
        - Google Cloud Functions and Azure Functions have a mini-agent spun up by the tracer.
          Similarly to AWS Lambdas, sync mode should be used to avoid data loss.
        """
        return (in_aws_lambda() and has_aws_lambda_agent_extension()) or in_gcp_function() or in_azure_function()

    @staticmethod
    def _is_span_internal(span):
        return not span.span_type or span.span_type in _INTERNAL_APPLICATION_SPAN_TYPES

    def _on_global_config_update(self, cfg: Config, items: List[str]) -> None:
        # sampling configs always come as a pair
        if "_trace_sample_rate" in items and "_trace_sampling_rules" in items:
            self._handle_sampler_update(cfg)

        if "tags" in items:
            self._tags = cfg.tags.copy()

        if "_tracing_enabled" in items:
            if self.enabled:
                if cfg._tracing_enabled is False:
                    self.enabled = False
            else:
                # the product specification says not to allow tracing to be re-enabled remotely at runtime
                if cfg._tracing_enabled is True and cfg._get_source("_tracing_enabled") != "remote_config":
                    self.enabled = True

        if "logs_injection" in items:
            if config.logs_injection:
                from ddtrace.contrib.logging import patch

                patch()
            else:
                from ddtrace.contrib.logging import unpatch

                unpatch()

    def _handle_sampler_update(self, cfg: Config) -> None:
        if (
            cfg._get_source("_trace_sample_rate") != "remote_config"
            and cfg._get_source("_trace_sampling_rules") != "remote_config"
            and self._user_sampler
        ):
            # if we get empty configs from rc for both sample rate and rules, we should revert to the user sampler
            self.sampler = self._user_sampler
            return

        if cfg._get_source("_trace_sample_rate") != "remote_config" and self._user_sampler:
            try:
                sample_rate = self._user_sampler.default_sample_rate  # type: ignore[attr-defined]
            except AttributeError:
                log.debug("Custom non-DatadogSampler is being used, cannot pull default sample rate")
                sample_rate = None
        elif cfg._get_source("_trace_sample_rate") != "default":
            sample_rate = cfg._trace_sample_rate
        else:
            sample_rate = None

        if cfg._get_source("_trace_sampling_rules") != "remote_config" and self._user_sampler:
            try:
                sampling_rules = self._user_sampler.rules  # type: ignore[attr-defined]
                # we need to chop off the default_sample_rate rule so the new sample_rate can be applied
                sampling_rules = sampling_rules[:-1]
            except AttributeError:
                log.debug("Custom non-DatadogSampler is being used, cannot pull sampling rules")
                sampling_rules = None
        elif cfg._get_source("_trace_sampling_rules") != "default":
            sampling_rules = DatadogSampler._parse_rules_from_str(cfg._trace_sampling_rules)
        else:
            sampling_rules = None

        sampler = DatadogSampler(rules=sampling_rules, default_sample_rate=sample_rate)

        self._sampler = sampler
