@echo off
echo Building Pickish Executable...
echo.

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Build the executable
pyinstaller pickish.spec --clean

echo.
echo Build completed!
echo.
echo The executable is located in the 'dist' folder.
echo You can distribute the 'Pickish.exe' file to other computers.
echo.
pause 