import re
from typing import List, Pattern, Tuple


def compile_regexes(regex_list: List[Tuple[str, str]]) -> List[Tuple[str, Pattern]]:
    return [(name, re.compile(pattern, re.I)) for name, pattern in regex_list]


BROWSER_REGEXES = [
    ("Epiphany", r"Epiphany\/([\d\w\.]+)"),
    ("YaBrowser", r"YaBrowser\/([\d\w\.]+)"),
    ("Edge", r"(?:edge|edga|edgios|edg)\/([\d\w\.]+)"),
    ("Chrome", r"(?:chrome|crios)\/([\d\w\.]+)"),
    ("Chromium", r"chromium\/([\d\w\.]+)"),
    ("Firefox", r"(?:firefox|fxios)\/([\d\w\.]+)"),
    ("Opera", r"(?:opera|opr)\/([\d\w\.]+)"),
    ("UC", r"ucbrowser\/([\d\w\.]+)"),
    ("Facebook", r"FBAV\/([\d\w\.]+)"),
    ("Safari", r"Safari\/([\d\w\.]+)"),
    ("IE", r"msie\s([\d\.]+[\d])|trident\/\d+\.\d+;.*[rv:]+(\d+\.\d)"),
]

OS_REGEXES = [
    ("Windows 10", r"windows nt 10\.0"),
    ("Windows 8.1", r"windows nt 6\.3"),
    ("Windows 8", r"windows nt 6\.2"),
    ("Windows 7", r"windows nt 6\.1"),
    ("Windows", r"windows nt (\d+\.\d+)"),
    ("macOS", r"mac os x (\d+[._]\d+([._]\d+)?)"),
    ("iOS", r"ip[honead]+(?:.*os (\d+[._]\d+([._]\d+)?))"),
    ("Android", r"android (\d+(\.\d+)?)"),
    ("Linux", r"linux"),
]

DEVICE_REGEXES = [
    ("Mobile", r"mobile|ip[honead]+|android|blackberry|webos"),
    ("Tablet", r"tablet|ipad|playbook|silk"),
    ("Desktop", r"(windows|macintosh|linux)"),
]

CONSOLE_REGEXES = [
    ("PlayStation", r"playstation"),
    ("Xbox", r"xbox"),
    ("Nintendo", r"nintendo"),
]

BOT_REGEX = r"bot|crawler|spider|slurp"


def is_bot(user_agent_string: str) -> bool:
    return bool(re.search(BOT_REGEX, user_agent_string, re.I))
