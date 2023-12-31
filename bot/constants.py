from pathlib import Path

DEFAULT_LIMIT_THROTTLING_MIDDLEWARE = 0.4
DEFAULT_KEY_THROTTLING_MIDDLEWARE = 'antiflood'

DEFAULT_LIMIT_SUBSCRIBE_MIDDLEWARE = 30.0
DEFAULT_KEY_SUBSCRIBE_MIDDLEWARE = 'sub'

DEFAULT_LATENCY_ALBUM_MIDDLEWARE = 0.8
DEFAULT_TTL_ALBUM_MIDDLEWARE = 1.0

REGEX_LINKS = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|www\.)+[a-zA-Z0-9\-.]+[a-zA-Z0-9\-_&=]'
LIMIT_ADS_ON_PAGE = 10
LIMIT_LENGTH_IN_CAPTION = 1024

PROJECT_ROOT = Path(__file__).resolve().parent
