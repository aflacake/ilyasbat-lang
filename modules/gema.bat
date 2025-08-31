@echo off
REM modules/gema.bat

shift

for /f "delims=" %%a in ('python helpers\gema.py %*') do set "output=%%a"
echo %output%
