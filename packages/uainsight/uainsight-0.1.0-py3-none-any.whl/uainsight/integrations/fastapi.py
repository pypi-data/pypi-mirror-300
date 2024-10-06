try:
    from fastapi import Request
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.types import ASGIApp
except ImportError:
    raise ModuleNotFoundError(
        "FastAPI is not installed. Please install it using: `pip install fastapi`"
    )

from logging import getLogger
from typing import Optional

from uainsight.core import UserAgent, UserAgentParser

logger = getLogger(__name__)


class FastapiUserAgentMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, ua_header: str = "User-Agent", ua_key: str = "user_agent"
    ) -> None:
        super().__init__(app)
        self.ua_parser = UserAgentParser()
        self.ua_header = ua_header
        self.ua_key = ua_key

    async def dispatch(self, request: Request, call_next):
        ua_string = request.headers.get(self.ua_header)
        if ua_string:
            try:
                parsed_ua: Optional[UserAgent] = self.ua_parser.parse(ua_string)
                if parsed_ua:
                    request.state.__setattr__(self.ua_key, parsed_ua)
                else:
                    request.state.__setattr__(self.ua_key, None)
                    logger.warning(f"Failed to parse User-Agent: {ua_string}")
            except Exception as e:
                request.state.__setattr__(self.ua_key, None)
                logger.error(f"Error parsing User-Agent: {e}")
        else:
            request.state.__setattr__(self.ua_key, None)
        response = await call_next(request)
        return response
