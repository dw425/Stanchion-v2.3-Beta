# Stanchion v2.3 Beta — macOS

**Local-first runtime governance for your AI coding agents.** Stanchion meters and governs what every AI assistant and chat surface actually does — tokens, cost, models, tool calls — entirely on your Mac. Nothing leaves your machine.

This repo hosts the **signed & notarized installer downloads only** (no source).

---

## Requirements

- **Apple Silicon** Mac (M1/M2/M3/M4)
- **macOS 12 (Monterey) or newer**
- Admin password (the install sets up a global daemon + CLI)

---

## Download

➡️ **[Latest release](https://github.com/dw425/Stanchion-v2.3-Beta/releases/latest)**

| File | Use this if… |
|------|--------------|
| **Stanchion-Installer-2.3.0-arm64.dmg** | You want the guided, branded installer (recommended) |
| **Stanchion-2.3.0.pkg** | You want a plain double-click install (same result, no wizard) |

Both are signed with a Developer ID and notarized by Apple — Gatekeeper opens them without warnings.

---

## Install

**Visual installer (DMG):** open the `.dmg`, launch **Stanchion Installer**, and follow the wizard (Welcome → EULA → Personalize → Scan → Install). It asks for your admin password once to set up the global daemon, then wires the tools you already use.

**Package (.pkg):** double-click and follow the prompts.

### Verify the download (optional)
```sh
pkgutil --check-signature Stanchion-2.3.0.pkg
spctl -a -vvv --type install Stanchion-2.3.0.pkg   # expect: accepted / Notarized Developer ID
```

---

## What gets installed

- **Daemon** — local governance service on `http://127.0.0.1:52737`, auto-started via a LaunchAgent.
- **CLI** — `/usr/local/bin/stanchion`.
- **InsightsHub** — the full operator dashboard (served by the daemon).
- **Data** — everything lives under `~/.stanchion/` (database, config, token). 100% local.

### First run
Open the dashboard from your editor: **Cmd-Shift-P → "Stanchion: Open InsightsHub"** (VS Code / Cursor), or confirm the daemon is healthy with:
```sh
stanchion doctor
```

The beta ships with the **demo / lockdown** showcase enabled — you'll see **DEMO** and **LOCK** buttons on the InsightsHub header to seed sample data and demonstrate a live lockdown. (Demo seeding refuses to run if real data is present, so it can't clobber anything.)

---

## Enhancement packages — extend Stanchion's coverage

The installer auto-wires what it detects. Here's each integration and how to enable/configure it.

### 1. Editor extension — VS Code / Cursor / Windsurf
Installed automatically into any detected editor. To add it manually later:
```sh
code   --install-extension /usr/local/stanchion/stanchion-2.3.0.vsix --force
cursor --install-extension /usr/local/stanchion/stanchion-2.3.0.vsix --force
```
Gives you the live session sidebar + the **Open InsightsHub** command. If an editor was open during install, **fully quit and reopen it** (Cmd-Q) so the extension loads cleanly.

**Extension settings** (Settings → search "Stanchion"):
| Setting | Default | Purpose |
|---|---|---|
| `stanchion.daemonUrl` | `http://127.0.0.1:52737` | Where the daemon lives |
| `stanchion.token` | (auto) | Bearer token |
| `stanchion.contextWindow` | `auto` | Context-% gauge window (`auto` / `200k` / `1m`) |
| `stanchion.sidebarMode` | `native` | `native` live dashboard, or `unified` embedded SPA |
| `stanchion.captureThirdPartyAssistants` | `false` | Also meter Augment, Refact, Supermaven, Codeium, Qodo, IntelliCode, GitHub Models |

### 2. Terminal & shell
Shell hooks are wired during install so CLI agents (Claude Code, Codex, Gemini CLI, etc.) are metered automatically. Restart your terminal after install.

### 3. JetBrains / PyCharm
If a JetBrains IDE is detected, the plugin is dropped into its plugins folder — **restart the IDE** to activate. Otherwise search "Stanchion" in the IDE's Plugins marketplace.

### 4. 🌐 Browser web-capture extension (Chrome / Brave / Edge)
This is what lets Stanchion **govern the in-browser AI chats** — ChatGPT, Claude.ai, Gemini, and Copilot web.

Chrome doesn't allow installers to add unpacked extensions silently, so the installer **drops it on your Desktop** with a README. To load it (~30 seconds, one time):

1. Open **`chrome://extensions`** (Brave: `brave://extensions`, Edge: `edge://extensions`)
2. Turn on **Developer mode** (top-right toggle)
3. Click **Load unpacked**
4. Select the **`Stanchion Chrome Extension`** folder on your **Desktop**
5. You'll see **Stanchion** appear in your extensions — done.

Keep that folder where it is (the extension runs from it); move it anywhere permanent and just reload it from the new path.

---

## Controlling the web chats

Once the browser extension is loaded, you govern the web surface from **InsightsHub → Security → Models**, which has two independent, mirrored sections:

- **Web Interface Control** — governs the browser chats
- **IDE / CLI / Proxy Control** — governs editors & CLIs

For each model on each surface you can set **Allow / Deny**, **control toggles** (tool calls, file writes, network, agent/crew spawning), **token caps**, **cost caps**, and **external** (web access, data export).

**Live enforcement on the web:** deny a model under **Web Interface Control**, and the browser extension **blocks the send** on chatgpt.com / claude.ai / gemini.google.com. It's tier-aware — denying "Opus" blocks any Opus; "GPT-5.5" blocks just that model — and a banner explains the block. Allowed models send normally.

**Fleet control via YAML:** each surface has **Export / Import YAML** — ship one policy file to deny/allow models across many machines at once.

---

## CLI reference
```sh
stanchion doctor        # health check (run this first if anything's off)
stanchion status        # daemon status
stanchion start|stop|restart
stanchion repair        # auto-fix a stuck daemon / extension wiring
stanchion-diagnose      # detailed diagnostics bundle
```

## Troubleshooting
- **Dashboard/sidebar looks stale or blank** → fully quit and reopen the editor (Cmd-Q), then reopen InsightsHub.
- **Extension shows "invalid" / won't reinstall** → quit the editor completely first; it half-removes if quit while running.
- **Anything else** → `stanchion doctor`, then `stanchion repair`.

## Uninstall
```sh
sudo /usr/local/stanchion/uninstall.sh
```

---

## Privacy
Stanchion is **local-first**. The daemon runs only on loopback (`127.0.0.1`), all data stays in `~/.stanchion/`, and from the in-browser chats it records **metadata only** (model, token counts, timing) — never your prompts or the responses.

---
© 2026 Daniel Warren. All rights reserved. Confidential beta — do not redistribute.
