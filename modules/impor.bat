REM modules/impor.bat

@echo off

if "%~1"=="" (
    echo Kesalahan: Nama file modul tidak diberikan.
    exit /b 1
)

python helpers\impor.py "%~1"

set "errorcode=%ERRORLEVEL%"
exit /b %errorcode%
