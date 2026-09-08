#!/usr/bin/env python3
"""Check AndroidEasyRules versions without modifying the target project."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator


VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
PROJECT_VERSION_RE = re.compile(
    r"<!--\s*ANDROID_EASY_RULES_VERSION:\s*([^\s]+)\s*-->"
)
REMOTE_VERSION_URL = (
    "https://raw.githubusercontent.com/ahiwey/AndroidEasyRules/main/"
    "plugins/android-easy-rules/skills/android-easy-rules/assets/rules-pack/VERSION"
)
REMOTE_TTL_SECONDS = 7 * 24 * 60 * 60
REMOTE_TIMEOUT_SECONDS = 2
LOCK_WAIT_SECONDS = 0.25
LOCK_STALE_SECONDS = 30


def parse_version(value: str) -> tuple[int, int, int]:
    match = VERSION_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Invalid rules version: {value!r}")
    return tuple(int(part) for part in match.groups())


def read_version(path: Path) -> str:
    value = path.read_text(encoding="utf-8").strip()
    parse_version(value)
    return value


def default_local_version_file() -> Path:
    installed = Path(__file__).resolve().parent / "VERSION"
    if installed.is_file():
        return installed
    return Path(__file__).resolve().parents[1] / "assets" / "rules-pack" / "VERSION"


def read_project_version(project_root: Path) -> tuple[str | None, str | None]:
    agents = project_root / "AGENTS.md"
    if not agents.is_file():
        return None, None
    match = PROJECT_VERSION_RE.search(agents.read_text(encoding="utf-8"))
    if not match:
        return None, None
    value = match.group(1)
    try:
        parse_version(value)
    except ValueError:
        return None, value
    return value, None


def project_key(project_root: Path) -> str:
    normalized = os.path.normcase(str(project_root.resolve()))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def fetch_remote_version() -> str:
    request = urllib.request.Request(
        REMOTE_VERSION_URL,
        headers={"User-Agent": "AndroidEasyRules-version-checker"},
    )
    with urllib.request.urlopen(request, timeout=REMOTE_TIMEOUT_SECONDS) as response:
        value = response.read(64).decode("utf-8").strip()
    parse_version(value)
    return value


def load_state(path: Path) -> dict:
    if not path.is_file():
        return {"remote": {}, "projects": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"remote": {}, "projects": {}}
    if not isinstance(state, dict):
        return {"remote": {}, "projects": {}}
    if not isinstance(state.get("remote"), dict):
        state["remote"] = {}
    if not isinstance(state.get("projects"), dict):
        state["projects"] = {}
    return state


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)


@contextmanager
def state_lock(lock_path: Path) -> Iterator[bool]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + LOCK_WAIT_SECONDS
    acquired = False
    while time.monotonic() <= deadline:
        try:
            descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                stale = time.time() - lock_path.stat().st_mtime > LOCK_STALE_SECONDS
            except FileNotFoundError:
                continue
            if stale:
                try:
                    lock_path.unlink()
                except FileNotFoundError:
                    pass
                continue
            time.sleep(0.025)
            continue
        else:
            os.close(descriptor)
            acquired = True
            break
    try:
        yield acquired
    finally:
        if acquired:
            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass


def latest_known_version(
    state: dict,
    local_version_file: Path,
    remote_fetcher: Callable[[], str],
    now: float,
) -> tuple[str | None, str]:
    candidates: list[tuple[str, str]] = []
    try:
        candidates.append((read_version(local_version_file), "local"))
    except (OSError, ValueError):
        pass

    remote = state["remote"]
    checked_at = remote.get("checked_at")
    should_check = not isinstance(checked_at, (int, float)) or now - checked_at >= REMOTE_TTL_SECONDS
    if should_check:
        remote["checked_at"] = now
        try:
            remote["version"] = remote_fetcher()
        except (OSError, UnicodeError, ValueError):
            pass

    cached_remote = remote.get("version")
    if isinstance(cached_remote, str):
        try:
            parse_version(cached_remote)
        except ValueError:
            remote.pop("version", None)
        else:
            candidates.append((cached_remote, "remote-cache"))

    if not candidates:
        return None, "unknown"
    version, source = max(candidates, key=lambda item: parse_version(item[0]))
    return version, source


def check_project(
    project_root: Path,
    *,
    state_dir: Path | None = None,
    local_version_file: Path | None = None,
    remote_fetcher: Callable[[], str] = fetch_remote_version,
    now: float | None = None,
) -> dict:
    resolved_state_dir = state_dir or Path.home() / ".android-easy-rules"
    state_path = resolved_state_dir / "state.json"
    timestamp = time.time() if now is None else now
    with state_lock(resolved_state_dir / "state.lock") as acquired:
        if not acquired:
            return {"status": "suppressed", "reason": "checker_busy"}

        state = load_state(state_path)
        latest, source = latest_known_version(
            state,
            local_version_file or default_local_version_file(),
            remote_fetcher,
            timestamp,
        )
        current, invalid = read_project_version(project_root)
        if invalid is not None:
            save_state(state_path, state)
            return {
                "status": "unknown",
                "reason": "invalid_project_version",
                "current": invalid,
                "latest": latest,
            }
        if latest is None:
            save_state(state_path, state)
            return {
                "status": "unknown",
                "reason": "latest_version_unavailable",
                "current": current or "legacy",
            }

        key = project_key(project_root)
        projects = state["projects"]
        project_state = projects.setdefault(key, {})
        result = {
            "current": current or "legacy",
            "latest": latest,
            "source": source,
        }
        if current is not None and parse_version(current) >= parse_version(latest):
            projects.pop(key, None)
            result["status"] = "current"
        elif project_state.get("ignored_version") == latest:
            result.update(status="suppressed", reason="ignored_version")
        else:
            snooze_until = project_state.get("snooze_until")
            if isinstance(snooze_until, (int, float)) and snooze_until > timestamp:
                result.update(status="suppressed", reason="snoozed", snooze_until=snooze_until)
            elif project_state.get("last_notified_version") == latest and not isinstance(
                snooze_until, (int, float)
            ):
                result.update(status="suppressed", reason="already_notified")
            else:
                project_state.pop("snooze_until", None)
                project_state["last_notified_version"] = latest
                result["status"] = "notify"

        save_state(state_path, state)
        return result


def update_preference(
    project_root: Path,
    *,
    action: str,
    version: str | None = None,
    days: int = 7,
    state_dir: Path | None = None,
    now: float | None = None,
) -> dict:
    resolved_state_dir = state_dir or Path.home() / ".android-easy-rules"
    state_path = resolved_state_dir / "state.json"
    timestamp = time.time() if now is None else now
    with state_lock(resolved_state_dir / "state.lock") as acquired:
        if not acquired:
            return {"status": "suppressed", "reason": "checker_busy"}
        state = load_state(state_path)
        project_state = state["projects"].setdefault(project_key(project_root), {})
        if action == "snooze":
            if days < 1:
                raise ValueError("Snooze days must be at least 1")
            project_state["snooze_until"] = timestamp + days * 24 * 60 * 60
            result = {"status": "suppressed", "reason": "snoozed", "days": days}
        elif action == "ignore":
            if version is None:
                raise ValueError("Ignore requires a version")
            parse_version(version)
            project_state["ignored_version"] = version
            project_state.pop("snooze_until", None)
            result = {"status": "suppressed", "reason": "ignored_version", "version": version}
        else:
            raise ValueError(f"Unsupported action: {action}")
        save_state(state_path, state)
        return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check_parser = subparsers.add_parser("check", help="Check one project's rules version.")
    check_parser.add_argument("project_root", type=Path)
    snooze_parser = subparsers.add_parser("snooze", help="Remind again after a delay.")
    snooze_parser.add_argument("project_root", type=Path)
    snooze_parser.add_argument("--days", type=int, default=7)
    ignore_parser = subparsers.add_parser("ignore", help="Ignore one available rules version.")
    ignore_parser.add_argument("project_root", type=Path)
    ignore_parser.add_argument("--version", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "check":
            result = check_project(args.project_root.resolve())
        elif args.command == "snooze":
            result = update_preference(
                args.project_root.resolve(), action="snooze", days=args.days
            )
        else:
            result = update_preference(
                args.project_root.resolve(), action="ignore", version=args.version
            )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
