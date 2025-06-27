@echo off
echo Creating Pickish Distribution Package...
echo.

REM Create distribution folder
if exist "Pickish_Distribution" rmdir /s /q "Pickish_Distribution"
mkdir "Pickish_Distribution"

REM Copy executable
copy "dist\Pickish.exe" "Pickish_Distribution\"

REM Copy documentation
copy "DISTRIBUTION_README.md" "Pickish_Distribution\README.md"
copy "VERSION_HISTORY.md" "Pickish_Distribution\"

REM Copy batch file
copy "run_pickish.bat" "Pickish_Distribution\"

echo.
echo Distribution package created in 'Pickish_Distribution' folder!
echo.
echo Files included:
echo - Pickish.exe (main application)
echo - README.md (user guide)
echo - VERSION_HISTORY.md (version information)
echo - run_pickish.bat (easy launcher)
echo.
echo You can now zip the 'Pickish_Distribution' folder and share it!
echo.
pause 