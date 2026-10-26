#!/usr/bin/env python3
"""Run the dependency-advisory gates used locally and in CI."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(label: str, command: tuple[str, ...], *, cwd: Path = ROOT) -> None:
    print(f"\n==> {label}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def _require_tools() -> None:
    required = ("uv", "cargo-audit", "npm", "bun")
    missing = [tool for tool in required if shutil.which(tool) is None]
    if missing:
        names = ", ".join(missing)
        raise RuntimeError(
            f"missing dependency-audit tools: {names}; "
            "install cargo-audit with `cargo install cargo-audit --locked`"
        )


def main() -> int:
    try:
        _require_tools()
        _run(
            "verify dependency lock inventory",
            (sys.executable, "scripts/verify_dependency_lock_inventory.py"),
        )
        _run(
            "sync root Python environment",
            ("uv", "sync", "--locked", "--all-extras", "--all-groups"),
        )
        _run(
            "audit root Python environment",
            (
                "uv",
                "run",
                "--no-sync",
                "--with",
                "pip-audit",
                "pip-audit",
                "--progress-spinner",
                "off",
            ),
        )
        _run(
            "sync documentation Python environment",
            ("uv", "sync", "--project", "docs/app", "--locked", "--group", "dev"),
        )
        _run(
            "audit documentation Python environment",
            (
                "uv",
                "run",
                "--project",
                "docs/app",
                "--no-sync",
                "--with",
                "pip-audit",
                "pip-audit",
                "--progress-spinner",
                "off",
            ),
        )
        _run(
            "audit benchmark Python lock",
            (
                "uvx",
                "--from",
                "pip-audit",
                "pip-audit",
                "-r",
                "benchmarks/requirements-ci.lock",
                "--progress-spinner",
                "off",
            ),
        )
        _run("audit root Rust lock", ("cargo", "audit"))
        _run(
            "audit osmium example Rust lock",
            ("cargo", "audit", "--file", "examples/osm/osmium-rs/Cargo.lock"),
        )
        _run(
            "audit npm lock",
            ("npm", "audit", "--package-lock-only", "--audit-level=high"),
        )
        bun_dir = ROOT / "docs" / "app" / "reflex.lock"
        _run("install frozen Bun lock", ("bun", "install", "--frozen-lockfile"), cwd=bun_dir)
        _run("audit Bun lock", ("bun", "audit", "--audit-level=high"), cwd=bun_dir)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"dependency audit failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
