#!/usr/bin/env powershell
# Quick Cities Search - Interactive Mode PowerShell version

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "              🇲🇦 QUICK MOROCCO CITIES SEARCH 🇲🇦" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This tool helps you find business opportunities across Morocco:" -ForegroundColor Green
Write-Host ""
Write-Host "✅ All major cities supported (Marrakesh, Casablanca, Rabat, etc.)" -ForegroundColor Green
Write-Host "✅ Interactive city and search size selection" -ForegroundColor Green
Write-Host "✅ Automated result organization by city" -ForegroundColor Green
Write-Host "✅ Lead scoring and opportunity analysis" -ForegroundColor Green
Write-Host ""
Write-Host "Loading interactive search..." -ForegroundColor Yellow
Write-Host ""

Set-Location $PSScriptRoot
python quick_all_cities_search.py --interactive

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Search completed! Check results/cities/[city_name]/searches/" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Read-Host "Press Enter to continue"
