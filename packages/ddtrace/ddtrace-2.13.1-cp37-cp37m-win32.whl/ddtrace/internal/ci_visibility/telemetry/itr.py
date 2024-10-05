from enum import Enum
import functools
from typing import Optional

from ddtrace.internal.ci_visibility.constants import SUITE
from ddtrace.internal.ci_visibility.telemetry.constants import CIVISIBILITY_TELEMETRY_NAMESPACE as _NAMESPACE
from ddtrace.internal.ci_visibility.telemetry.constants import ERROR_TYPES
from ddtrace.internal.ci_visibility.telemetry.constants import EVENT_TYPES
from ddtrace.internal.logger import get_logger
from ddtrace.internal.telemetry import telemetry_writer


log = get_logger(__name__)


class ITR_TELEMETRY(str, Enum):
    SKIPPED = "itr_skipped"
    UNSKIPPABLE = "itr_unskippable"
    FORCED_RUN = "itr_forced_run"


class SKIPPABLE_TESTS_TELEMETRY(str, Enum):
    REQUEST = "itr_skippable_tests.request"
    REQUEST_MS = "itr_skippable_tests.request_ms"
    REQUEST_ERRORS = "itr_skippable_tests.request_errors"
    RESPONSE_BYTES = "itr_skippable_tests.response_bytes"
    RESPONSE_TESTS = "itr_skippable_tests.response_tests"
    RESPONSE_SUITES = "itr_skippable_tests.response_suites"


def _enforce_event_is_test_or_suite(func):
    @functools.wraps(func)
    def wrapper(event_type: str):
        if event_type not in [EVENT_TYPES.SUITE, EVENT_TYPES.TEST]:
            log.debug("%s can only be used for suites or tests, not %s", func.__name__, event_type)
            return
        return func(event_type)

    return wrapper


@_enforce_event_is_test_or_suite
def record_itr_skipped(event_type: EVENT_TYPES):
    log.debug("Recording itr skipped telemetry for %s", event_type)
    telemetry_writer.add_count_metric(_NAMESPACE, ITR_TELEMETRY.SKIPPED, 1, (("event_type", event_type.value),))


@_enforce_event_is_test_or_suite
def record_itr_unskippable(event_type: EVENT_TYPES):
    log.debug("Recording itr unskippable telemetry for %s", event_type)
    telemetry_writer.add_count_metric(_NAMESPACE, ITR_TELEMETRY.UNSKIPPABLE, 1, (("event_type", event_type.value),))


def record_itr_forced_run(event_type: EVENT_TYPES):
    log.debug("Recording itr forced run telemetry for %s", event_type)
    telemetry_writer.add_count_metric(_NAMESPACE, ITR_TELEMETRY.FORCED_RUN, 1, (("event_type", event_type.value),))


def record_itr_skippable_request(
    duration: float,
    response_bytes: int,
    skipping_level: str,
    skippable_count: Optional[int] = None,
    error: Optional[ERROR_TYPES] = None,
):
    log.debug(
        "Recording itr skippable request telemetry: %s, %s, %s, %s, %s",
        duration,
        response_bytes,
        skippable_count,
        skipping_level,
        error,
    )

    telemetry_writer.add_count_metric(_NAMESPACE, SKIPPABLE_TESTS_TELEMETRY.REQUEST, 1)
    telemetry_writer.add_distribution_metric(_NAMESPACE, SKIPPABLE_TESTS_TELEMETRY.REQUEST_MS, duration)
    telemetry_writer.add_distribution_metric(_NAMESPACE, SKIPPABLE_TESTS_TELEMETRY.RESPONSE_BYTES, response_bytes)

    if error is not None:
        telemetry_writer.add_count_metric(
            _NAMESPACE, SKIPPABLE_TESTS_TELEMETRY.REQUEST_ERRORS, 1, (("error_type", error),)
        )
        # If there was an error, assume no skippable items can be counted
        return

    if skippable_count is not None:
        skippable_count_metric = (
            SKIPPABLE_TESTS_TELEMETRY.RESPONSE_SUITES
            if skipping_level == SUITE
            else SKIPPABLE_TESTS_TELEMETRY.RESPONSE_TESTS
        )
        telemetry_writer.add_count_metric(_NAMESPACE, skippable_count_metric, skippable_count)
