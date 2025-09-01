@echo off
REM modules/kalku.bat

setlocal enabledelayedexpansion

REM Tangkap seluruh argumen sebagai ekspresi
set "expr=%*"

REM Pisahkan nama variabel dan ekspresi
for /f "tokens=1,* delims==" %%a in ("!expr!") do (
    set "varname=%%a"
    set "raw_expr=%%b"
)

set "result="
for /f "delims=" %%r in ('python helpers\kalku.py !varname! = !raw_expr! 2^>nul') do (
    set "result=%%r"
)

if not defined result (
    echo Terjadi kesalahan saat kalkulasi.
    endlocal & exit /b 1
)

(
    endlocal
    set "%varname%=%result%"
)

echo [DEBUG] Set environment: %varname%=%result%
