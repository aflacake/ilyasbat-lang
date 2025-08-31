@echo off
REM modules/kalku.bat

setlocal enabledelayedexpansion

set "line=%*"
for /f "tokens=1,2,3,4,5 delims= " %%a in ("%line%") do (
    set "var=%%a"
    set "equal=%%b"
    set "val1=%%c"
    set "op=%%d"
    set "val2=%%e"
)

if "!equal!" NEQ "=" (
    echo Format salah. Gunakan: var = nilai1 op nilai2
    endlocal & exit /b 1
)

set "result="
for /f "delims=" %%r in ('python helpers\kalku.py !val1! !op! !val2! 2^>nul') do (
    set "result=%%r"
)

if not defined result (
    echo Terjadi kesalahan saat menjalankan kalkulasi.
    endlocal & exit /b 1
)

endlocal & set "%var%=%result%"
