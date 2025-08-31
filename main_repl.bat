@echo off
REM main_repl.bat

setlocal enabledelayedexpansion
title IlyasBat Mode REPL

echo == IlyasBat Mode REPL ==
echo Ketik 'keluar' untuk mengakhiri sesi.

:REPL
set /p "line=> "

if /i "!line!"=="keluar" goto :SELESAI

echo !line! > .repl.ibat

call main.bat .repl.ibat

goto REPL

:SELESAI
del .repl.ibat >nul 2>&1
exit /b
