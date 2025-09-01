@echo off
REM modules/menampilkan.bat

setlocal EnableDelayedExpansion

set var=%1

for /f "delims=" %%A in ('python helpers\menampilkan.py %var% 2^>nul') do (
    echo %%A
)
