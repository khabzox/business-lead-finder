@echo off
echo Setting up Business Lead Finder (BLF) command...

:: Get current directory
set "BLF_DIR=%~dp0"
set "BLF_DIR=%BLF_DIR:~0,-1%"

:: Check if already in PATH
echo %PATH% | find /i "%BLF_DIR%" >nul
if %errorlevel%==0 (
    echo BLF is already set up in your PATH!
    goto :end
)

:: Add to PATH for current session
set "PATH=%BLF_DIR%;%PATH%"

:: Add to permanent PATH (requires admin rights - optional)
echo.
echo Adding BLF directory to your PATH...
echo Directory: %BLF_DIR%
echo.
choice /C YN /M "Add to permanent PATH (requires restart)? "
if errorlevel 2 goto :session
if errorlevel 1 goto :permanent

:permanent
:: Add to system PATH permanently
setx PATH "%BLF_DIR%;%PATH%" >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Successfully added to permanent PATH!
    echo You can now run 'blf' from any directory after restart.
) else (
    echo ❌ Failed to add to permanent PATH. You may need admin rights.
    echo Using session PATH only.
)
goto :end

:session
echo ✅ Added to session PATH only.
echo You can run 'blf' in this command prompt session.

:end
echo.
echo 🚀 Business Lead Finder Setup Complete!
echo.
echo Usage examples:
echo   blf                          # Interactive mode
echo   blf restaurants marrakech    # Quick search
echo   blf cafes casablanca        # Find cafes
echo   blf demo                    # Run demo
echo.
pause
