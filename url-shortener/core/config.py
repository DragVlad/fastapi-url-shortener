import logging

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILEPATH = BASE_DIR / "short-urls.json"

LOG_LEVEL = logging.INFO

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

API_TOKENS: frozenset[str] = frozenset(
    {
        "QiGf4HQPlwDlSAcG0HJ4hg",
        "VAcHsSPUVKB3WV2FCzp2mg",
        "4Fds2MAbis2bvLj5-K0dcA",
    }
)

USERS_DB: dict[str, str] = {
    "admin": "admin",
    "bob": "margo",
}
