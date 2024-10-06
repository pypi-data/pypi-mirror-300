try:
    from flask import Flask, request
except ImportError:
    raise ModuleNotFoundError(
        "Flask is not installed. Please install it using: `pip install flask`"
    )

from logging import getLogger
from typing import Optional

from uainsight.core import UserAgent, UserAgentParser

logger = getLogger(__name__)


class FlaskUserAgentMiddleware:
    def __init__(self, app: Flask):
        self.app = app
        self.ua_parser = UserAgentParser()
        self.ua_header = "User-Agent"
        self.ua_key = "user_agent"

        @app.before_request
        def parse_user_agent():
            ua_string = request.headers.get(self.ua_header)
            if ua_string:
                try:
                    parsed_ua: Optional[UserAgent] = self.ua_parser.parse(ua_string)
                    if parsed_ua:
                        setattr(request, self.ua_key, parsed_ua)
                    else:
                        logger.warning(f"Failed to parse User-Agent: {ua_string}")
                except Exception as e:
                    logger.error(f"Error parsing User-Agent: {e}")
