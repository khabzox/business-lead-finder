#!/usr/bin/env powershell
# Quick All Cities Search - Search ALL Morocco cities at once

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "           🇲🇦 MASSIVE ALL MOROCCO CITIES SEARCH 🇲🇦" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will search ALL major Morocco cities:" -ForegroundColor Green
Write-Host ""
Write-Host "🏙️  Cities: Marrakesh, Casablanca, Rabat, Fez, Tangier," -ForegroundColor White
Write-Host "           Agadir, Meknes, Oujda, Tetouan, Essaouira" -ForegroundColor White
Write-Host ""
Write-Host "📊 Search Size: Standard (~50,000 businesses per city)" -ForegroundColor Yellow
Write-Host "⏱️  Estimated Time: 5-8 hours total" -ForegroundColor Yellow
Write-Host "📁 Results: Saved to results/cities/[city]/searches/" -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Do you want to start the massive all-cities search? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Search cancelled." -ForegroundColor Yellow
    Read-Host "Press Enter to continue"
    exit
}

Write-Host ""
Write-Host "🚀 Starting massive search of ALL Morocco cities..." -ForegroundColor Green
Write-Host "Please be patient, this will take several hours." -ForegroundColor Yellow
Write-Host ""

Set-Location $PSScriptRoot
python quick_all_cities_search.py --all-cities --search-size standard

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "ALL CITIES SEARCH COMPLETED!" -ForegroundColor Green
Write-Host "Check individual city results in: results/cities/[city_name]/" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Read-Host "Press Enter to continue"
