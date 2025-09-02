@echo off
REM modules/menampilkan.bat

setlocal EnableDelayedExpansion
if exist ".env.bat" call ".env.bat"

python helpers\menampilkan.py %*

endlocal
