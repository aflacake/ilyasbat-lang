@echo off
REM modules/kalku.bat

setlocal enabledelayedexpansion

set "line=%*"

set "line_no_space="
for %%x in (!line!) do (
    set "line_no_space=!line_no_space!%%x "
)

for /f "tokens=1,* delims==" %%a in ("!line_no_space!") do (
    set "var=%%a"
    set "expr=%%b"
)

if not defined expr (
    echo Format salah. Gunakan: variabel = ekspresi
    endlocal & exit /b 1
)

set "result="
for /f "delims=" %%r in ('python helpers\kalku.py !expr! 2^>nul') do (
    set "result=%%r"
)

if not defined result (
    echo Terjadi kesalahan saat kalkulasi.
    endlocal & exit /b 1
)

endlocal & set "%var%=%result%"
