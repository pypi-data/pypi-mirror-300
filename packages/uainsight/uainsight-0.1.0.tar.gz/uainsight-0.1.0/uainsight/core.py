from dataclasses import dataclass
from typing import Optional

from uainsight.utils import (
    BROWSER_REGEXES,
    CONSOLE_REGEXES,
    DEVICE_REGEXES,
    OS_REGEXES,
    compile_regexes,
    is_bot,
)


@dataclass
class Browser:
    name: str
    version: str
    family: str = ""


@dataclass
class OperatingSystem:
    name: str
    version: str
    edition: str = ""


@dataclass
class UserAgent:
    browser: Browser
    os: OperatingSystem
    device: str
    is_bot: bool
    is_mobile: bool
    is_tablet: bool
    is_desktop: bool
    is_touch_capable: bool
    is_pc: bool
    is_web_view: bool
    web_view_type: str
    is_smart_tv: bool
    is_console: bool
    console_type: str
    is_ereader: bool
    raw: str


class UserAgentParser:
    def __init__(self):
        self._browser_regexes = compile_regexes(BROWSER_REGEXES)
        self._os_regexes = compile_regexes(OS_REGEXES)
        self._device_regexes = compile_regexes(DEVICE_REGEXES)
        self._console_regexes = compile_regexes(CONSOLE_REGEXES)

    def parse(self, user_agent_string: str) -> Optional[UserAgent]:
        """
        Parse a User-Agent string and return a UserAgent object.

        Args:
            user_agent_string (str): The User-Agent string to parse

        Returns:
            UserAgent: An object containing parsed User-Agent information
        """
        try:
            user_agent_lower_string = user_agent_string.lower()
            device = self._get_device(user_agent_lower_string)
            is_mobile = device == "Mobile"
            is_tablet = device == "Tablet"
            is_desktop = device == "Desktop"
            is_smart_tv = device == "Smart TV"
            is_console, console_type = self._is_console(user_agent_string)
            is_ereader = device == "E-reader"
            is_web_view, web_view_type = self._is_web_view(user_agent_lower_string)

            return UserAgent(
                browser=self._get_browser(user_agent_string),
                os=self._get_os(user_agent_string),
                device=device,
                is_bot=is_bot(user_agent_string),
                is_mobile=is_mobile,
                is_tablet=is_tablet,
                is_desktop=is_desktop,
                is_touch_capable=self._is_touch_capable(user_agent_string),
                is_pc=is_desktop,
                is_web_view=is_web_view,
                web_view_type=web_view_type,
                is_smart_tv=is_smart_tv,
                is_console=is_console,
                console_type=console_type,
                is_ereader=is_ereader,
                raw=user_agent_string,
            )
        except Exception as e:
            print(f"Error parsing user agent string: {e}")
            return None

    def _get_browser(self, user_agent_string: str) -> Browser:
        for name, regex in self._browser_regexes:
            match = regex.search(user_agent_string)
            if match:
                version = match.group(1) if match.groups() else ""
                family = self._get_browser_family(name)
                return Browser(name=name, version=version, family=family)
        return Browser(name="Unknown", version="", family="")

    def _get_browser_family(self, browser_name: str) -> str:
        chromium_based = ["Chrome", "Chromium", "Edge", "Opera"]
        if browser_name in chromium_based:
            return "Chromium"
        return ""

    def _get_os(self, user_agent_string: str) -> OperatingSystem:
        for name, regex in self._os_regexes:
            match = regex.search(user_agent_string)
            if match:
                if name == "Windows":
                    version = match.group(1)
                    return OperatingSystem(
                        name=f"Windows {version}",
                        version=version,
                        edition=self._get_os_edition(
                            user_agent_string, f"Windows {version}"
                        ),
                    )
                version = match.group(1).replace("_", ".") if match.groups() else ""
                edition = self._get_os_edition(user_agent_string, name)
                return OperatingSystem(name=name, version=version, edition=edition)
        return OperatingSystem(name="Unknown", version="", edition="")

    def _get_os_edition(self, user_agent_string: str, os_name: str) -> str:
        if os_name == "Windows 10":
            if "Windows NT 10.0; Win64; x64" in user_agent_string:
                return "Pro 64-bit"
        return ""

    def _get_device(self, user_agent_lower_string: str) -> str:
        if self._is_smart_tv(user_agent_lower_string):
            return "Smart TV"
        elif self._is_ereader(user_agent_lower_string):
            return "E-reader"
        elif self._is_tablet(user_agent_lower_string):
            return "Tablet"
        elif self._is_mobile(user_agent_lower_string):
            return "Mobile"
        elif self._is_desktop(user_agent_lower_string):
            return "Desktop"
        elif self._is_console(user_agent_lower_string)[0]:
            return "Game Console"
        return "Unknown"

    def _is_mobile(self, user_agent_lower_string: str) -> bool:
        mobile_devices = ["mobile", "android", "iphone", "ipod", "webos", "blackberry"]
        return any(
            device in user_agent_lower_string for device in mobile_devices
        ) and not self._is_tablet(user_agent_lower_string)

    def _is_desktop(self, user_agent_lower_string: str) -> bool:
        desktop_os = ["windows nt", "macintosh", "x11"]
        return any(os in user_agent_lower_string for os in desktop_os) or (
            "linux" in user_agent_lower_string
            and "android" not in user_agent_lower_string
        )

    def _is_tablet(self, user_agent_lower_string: str) -> bool:
        tablet_devices = ["ipad", "tablet", "kindle", "playbook", "silk"]
        return any(device in user_agent_lower_string for device in tablet_devices)

    def _is_touch_capable(self, user_agent_string: str) -> bool:
        return "Touch" in user_agent_string

    def _is_web_view(self, user_agent_lower_string: str) -> tuple[bool, str]:
        web_view_indicators = [
            ("wv", "WebView"),
            ("fban", "Facebook"),
            ("fbav", "Facebook"),
            ("instagram", "Instagram"),
        ]
        for indicator, view_type in web_view_indicators:
            if indicator in user_agent_lower_string:
                return True, view_type
        return False, ""

    def _is_smart_tv(self, user_agent_lower_string: str) -> bool:
        smart_tv_indicators = [
            "smart-tv",
            "smarttv",
            "googletv",
            "appletv",
            "hbbtv",
            "pov_tv",
            "netcast.tv",
            "tizen",
        ]
        return any(
            indicator in user_agent_lower_string for indicator in smart_tv_indicators
        )

    def _is_console(self, user_agent_string: str) -> tuple[bool, str]:
        for name, regex in self._console_regexes:
            if regex.search(user_agent_string):
                return True, name
        return False, ""

    def _is_ereader(self, user_agent_lower_string: str) -> bool:
        ereader_indicators = ["kindle", "nook", "kobo"]
        return any(
            indicator in user_agent_lower_string for indicator in ereader_indicators
        )


def parse_user_agent(user_agent_string: str) -> Optional[UserAgent]:
    """
    Parse a User-Agent string and return a UserAgent object.

    This is a convenience function that creates a UserAgentParser instance
    and calls its parse method.

    Args:
        user_agent_string (str): The User-Agent string to parse

    Returns:
        UserAgent: An object containing parsed User-Agent information
    """
    return UserAgentParser().parse(user_agent_string)
