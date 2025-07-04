@echo off
echo ========================================
echo Google Maps CLI Integration Test
echo ========================================
echo.

echo Checking Google Maps scraping availability...
python test_google_maps_cli.py

echo.
echo ========================================
echo Quick Examples (run these manually):
echo ========================================
echo.
echo 1. Standard search:
echo python main.py search --location "Marrakesh, Morocco" --categories restaurants --filter no-website
echo.
echo 2. Google Maps enhanced search:
echo python main.py search --location "Marrakesh, Morocco" --categories hotels --use-google-maps --max-results 10
echo.
echo 3. Google Maps only (with emails):
echo python main.py search --location "Casablanca, Morocco" --categories spas --google-maps-only --max-results 5
echo.
echo 4. Combined search with AI:
echo python main.py search --location "Fez, Morocco" --categories restaurants --use-google-maps --ai-analysis
echo.
echo 5. Interactive mode:
echo python main.py interactive
echo.
echo 6. Check system status:
echo python main.py status
echo.

pause
