@echo off
REM Quick City-Specific Search
REM Search a specific city with custom parameters

echo.
echo ================================================================
echo           🏙️ QUICK CITY-SPECIFIC SEARCH 🏙️
echo ================================================================
echo.
echo Available cities:
echo   1. Marrakesh (Tourist capital)
echo   2. Casablanca (Economic hub)  
echo   3. Rabat (Political capital)
echo   4. Fez (Cultural center)
echo   5. Tangier (Northern gateway)
echo   6. Agadir (Beach resort)
echo   7. Meknes (Imperial city)
echo   8. Oujda (Eastern gateway)
echo   9. Tetouan (Cultural center)
echo  10. Essaouira (Coastal gem)
echo.

if "%1"=="" (
    echo Usage examples:
    echo   quick_city.bat marrakesh        ^(Standard search^)
    echo   quick_city.bat casablanca mega  ^(MEGA search^)
    echo   quick_city.bat rabat test       ^(Quick test^)
    echo.
    echo Available search sizes: test, standard, mega
    echo.
    pause
    exit /b
)

set CITY=%1
set SIZE=%2
if "%SIZE%"=="" set SIZE=standard

echo.
echo 🚀 Starting %SIZE% search for %CITY%...
echo.

cd /d "%~dp0"
python quick_all_cities_search.py --city %CITY% --search-size %SIZE%

echo.
echo ================================================================
echo Search completed! Check results/cities/%CITY%/searches/
echo ================================================================
pause
