@echo off

if "%~1"=="" (
    echo Error: Nama file modul tidak diberikan.
    exit /b 1
)

call "%~1"
exit
