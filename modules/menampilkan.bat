@echo off
REM modules/menampilkan.bat

setlocal EnableDelayedExpansion

if exist ".env.bat" call ".env.bat"

set "args=%*"

python helpers\menampilkan.py "%args%"

endlocal

