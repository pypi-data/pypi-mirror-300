try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    raise ModuleNotFoundError(
        "Django is not installed. Please install it using: `pip install django`"
    )

from logging import getLogger
from typing import Optional

from uainsight.core import UserAgent, UserAgentParser

logger = getLogger(__name__)


class DjangoUserAgentMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.ua_parser = UserAgentParser()
        self.ua_header = "HTTP_USER_AGENT"
        self.ua_key = "user_agent"

    def process_request(self, request):
        ua_string = request.META.get(self.ua_header)
        if ua_string:
            try:
                parsed_ua: Optional[UserAgent] = self.ua_parser.parse(ua_string)
                if parsed_ua:
                    setattr(request, self.ua_key, parsed_ua)
                else:
                    logger.warning(f"Failed to parse User-Agent: {ua_string}")
            except Exception as e:
                logger.error(f"Error parsing User-Agent: {e}")
        return None
