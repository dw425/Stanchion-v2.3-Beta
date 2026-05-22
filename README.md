# Stanchion — Beta v1.8 UAT

Public distribution point for the **Stanchion v1.8.0** UAT build (Crew Governance).
This repo contains **only the installer and the frozen install packages** — no source code.

> Stanchion is a local-first runtime governance daemon for coding agents:
> a live terminal/VS Code sidebar + insights hub across every model, platform, and tool,
> now with multi-agent **Crew Governance** (monitor, capture, intercept, and govern crews).

---

## Install

### macOS / Linux
```bash
curl -fsSL https://raw.githubusercontent.com/dw425/Beta_V1.8_UAT/main/install.sh | bash
```

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/dw425/Beta_V1.8_UAT/main/install.ps1 | iex
```

### Or run the universal installer directly
```bash
python3 install.py            # detects your OS/CPU, pulls the matching package
python3 install.py --keep     # download only, don't run the OS installer
```

The installer detects your platform and downloads the matching frozen build from this
repo's [latest release](../../releases/latest). No Python source, no pip, no compiler —
the package bundles its own runtime.

## After installing
```bash
stanchion install     # wire up agent hooks + the sidebar
stanchion start       # launch the daemon
stanchion monitor     # live terminal dashboard
```
Then open the Insights Hub at the URL `stanchion start` prints (default http://127.0.0.1:52737/insights).

## Platform availability (this UAT)
| Platform | Status |
|---|---|
| macOS — Apple Silicon (arm64) | ✅ available |
| macOS — Intel (x86_64) | ⏳ not yet published |
| Windows (x64) | ⏳ not yet published |
| Linux | source install only (private repo) |

## macOS: first-launch note (unsigned beta)
This UAT build is **not yet notarized**, so macOS Gatekeeper may warn on first launch.
The installer clears the quarantine flag automatically. If you ever download the `.pkg`
manually and Gatekeeper blocks it:
```bash
xattr -dr com.apple.quarantine ~/Downloads/Stanchion-1.8.0-macos-arm64.pkg
```
or right-click the `.pkg` → **Open**.

## What's new in v1.8.0 — Crew Governance
- **Crew section + Hierarchy** in the Insights Hub; sidebar **crew status box** (green/red) with a live build feed
- Capture of multi-agent crews across Claude Code sub-agents, CrewAI, AutoGen, and more — including the work farmed out and handoffs
- **Control**: kill switches, a crew-create gate, per-model spawn limits, a `stanchion crew` CLI
- **Governance**: per-framework specs + building specs (required roles / forbidden tools / caps), enforcement modes, YAML import/export

---
© 2026 Daniel Warren. All rights reserved. Use of this software is governed by its EULA.
