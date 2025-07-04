@echo off
REM Quick Cities Search - Interactive Mode
REM Launch the all-cities search tool with interactive menus

echo.
echo ================================================================
echo              🇲🇦 QUICK MOROCCO CITIES SEARCH 🇲🇦
echo ================================================================
echo.
echo This tool helps you find business opportunities across Morocco:
echo.
echo ✅ All major cities supported (Marrakesh, Casablanca, Rabat, etc.)
echo ✅ Interactive city and search size selection
echo ✅ Automated result organization by city
echo ✅ Lead scoring and opportunity analysis
echo.
echo Loading interactive search...
echo.

cd /d "%~dp0"
python quick_all_cities_search.py --interactive

echo.
echo ================================================================
echo Search completed! Check results/cities/[city_name]/searches/
echo ================================================================
pause
