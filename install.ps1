# Stanchion universal installer (Windows). Fetches install.py and runs it.
#   irm https://raw.githubusercontent.com/dw425/Beta_V1.8_UAT/main/install.ps1 | iex
$ErrorActionPreference = "Stop"
$tmp = Join-Path $env:TEMP "stanchion-install.py"
$url = "https://raw.githubusercontent.com/dw425/Beta_V1.8_UAT/main/install.py"
Invoke-WebRequest -Uri $url -OutFile $tmp -UseBasicParsing
$py = (Get-Command python -ErrorAction SilentlyContinue) ?? (Get-Command python3 -ErrorAction SilentlyContinue)
if (-not $py) { Write-Error "Python 3 is required to run the installer."; exit 1 }
& $py.Source $tmp @args
