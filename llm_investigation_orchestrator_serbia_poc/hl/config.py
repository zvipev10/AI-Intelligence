"""Runtime configuration. Everything comes from environment variables; nothing is a secret."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, "") or default)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    port: int
    host: str
    hl_api_url: str
    hl_api_public_origin: str
    scenario: str
    type_prefix: str
    mapping_path: Path
    snapshot_ttl_seconds: int
    snapshot_max_rows: int
    cookie_secure: bool
    request_timeout_seconds: int
    build: str
    # An existing i360 type to use as the investigation list (e.g. INTELLIGENCE_INVESTIGATION).
    # Empty: the app's own <prefix>INVESTIGATION records.
    external_investigation_type: str = ""
    # Items read per profile query (one query per item type); 0 keeps each query's own "limit".
    items_per_type: int = 0
    # The i360 chat service (analytics/i360-chat, http://i360-chat:4020 on LAMBDA). Empty: the chat is off.
    chat_service_url: str = ""
    # Model id the i360 chat is asked to use; empty keeps the service's own default.
    chat_model: str = ""
    # The app's own small assistant over HL API /llm/chat. Empty model: the first of GET /llm/models.
    llm_enabled: bool = True
    llm_model: str = ""
    chat_idle_timeout_seconds: int = 300

    @property
    def investigation_type(self) -> str:
        return f"{self.type_prefix}INVESTIGATION"

    @property
    def memory_item_type(self) -> str:
        return f"{self.type_prefix}MEMORY_ITEM"

    @property
    def approval_type(self) -> str:
        return f"{self.type_prefix}TELECOM_APPROVAL"


def load_settings() -> Settings:
    hl_api_url = os.environ.get("HL_API_URL", "").rstrip("/")
    return Settings(
        port=_int("PORT", 8080),
        host=os.environ.get("APP_HOST", "0.0.0.0"),
        hl_api_url=hl_api_url,
        hl_api_public_origin=os.environ.get("HL_API_PUBLIC_ORIGIN", "").rstrip("/") or hl_api_url,
        scenario=os.environ.get("APP_SCENARIO", "syria").strip().lower() or "syria",
        type_prefix=os.environ.get("APP_TYPE_PREFIX", "AII_"),
        mapping_path=Path(os.environ.get("APP_MAPPING", str(ROOT / "mapping" / "default.json"))),
        snapshot_ttl_seconds=_int("APP_SNAPSHOT_TTL", 300),
        snapshot_max_rows=_int("APP_SNAPSHOT_MAX_ROWS", 30000),
        cookie_secure=_bool("APP_COOKIE_SECURE", True),
        request_timeout_seconds=_int("HL_API_TIMEOUT", 30),
        build=os.environ.get("APP_BUILD", "dev"),
        external_investigation_type=os.environ.get("APP_INVESTIGATION_TYPE", "").strip(),
        items_per_type=_int("APP_ITEMS_PER_TYPE", 0),
        chat_service_url=os.environ.get("CHAT_SERVICE_URL", "").strip().rstrip("/"),
        chat_model=os.environ.get("CHAT_MODEL", "").strip(),
        llm_enabled=_bool("APP_CHAT_ASSISTANT", True),
        llm_model=os.environ.get("APP_CHAT_ASSISTANT_MODEL", "").strip(),
        chat_idle_timeout_seconds=_int("CHAT_IDLE_TIMEOUT", 300),
    )
