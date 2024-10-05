import os

import requests
from wrapt import wrap_function_wrapper as _w

from ddtrace import config
from ddtrace.appsec._common_module_patches import wrapped_request_D8CB81E472AF98A2 as _wrap_request
from ddtrace.appsec._iast._metrics import _set_metric_iast_instrumented_sink
from ddtrace.appsec._iast.constants import VULN_SSRF
from ddtrace.contrib.trace_utils import unwrap as _u
from ddtrace.internal.schema import schematize_service_name
from ddtrace.internal.utils.formats import asbool
from ddtrace.pin import Pin
from ddtrace.settings.asm import config as asm_config

from .connection import _wrap_send


# requests default settings
config._add(
    "requests",
    {
        "distributed_tracing": asbool(os.getenv("DD_REQUESTS_DISTRIBUTED_TRACING", default=True)),
        "split_by_domain": asbool(os.getenv("DD_REQUESTS_SPLIT_BY_DOMAIN", default=False)),
        "default_http_tag_query_string": os.getenv("DD_HTTP_CLIENT_TAG_QUERY_STRING", "true"),
        "_default_service": schematize_service_name("requests"),
    },
)


def get_version():
    # type: () -> str
    return getattr(requests, "__version__", "")


def patch():
    """Activate http calls tracing"""
    if getattr(requests, "__datadog_patch", False):
        return
    requests.__datadog_patch = True

    _w("requests", "Session.send", _wrap_send)
    # IAST needs to wrap this function because `Session.send` is too late
    _w("requests", "Session.request", _wrap_request)
    Pin(_config=config.requests).onto(requests.Session)

    if asm_config._iast_enabled:
        _set_metric_iast_instrumented_sink(VULN_SSRF)


def unpatch():
    """Disable traced sessions"""
    if not getattr(requests, "__datadog_patch", False):
        return
    requests.__datadog_patch = False

    _u(requests.Session, "request")
    _u(requests.Session, "send")
