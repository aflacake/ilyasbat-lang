@echo off
REM modules/menampilkan.bat

set var=%1
call set val=%%^%var%%%
if not defined val (
    echo [!%var%! tidak ditemukan]
) else (
    echo %val%
)
