# PowerShell script to extract SSH private key for GitHub Secrets
# Usage: .\extract-ssh-key.ps1

$keyFile = "github_actions_vm"

if (-not (Test-Path $keyFile)) {
    Write-Host "Error: Key file '$keyFile' not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the directory containing your SSH key file" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n=== SSH Key Content for GitHub Secrets ===" -ForegroundColor Green
Write-Host "Copy everything below (including BEGIN and END lines):`n" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Cyan

Get-Content $keyFile

Write-Host "----------------------------------------`n" -ForegroundColor Cyan
Write-Host "Instructions:" -ForegroundColor Green
Write-Host "1. Select and copy ALL the text above (including BEGIN/END lines)" -ForegroundColor White
Write-Host "2. Go to GitHub → Repository → Settings → Secrets → Actions" -ForegroundColor White
Write-Host "3. Add/Update secret 'VPS_SSH_KEY' with the copied content" -ForegroundColor White
Write-Host "`nAlso verify these secrets are set:" -ForegroundColor Yellow
Write-Host "  - VPS_HOST: 4.145.116.160" -ForegroundColor White
Write-Host "  - VPS_USERNAME: github" -ForegroundColor White
Write-Host "  - VPS_PORT: 22 (or leave empty)" -ForegroundColor White

