# Stanchion v2.3 Beta — macOS Installer

Signed & notarized macOS installer for **Stanchion v2.3.0**. No source — downloads only.

## Download

➡️ **[Download the latest installer](https://github.com/dw425/Stanchion-v2.3-Beta/releases/latest)**

Direct link:
```
https://github.com/dw425/Stanchion-v2.3-Beta/releases/download/v2.3.0/Stanchion-2.3.0-signed.pkg
```

## Install

Double-click the `.pkg` and follow the prompts. It is signed with a Developer ID
and notarized by Apple, so macOS Gatekeeper will open it without warnings.

## Verify (optional)

```sh
shasum -a 256 Stanchion-2.3.0-signed.pkg
# 9938dc64ecca9703321fbf7350ae4700f28bdd340144c9e43bd437c4c55ba2e2

pkgutil --check-signature Stanchion-2.3.0-signed.pkg
spctl -a -vvv --type install Stanchion-2.3.0-signed.pkg   # expect: accepted / Notarized Developer ID
```

---
© 2026 Daniel Warren. All rights reserved.
