@echo off
REM Quick All Cities Search - Search ALL Morocco cities at once
REM This will search all major cities with standard search size

echo.
echo ================================================================
echo           🇲🇦 MASSIVE ALL MOROCCO CITIES SEARCH 🇲🇦
echo ================================================================
echo.
echo This will search ALL major Morocco cities:
echo.
echo 🏙️  Cities: Marrakesh, Casablanca, Rabat, Fez, Tangier,
echo           Agadir, Meknes, Oujda, Tetouan, Essaouira
echo.
echo 📊 Search Size: Standard (~50,000 businesses per city)
echo ⏱️  Estimated Time: 5-8 hours total
echo 📁 Results: Saved to results/cities/[city]/searches/
echo.

set /p CONFIRM="Do you want to start the massive all-cities search? (y/N): "
if /i "%CONFIRM%" neq "y" (
    echo Search cancelled.
    pause
    exit /b
)

echo.
echo 🚀 Starting massive search of ALL Morocco cities...
echo Please be patient, this will take several hours.
echo.

cd /d "%~dp0"
python quick_all_cities_search.py --all-cities --search-size standard

echo.
echo ================================================================
echo ALL CITIES SEARCH COMPLETED!
echo Check individual city results in: results/cities/[city_name]/
echo ================================================================
pause
