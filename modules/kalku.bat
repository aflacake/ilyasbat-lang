@echo off
REM modules/kalku.bat

setlocal enabledelayedexpansion

set "line=%*"

REM Hapus "kalku " di depan supaya ambil expression yang benar
set "expr=!line:kalku =!"

set "result="
for /f "delims=" %%r in ('python helpers\kalku.py !expr! 2^>nul') do (
    set "result=%%r"
)

for /f "tokens=1 delims==" %%a in ("!expr!") do (
    set "var=%%a"
)

if not defined result (
    echo Terjadi kesalahan saat kalkulasi.
    endlocal & exit /b 1
)

set "varname=%var%"
set "resvalue=%result%"

(
    endlocal
    set "%varname%=%resvalue%"
)

echo [DEBUG] Set environment: %varname%=%resvalue%
