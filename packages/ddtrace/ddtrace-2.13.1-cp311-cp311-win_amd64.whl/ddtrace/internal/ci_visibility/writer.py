from http.client import RemoteDisconnected
import os
import socket
from typing import TYPE_CHECKING  # noqa:F401
from typing import Optional  # noqa:F401

import ddtrace
from ddtrace import config
from ddtrace.internal.utils.time import StopWatch
from ddtrace.vendor.dogstatsd import DogStatsd  # noqa:F401

from .. import agent
from .. import service
from ..runtime import get_runtime_id
from ..writer import HTTPWriter
from ..writer import WriterClientBase
from .constants import AGENTLESS_BASE_URL
from .constants import AGENTLESS_COVERAGE_BASE_URL
from .constants import AGENTLESS_COVERAGE_ENDPOINT
from .constants import AGENTLESS_DEFAULT_SITE
from .constants import AGENTLESS_ENDPOINT
from .constants import EVP_PROXY_AGENT_ENDPOINT
from .constants import EVP_PROXY_COVERAGE_ENDPOINT
from .constants import EVP_SUBDOMAIN_HEADER_COVERAGE_VALUE
from .constants import EVP_SUBDOMAIN_HEADER_NAME
from .encoder import CIVisibilityCoverageEncoderV02
from .encoder import CIVisibilityEncoderV01
from .telemetry.payload import REQUEST_ERROR_TYPE
from .telemetry.payload import record_endpoint_payload_bytes
from .telemetry.payload import record_endpoint_payload_request
from .telemetry.payload import record_endpoint_payload_request_error
from .telemetry.payload import record_endpoint_payload_request_time


if TYPE_CHECKING:  # pragma: no cover
    from typing import Dict  # noqa:F401
    from typing import List  # noqa:F401

    from ddtrace.internal.utils.http import Response  # noqa:F401


class CIVisibilityEventClient(WriterClientBase):
    def __init__(self):
        encoder = CIVisibilityEncoderV01(0, 0)
        encoder.set_metadata(
            {
                "language": "python",
                "env": config.env,
                "runtime-id": get_runtime_id(),
                "library_version": ddtrace.__version__,
            }
        )
        super(CIVisibilityEventClient, self).__init__(encoder)


class CIVisibilityCoverageClient(WriterClientBase):
    def __init__(self, intake_url, headers=None, itr_suite_skipping_mode=False):
        encoder = CIVisibilityCoverageEncoderV02(0, 0)
        if itr_suite_skipping_mode:
            encoder._set_itr_suite_skipping_mode(itr_suite_skipping_mode)
        self._intake_url = intake_url
        if headers:
            self._headers = headers
        super(CIVisibilityCoverageClient, self).__init__(encoder)


class CIVisibilityProxiedCoverageClient(CIVisibilityCoverageClient):
    ENDPOINT = EVP_PROXY_COVERAGE_ENDPOINT


class CIVisibilityAgentlessCoverageClient(CIVisibilityCoverageClient):
    ENDPOINT = AGENTLESS_COVERAGE_ENDPOINT


class CIVisibilityAgentlessEventClient(CIVisibilityEventClient):
    ENDPOINT = AGENTLESS_ENDPOINT


class CIVisibilityProxiedEventClient(CIVisibilityEventClient):
    ENDPOINT = EVP_PROXY_AGENT_ENDPOINT


class CIVisibilityWriter(HTTPWriter):
    RETRY_ATTEMPTS = 5
    HTTP_METHOD = "POST"
    STATSD_NAMESPACE = "civisibility.writer"

    def __init__(
        self,
        intake_url="",  # type: str
        processing_interval=None,  # type: Optional[float]
        timeout=None,  # type: Optional[float]
        dogstatsd=None,  # type: Optional[DogStatsd]
        sync_mode=False,  # type: bool
        report_metrics=False,  # type: bool
        api_version=None,  # type: Optional[str]
        reuse_connections=None,  # type: Optional[bool]
        headers=None,  # type: Optional[Dict[str, str]]
        use_evp=False,  # type: bool
        coverage_enabled=False,  # type: bool
        itr_suite_skipping_mode=False,  # type: bool
    ):
        if processing_interval is None:
            processing_interval = config._trace_writer_interval_seconds
        if timeout is None:
            timeout = config._agent_timeout_seconds
        intake_cov_url = None
        if use_evp:
            intake_url = agent.get_trace_url()
            intake_cov_url = agent.get_trace_url()
        elif config._ci_visibility_agentless_url:
            intake_url = config._ci_visibility_agentless_url
            intake_cov_url = config._ci_visibility_agentless_url
        if not intake_url:
            intake_url = "%s.%s" % (AGENTLESS_BASE_URL, os.getenv("DD_SITE", AGENTLESS_DEFAULT_SITE))

        clients = (
            [CIVisibilityProxiedEventClient()] if use_evp else [CIVisibilityAgentlessEventClient()]
        )  # type: List[WriterClientBase]
        if coverage_enabled:
            if not intake_cov_url:
                intake_cov_url = "%s.%s" % (AGENTLESS_COVERAGE_BASE_URL, os.getenv("DD_SITE", AGENTLESS_DEFAULT_SITE))
            clients.append(
                CIVisibilityProxiedCoverageClient(
                    intake_url=intake_cov_url,
                    headers={EVP_SUBDOMAIN_HEADER_NAME: EVP_SUBDOMAIN_HEADER_COVERAGE_VALUE},
                    itr_suite_skipping_mode=itr_suite_skipping_mode,
                )
                if use_evp
                else CIVisibilityAgentlessCoverageClient(
                    intake_url=intake_cov_url, itr_suite_skipping_mode=itr_suite_skipping_mode
                )
            )

        super(CIVisibilityWriter, self).__init__(
            intake_url=intake_url,
            clients=clients,
            processing_interval=processing_interval,
            timeout=timeout,
            dogstatsd=dogstatsd,
            sync_mode=sync_mode,
            reuse_connections=reuse_connections,
            headers=headers,
        )

    def stop(self, timeout=None):
        if self.status != service.ServiceStatus.STOPPED:
            super(CIVisibilityWriter, self).stop(timeout=timeout)

    def recreate(self):
        # type: () -> HTTPWriter
        return self.__class__(
            intake_url=self.intake_url,
            processing_interval=self._interval,
            timeout=self._timeout,
            dogstatsd=self.dogstatsd,
            sync_mode=self._sync_mode,
        )

    def _put(self, data, headers, client, no_trace):
        # type: (bytes, Dict[str, str], WriterClientBase, bool) -> Response
        request_error = None  # type: Optional[REQUEST_ERROR_TYPE]

        with StopWatch() as sw:
            try:
                response = super()._put(data, headers, client, no_trace)
                if response.status >= 400:
                    request_error = REQUEST_ERROR_TYPE.STATUS_CODE
            except (TimeoutError, socket.timeout):
                request_error = REQUEST_ERROR_TYPE.TIMEOUT
                raise
            except RemoteDisconnected:
                request_error = REQUEST_ERROR_TYPE.NETWORK
                raise
            finally:
                if isinstance(client.encoder, CIVisibilityEncoderV01):
                    endpoint = client.encoder.ENDPOINT_TYPE
                    record_endpoint_payload_bytes(endpoint, nbytes=len(data))
                    record_endpoint_payload_request(endpoint)
                    record_endpoint_payload_request_time(endpoint, seconds=sw.elapsed())
                    if request_error:
                        record_endpoint_payload_request_error(endpoint, request_error)

        return response
