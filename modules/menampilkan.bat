@echo off
REM modules/menampilkan.bat

setlocal EnableDelayedExpansion

if exist ".env.bat" call ".env.bat"

set var=%1
python helpers\menampilkan.py !var!

endlocal
