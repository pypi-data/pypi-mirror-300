# uainsight

uainsight is a Python package for parsing and analyzing User-Agent strings. It provides easy integration with FastAPI, Django, and Flask.

## Features

- Parse User-Agent strings
- Extract browser, operating system, and device information
- Bot detection
- Easy integration with FastAPI, Django, and Flask frameworks

## Installation

Using Poetry (recommended):

```bash
poetry add uainsight
```

Using pip:

```bash
pip install uainsight
```

## Quick Start

```python
from uainsight import parse_user_agent

ua_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
ua = parse_user_agent(ua_string)

print(f"Browser: {ua.browser.name} {ua.browser.version}")
print(f"OS: {ua.os.name} {ua.os.version}")
print(f"Device: {ua.device}")
```

## Documentation

For full documentation, visit [https://joongi007.github.io/uainsight/](https://joongi007.github.io/uainsight/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.