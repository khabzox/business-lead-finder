@echo off
echo 🚀 MASSIVE MARRAKESH BUSINESS SEARCH - Quick Start
echo.
echo This will find THOUSANDS of business opportunities in Marrakesh!
echo Results saved to results/ folder in JSON format
echo.

:menu
echo ================================================
echo Choose your search size:
echo.
echo 1. Quick Test        (1,000 businesses - 2 minutes)
echo 2. Standard Search   (50,000+ businesses - 1 hour)  
echo 3. MEGA Search       (200,000+ businesses - 4 hours)
echo 4. Setup Automation  (Weekly/Monthly searches)
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto test
if "%choice%"=="2" goto standard  
if "%choice%"=="3" goto mega
if "%choice%"=="4" goto schedule
if "%choice%"=="5" goto exit
echo Invalid choice. Please try again.
goto menu

:test
echo.
echo 🧪 Running Quick Test Search...
echo Expected: ~1,000 businesses in 2-5 minutes
python quick_marrakesh_search.py --test
goto done

:standard  
echo.
echo 📊 Running Standard Search...
echo Expected: ~50,000+ businesses in 30-60 minutes
python quick_marrakesh_search.py --standard
goto done

:mega
echo.
echo 🚀 Running MEGA Search...
echo Expected: ~200,000+ businesses in 2-4 hours
echo This is a MASSIVE search - make sure you have time!
set /p confirm="Continue with MEGA search? (y/n): "
if /i "%confirm%"=="y" (
    python quick_marrakesh_search.py --mega
) else (
    echo MEGA search cancelled.
    goto menu
)
goto done

:schedule
echo.
echo 🔄 Setting up Automated Searches...
python quick_marrakesh_search.py --schedule
echo.
echo To start the scheduler:
echo 1. pip install schedule  
echo 2. python simple_scheduler.py
goto menu

:done
echo.
echo ✅ Search completed! 
echo 📁 Check the 'results/' folder for your data
echo 💡 Look for businesses with 'opportunity_level': 'EXCELLENT'
echo.
pause
goto menu

:exit
echo.
echo Thanks for using Massive Marrakesh Business Search!
echo Your business opportunities await in the results/ folder 🚀
pause
