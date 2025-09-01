@echo off
REM modules/kalku.bat

setlocal enabledelayedexpansion

set "line=%*"

set "result="
for /f "delims=" %%r in ('python helpers\kalku.py !line! 2^>nul') do (
    set "result=%%r"
)

for /f "tokens=1 delims==" %%a in ("!line!") do (
    set "var=%%a"
)

if not defined result (
    echo Terjadi kesalahan saat kalkulasi.
    endlocal & exit /b 1
)

REM simpan dulu nilai var dan result ke variabel sementara
set "varname=%var%"
set "resvalue=%result%"

endlocal & set "%varname%=%resvalue%"
