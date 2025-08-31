@echo off
REM modules/ulangi.bat

setlocal enabledelayedexpansion

set "args="
for %%x in (%*) do (
    set "args=!args! %%x"
)

set "output="
for /f "delims=" %%r in ('python helpers\ulangi.py !args! 2^>nul') do (
    echo %%r
)

if errorlevel 1 (
    echo Terjadi kesalahan saat menjalankan ulangi.
    endlocal & exit /b 1
)

endlocal
