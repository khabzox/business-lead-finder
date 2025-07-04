@echo off
REM Quick Search Launcher - Points to quick_search folder
echo.
echo 🚀 Quick Search Launcher
echo.
echo Available commands:
echo.
echo 1. List cities:
echo    python quick_search/quick_all_cities_search.py --list-cities
echo.
echo 2. Search specific city:
echo    python quick_search/quick_all_cities_search.py --city [city_name] --search-size test
echo.
echo 3. Search all cities:
echo    python quick_search/quick_all_cities_search.py --all-cities --search-size test
echo.
echo 4. Interactive mode:
echo    python quick_search/quick_all_cities_search.py --interactive
echo.
echo Examples:
echo    python quick_search/quick_all_cities_search.py --city marrakesh --search-size test
echo    python quick_search/quick_all_cities_search.py --all-cities --search-size standard
echo.
pause
