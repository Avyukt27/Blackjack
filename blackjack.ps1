param(
    [Parameter(Mandatory=$false)]
    [switch]$debugging = $false
)

Set-Location $PSScriptRoot

if ($debugging) {
    Write-Host "Starting program in Debug Mode"
    python.exe .\Blackjack.py -debug 1
} else {
    Write-Host "Starting program in Normal Mode"
    python.exe .\Blackjack.py
}