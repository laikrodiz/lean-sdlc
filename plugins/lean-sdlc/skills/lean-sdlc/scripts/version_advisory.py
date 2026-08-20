#!/usr/bin/env python3
"""Report a newer Lean-SDLC release during a genuine startup."""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Any, Callable


REPOSITORY_TAGS_URL = "https://api.github.com/repos/laikrodiz/lean-sdlc/tags?per_page=100"
CACHE_SECONDS = 24 * 60 * 60
NETWORK_TIMEOUT_SECONDS = 2
MAX_RESPONSE_BYTES = 64 * 1024
CACHE_FILENAME = "version_advisory.json"
PLUGIN_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MANIFEST_VERSION_PATTERN = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z"
)
TAG_VERSION_PATTERN = re.compile(
    r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z"
)


def _manifest_version(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str):
        return None
    match = MANIFEST_VERSION_PATTERN.fullmatch(value)
    if match is None:
        return None
    try:
        return tuple(int(part) for part in match.groups())  # type: ignore[return-value]
    except ValueError:
        return None


def _tag_version(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str):
        return None
    match = TAG_VERSION_PATTERN.fullmatch(value)
    if match is None:
        return None
    try:
        return tuple(int(part) for part in match.groups())  # type: ignore[return-value]
    except ValueError:
        return None


def _version_text(value: tuple[int, int, int]) -> str:
    return ".".join(str(part) for part in value)


def _codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser()


def cache_path() -> Path:
    return _codex_home() / "state" / "lean-sdlc" / CACHE_FILENAME


def _read_manifest(path: Path) -> tuple[int, int, int] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    return _manifest_version(payload.get("version"))


def _read_cache(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    checked_at = payload.get("checked_at")
    latest = payload.get("latest")
    notified_for = payload.get("notified_for")
    if (
        isinstance(checked_at, bool)
        or not isinstance(checked_at, (int, float))
        or (latest is not None and _manifest_version(latest) is None)
        or (notified_for is not None and not isinstance(notified_for, str))
    ):
        return None
    return {
        "checked_at": checked_at,
        "latest": latest,
        "notified_for": notified_for,
    }


def _write_cache(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


def _fetch_tags(opener: Callable[..., Any] | None = None) -> list[tuple[int, int, int]] | None:
    request = urllib.request.Request(
        REPOSITORY_TAGS_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "lean-sdlc-version-advisory",
        },
    )
    try:
        response = (opener or urllib.request.urlopen)(
            request, timeout=NETWORK_TIMEOUT_SECONDS
        )
        try:
            status = getattr(response, "status", None)
            if status is None:
                getcode = getattr(response, "getcode", None)
                status = getcode() if getcode is not None else None
            if isinstance(status, int) and not 200 <= status < 300:
                return None
            body = response.read(MAX_RESPONSE_BYTES + 1)
        finally:
            close = getattr(response, "close", None)
            if close is not None:
                close()
    except Exception:
        return None
    if not isinstance(body, (bytes, bytearray, str)) or len(body) > MAX_RESPONSE_BYTES:
        return None
    try:
        payload = json.loads(body)
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    if not isinstance(payload, list):
        return None
    versions: set[tuple[int, int, int]] = set()
    for item in payload:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            return None
        parsed = _tag_version(item["name"])
        if parsed is not None:
            versions.add(parsed)
    return sorted(versions)


def _fresh(cache: dict[str, Any] | None, now: float) -> bool:
    if cache is None:
        return False
    age = now - cache["checked_at"]
    return 0 <= age < CACHE_SECONDS


def check_for_update(
    *,
    now: float | None = None,
    opener: Callable[..., Any] | None = None,
    manifest: Path = PLUGIN_MANIFEST,
    cache: Path | None = None,
) -> str | None:
    """Return one advisory, or None when startup should stay silent."""
    current = _read_manifest(manifest)
    if current is None:
        return None
    checked_at = time.time() if now is None else now
    path = cache or cache_path()
    saved = _read_cache(path)
    fresh = _fresh(saved, checked_at)
    if fresh:
        latest = _manifest_version(saved["latest"])
        notified_for = saved["notified_for"]
    else:
        versions = _fetch_tags(opener)
        if versions is None:
            failed = {"checked_at": checked_at, "latest": None, "notified_for": None}
            try:
                _write_cache(path, failed)
            except OSError:
                pass
            return None
        latest = max(versions) if versions else None
        saved = {
            "checked_at": checked_at,
            "latest": None if latest is None else _version_text(latest),
            "notified_for": None,
        }
        notified_for = None
    message = None
    if latest is not None and latest > current:
        notification_key = f"{_version_text(current)}:{_version_text(latest)}"
        if notified_for != notification_key:
            saved["notified_for"] = notification_key
            message = (
                f"Lean-SDLC v{_version_text(latest)} is available. "
                "Architect should propose an upgrade and review repo contract compatibility."
            )
    if not fresh or message is not None:
        try:
            _write_cache(path, saved)
        except OSError:
            pass
    return message


def main() -> int:
    try:
        event = json.load(sys.stdin)
        if (
            not isinstance(event, dict)
            or event.get("hook_event_name") != "SessionStart"
            or event.get("source") != "startup"
        ):
            return 0
        message = check_for_update()
        if message is not None:
            print(json.dumps({"systemMessage": message}))
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
