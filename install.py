#!/usr/bin/env python3
###############################################################################
#  Stanchion — universal installer (stdlib-only).
#
#  Detects your OS + CPU, downloads the matching frozen Stanchion package from
#  the public Beta_V1.8_UAT GitHub release, and installs it. No source code,
#  no pip, no compiler — just a frozen, self-contained build.
#
#  Usage:
#     python3 install.py                  # install the default version
#     python3 install.py --version 1.8.0
#     python3 install.py --keep           # download only, don't run installer
#
#  Copyright (c) 2026 Daniel Warren. All rights reserved.
###############################################################################
from __future__ import annotations

import argparse
import platform
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

REPO = "dw425/Beta_V1.8_UAT"
DEFAULT_VERSION = "1.8.0"

# (system, machine) -> release asset name template. Machine values are
# normalized below so "arm64"/"aarch64" and "x86_64"/"AMD64" both resolve.
ASSETS: dict[tuple[str, str], str] = {
    ("Darwin", "arm64"): "Stanchion-{v}-macos-arm64.pkg",
    ("Darwin", "x86_64"): "Stanchion-{v}-macos-x64.pkg",
    ("Windows", "x86_64"): "Stanchion-{v}-windows-x64.exe",
}


def _norm_machine(m: str) -> str:
    m = m.lower()
    if m in ("arm64", "aarch64"):
        return "arm64"
    if m in ("x86_64", "amd64", "x64"):
        return "x86_64"
    return m


def _say(msg: str) -> None:
    print(f"  {msg}", flush=True)


def _download(url: str, dest: Path) -> None:
    _say(f"downloading {url}")
    # Prefer the system curl (handles corporate proxies + TLS well); fall back
    # to urllib so the installer still works where curl is absent.
    if shutil.which("curl"):
        subprocess.run(["curl", "-fSL", "-o", str(dest), url], check=True)
        return
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(url, context=ctx, timeout=60) as r, dest.open("wb") as f:
            shutil.copyfileobj(r, f)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"download failed (HTTP {exc.code}) — is the release published yet?") from exc


def _install_macos(pkg: Path) -> None:
    # The dev build is unsigned — clear the quarantine flag so the install
    # isn't blocked, then run the headless installer (needs admin).
    subprocess.run(["xattr", "-dr", "com.apple.quarantine", str(pkg)], check=False)
    _say("installing (you'll be prompted for your password) ...")
    subprocess.run(["sudo", "installer", "-pkg", str(pkg), "-target", "/"], check=True)


def _install_windows(exe: Path) -> None:
    _say("launching the Windows installer ...")
    # Inno Setup silent flags; drop them to show the GUI wizard instead.
    subprocess.run([str(exe), "/SILENT", "/NORESTART"], check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Universal Stanchion installer")
    ap.add_argument("--version", default=DEFAULT_VERSION)
    ap.add_argument("--keep", action="store_true",
                    help="download only; don't run the OS installer")
    args = ap.parse_args()

    system = platform.system()
    machine = _norm_machine(platform.machine())
    print(f"Stanchion installer — {system} / {machine} (v{args.version})")

    asset_tmpl = ASSETS.get((system, machine))
    if asset_tmpl is None:
        _say(f"No frozen build for {system}/{machine} yet.")
        if system == "Linux":
            _say("Linux isn't packaged — install from the private source repo "
                 "with `uv tool install` (ask the maintainer for access).")
        else:
            _say("This platform's installer hasn't been published to this UAT "
                 "release yet. Check back, or request it from the maintainer.")
        return 2

    asset = asset_tmpl.format(v=args.version)
    url = f"https://github.com/{REPO}/releases/download/v{args.version}/{asset}"

    tmp = Path(tempfile.mkdtemp(prefix="stanchion-"))
    dest = tmp / asset
    try:
        _download(url, dest)
    except subprocess.CalledProcessError:
        _say("download failed — is the release published and the asset name correct?")
        return 1
    _say(f"saved to {dest}")

    if args.keep:
        _say("--keep set; not running the installer. Run it yourself when ready.")
        return 0

    try:
        if system == "Darwin":
            _install_macos(dest)
        elif system == "Windows":
            _install_windows(dest)
    except subprocess.CalledProcessError as exc:
        _say(f"installer exited with an error: {exc}")
        return 1

    print("\nStanchion installed. Next:")
    print("  stanchion install     # wire up hooks + the sidebar")
    print("  stanchion start       # launch the daemon")
    print("  stanchion monitor     # open the live terminal dashboard")
    return 0


if __name__ == "__main__":
    sys.exit(main())
