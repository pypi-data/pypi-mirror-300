import abc
from collections import defaultdict
from threading import Lock
from threading import RLock
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

from ddtrace import config
from ddtrace._trace.span import Span
from ddtrace._trace.span import _get_64_highest_order_bits_as_hex
from ddtrace._trace.span import _is_top_level
from ddtrace.constants import _APM_ENABLED_METRIC_KEY as MK_APM_ENABLED
from ddtrace.constants import SAMPLING_PRIORITY_KEY
from ddtrace.constants import USER_KEEP
from ddtrace.internal import gitmetadata
from ddtrace.internal import telemetry
from ddtrace.internal.constants import HIGHER_ORDER_TRACE_ID_BITS
from ddtrace.internal.constants import LAST_DD_PARENT_ID_KEY
from ddtrace.internal.constants import MAX_UINT_64BITS
from ddtrace.internal.logger import get_logger
from ddtrace.internal.sampling import SpanSamplingRule
from ddtrace.internal.sampling import is_single_span_sampled
from ddtrace.internal.service import ServiceStatusError
from ddtrace.internal.telemetry.constants import TELEMETRY_LOG_LEVEL
from ddtrace.internal.telemetry.constants import TELEMETRY_NAMESPACE_TAG_TRACER
from ddtrace.internal.writer import TraceWriter
from ddtrace.sampler import BaseSampler


try:
    from typing import DefaultDict  # noqa:F401
except ImportError:
    from collections import defaultdict as DefaultDict

log = get_logger(__name__)


class TraceProcessor(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        """Default post initializer which logs the representation of the
        TraceProcessor at the ``logging.DEBUG`` level.
        """
        log.debug("initialized trace processor %r", self)

    @abc.abstractmethod
    def process_trace(self, trace: List[Span]) -> Optional[List[Span]]:
        """Processes a trace.

        ``None`` can be returned to prevent the trace from being further
        processed.
        """
        pass


class SpanProcessor(metaclass=abc.ABCMeta):
    """A Processor is used to process spans as they are created and finished by a tracer."""

    __processors__: List["SpanProcessor"] = []

    def __init__(self) -> None:
        """Default post initializer which logs the representation of the
        Processor at the ``logging.DEBUG`` level.
        """
        log.debug("initialized processor %r", self)

    @abc.abstractmethod
    def on_span_start(self, span: Span) -> None:
        """Called when a span is started.

        This method is useful for making upfront decisions on spans.

        For example, a sampling decision can be made when the span is created
        based on its resource name.
        """
        pass

    @abc.abstractmethod
    def on_span_finish(self, span: Span) -> None:
        """Called with the result of any previous processors or initially with
        the finishing span when a span finishes.

        It can return any data which will be passed to any processors that are
        applied afterwards.
        """
        pass

    def shutdown(self, timeout: Optional[float]) -> None:
        """Called when the processor is done being used.

        Any clean-up or flushing should be performed with this method.
        """
        pass

    def register(self) -> None:
        """Register the processor with the global list of processors."""
        SpanProcessor.__processors__.append(self)

    def unregister(self) -> None:
        """Unregister the processor from the global list of processors."""
        try:
            SpanProcessor.__processors__.remove(self)
        except ValueError:
            log.warning("Span processor %r not registered", self)


class TraceSamplingProcessor(TraceProcessor):
    """Processor that runs both trace and span sampling rules.

    * Span sampling must be applied after trace sampling priority has been set.
    * Span sampling rules are specified with a sample rate or rate limit as well as glob patterns
      for matching spans on service and name.
    * If the span sampling decision is to keep the span, then span sampling metrics are added to the span.
    * If a dropped trace includes a span that had been kept by a span sampling rule, then the span is sent to the
      Agent even if the dropped trace is not (as is the case when trace stats computation is enabled).
    """

    def __init__(
        self,
        compute_stats_enabled: bool,
        sampler: BaseSampler,
        single_span_rules: List[SpanSamplingRule],
        apm_opt_out: bool,
    ):
        super(TraceSamplingProcessor, self).__init__()
        self._compute_stats_enabled = compute_stats_enabled
        self.sampler = sampler
        self.single_span_rules = single_span_rules
        self.apm_opt_out = apm_opt_out

    def process_trace(self, trace: List[Span]) -> Optional[List[Span]]:
        if trace:
            chunk_root = trace[0]
            root_ctx = chunk_root._context

            if self.apm_opt_out:
                chunk_root.set_metric(MK_APM_ENABLED, 0)

            # only trace sample if we haven't already sampled
            if root_ctx and root_ctx.sampling_priority is None:
                self.sampler.sample(trace[0])
            # When stats computation is enabled in the tracer then we can
            # safely drop the traces.
            if self._compute_stats_enabled and not self.apm_opt_out:
                priority = root_ctx.sampling_priority if root_ctx is not None else None
                if priority is not None and priority <= 0:
                    # When any span is marked as keep by a single span sampling
                    # decision then we still send all and only those spans.
                    single_spans = [_ for _ in trace if is_single_span_sampled(_)]

                    return single_spans or None

            # single span sampling rules are applied after trace sampling
            if self.single_span_rules:
                for span in trace:
                    if span.context.sampling_priority is not None and span.context.sampling_priority <= 0:
                        for rule in self.single_span_rules:
                            if rule.match(span):
                                rule.sample(span)
                                # If stats computation is enabled, we won't send all spans to the agent.
                                # In order to ensure that the agent does not update priority sampling rates
                                # due to single spans sampling, we set all of these spans to manual keep.
                                if config._trace_compute_stats:
                                    span.set_metric(SAMPLING_PRIORITY_KEY, USER_KEEP)
                                break

            return trace

        return None


class TopLevelSpanProcessor(SpanProcessor):
    """Processor marks spans as top level

    A span is top level when it is the entrypoint method for a request to a service.
    Top level span and service entry span are equivalent terms

    The "top level" metric will be used by the agent to calculate trace metrics
    and determine how spans should be displaced in the UI. If this metric is not
    set by the tracer the first span in a trace chunk will be marked as top level.

    """

    def on_span_start(self, _: Span) -> None:
        pass

    def on_span_finish(self, span: Span) -> None:
        # DEV: Update span after finished to avoid race condition
        if _is_top_level(span):
            span.set_metric("_dd.top_level", 1)


class TraceTagsProcessor(TraceProcessor):
    """Processor that applies trace-level tags to the trace."""

    def _set_git_metadata(self, chunk_root):
        repository_url, commit_sha, main_package = gitmetadata.get_git_tags()
        if repository_url:
            chunk_root.set_tag_str("_dd.git.repository_url", repository_url)
        if commit_sha:
            chunk_root.set_tag_str("_dd.git.commit.sha", commit_sha)
        if main_package:
            chunk_root.set_tag_str("_dd.python_main_package", main_package)

    def process_trace(self, trace: List[Span]) -> Optional[List[Span]]:
        if not trace:
            return trace

        chunk_root = trace[0]
        ctx = chunk_root._context
        if not ctx:
            return trace

        ctx._update_tags(chunk_root)
        self._set_git_metadata(chunk_root)
        chunk_root.set_tag_str("language", "python")
        # for 128 bit trace ids
        if chunk_root.trace_id > MAX_UINT_64BITS:
            trace_id_hob = _get_64_highest_order_bits_as_hex(chunk_root.trace_id)
            chunk_root.set_tag_str(HIGHER_ORDER_TRACE_ID_BITS, trace_id_hob)

        if LAST_DD_PARENT_ID_KEY in chunk_root._meta and chunk_root._parent is not None:
            # we should only set the last parent id on local root spans
            del chunk_root._meta[LAST_DD_PARENT_ID_KEY]
        return trace


class _Trace:
    def __init__(self, spans=None, num_finished=0):
        self.spans = spans if spans is not None else []
        self.num_finished = num_finished


class SpanAggregator(SpanProcessor):
    """Processor that aggregates spans together by trace_id and writes the
    spans to the provided writer when:
        - The collection is assumed to be complete. A collection of spans is
          assumed to be complete if all the spans that have been created with
          the trace_id have finished; or
        - A minimum threshold of spans (``partial_flush_min_spans``) have been
          finished in the collection and ``partial_flush_enabled`` is True.
    """

    def __init__(
        self,
        partial_flush_enabled: bool,
        partial_flush_min_spans: int,
        trace_processors: Iterable[TraceProcessor],
        writer: TraceWriter,
    ):
        self._partial_flush_enabled = partial_flush_enabled
        self._partial_flush_min_spans = partial_flush_min_spans
        self._trace_processors = trace_processors
        self._writer = writer

        self._traces: DefaultDict[int, _Trace] = defaultdict(lambda: _Trace())
        self._lock: Union[RLock, Lock] = RLock() if config._span_aggregator_rlock else Lock()

        # Tracks the number of spans created and tags each count with the api that was used
        # ex: otel api, opentracing api, datadog api
        self._span_metrics: Dict[str, DefaultDict] = {
            "spans_created": defaultdict(int),
            "spans_finished": defaultdict(int),
        }
        super(SpanAggregator, self).__init__()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self._partial_flush_enabled}, "
            f"{self._partial_flush_min_spans}, "
            f"{self._trace_processors}, "
            f"{self._writer})"
        )

    def on_span_start(self, span: Span) -> None:
        with self._lock:
            trace = self._traces[span.trace_id]
            trace.spans.append(span)
            self._span_metrics["spans_created"][span._span_api] += 1
            self._queue_span_count_metrics("spans_created", "integration_name")

    def on_span_finish(self, span: Span) -> None:
        with self._lock:
            self._span_metrics["spans_finished"][span._span_api] += 1

            # Calling finish on a span that we did not see the start for
            # DEV: This can occur if the SpanAggregator is recreated while there is a span in progress
            #      e.g. `tracer.configure()` is called after starting a span
            if span.trace_id not in self._traces:
                log_msg = "finished span not connected to a trace"
                telemetry.telemetry_writer.add_log(TELEMETRY_LOG_LEVEL.ERROR, log_msg)
                log.debug("%s: %s", log_msg, span)
                return

            trace = self._traces[span.trace_id]
            trace.num_finished += 1
            should_partial_flush = self._partial_flush_enabled and trace.num_finished >= self._partial_flush_min_spans
            if trace.num_finished == len(trace.spans) or should_partial_flush:
                trace_spans = trace.spans
                trace.spans = []
                if trace.num_finished < len(trace_spans):
                    finished = []
                    for s in trace_spans:
                        if s.finished:
                            finished.append(s)
                        else:
                            trace.spans.append(s)
                else:
                    finished = trace_spans

                num_finished = len(finished)
                trace.num_finished -= num_finished
                if trace.num_finished != 0:
                    log_msg = "unexpected finished span count"
                    telemetry.telemetry_writer.add_log(TELEMETRY_LOG_LEVEL.ERROR, log_msg)
                    log.debug("%s (%s) for span %s", log_msg, num_finished, span)
                    trace.num_finished = 0

                # If we have removed all spans from this trace, then delete the trace from the traces dict
                if len(trace.spans) == 0:
                    del self._traces[span.trace_id]

                # No spans to process, return early
                if not finished:
                    return

                # Set partial flush tag on the first span
                if should_partial_flush:
                    log.debug("Partially flushing %d spans for trace %d", num_finished, span.trace_id)
                    finished[0].set_metric("_dd.py.partial_flush", num_finished)

                spans: Optional[List[Span]] = finished
                for tp in self._trace_processors:
                    try:
                        if spans is None:
                            return
                        spans = tp.process_trace(spans)
                    except Exception:
                        log.error("error applying processor %r", tp, exc_info=True)

                self._queue_span_count_metrics("spans_finished", "integration_name")
                self._writer.write(spans)
                return

            log.debug("trace %d has %d spans, %d finished", span.trace_id, len(trace.spans), trace.num_finished)
            return None

    def shutdown(self, timeout: Optional[float]) -> None:
        """
        This will stop the background writer/worker and flush any finished traces in the buffer. The tracer cannot be
        used for tracing after this method has been called. A new tracer instance is required to continue tracing.

        :param timeout: How long in seconds to wait for the background worker to flush traces
            before exiting or :obj:`None` to block until flushing has successfully completed (default: :obj:`None`)
        :type timeout: :obj:`int` | :obj:`float` | :obj:`None`
        """
        # on_span_start queue span created counts in batches of 100. This ensures all remaining counts are sent
        # before the tracer is shutdown.
        self._queue_span_count_metrics("spans_created", "integration_name", 1)
        # on_span_finish(...) queues span finish metrics in batches of 100.
        # This ensures all remaining counts are sent before the tracer is shutdown.
        self._queue_span_count_metrics("spans_finished", "integration_name", 1)
        # Log a warning if the tracer is shutdown before spans are finished
        unfinished_spans = [
            f"trace_id={s.trace_id} parent_id={s.parent_id} span_id={s.span_id} name={s.name} resource={s.resource} started={s.start} sampling_priority={s.context.sampling_priority}"  # noqa: E501
            for t in self._traces.values()
            for s in t.spans
            if not s.finished
        ]
        if unfinished_spans:
            log.warning(
                "Shutting down tracer with %d unfinished spans. " "Unfinished spans will not be sent to Datadog: %s",
                len(unfinished_spans),
                ", ".join(unfinished_spans),
            )

        try:
            self._writer.stop(timeout)
        except ServiceStatusError:
            # It's possible the writer never got started in the first place :(
            pass

    def _queue_span_count_metrics(self, metric_name: str, tag_name: str, min_count: int = 100) -> None:
        """Queues a telemetry count metric for span created and span finished"""
        # perf: telemetry_metrics_writer.add_count_metric(...) is an expensive operation.
        # We should avoid calling this method on every invocation of span finish and span start.
        if config._telemetry_enabled and sum(self._span_metrics[metric_name].values()) >= min_count:
            for tag_value, count in self._span_metrics[metric_name].items():
                telemetry.telemetry_writer.add_count_metric(
                    TELEMETRY_NAMESPACE_TAG_TRACER, metric_name, count, tags=((tag_name, tag_value),)
                )
            self._span_metrics[metric_name] = defaultdict(int)
