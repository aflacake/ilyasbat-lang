@echo off

shift

for /f "delims=" %%a in ('python helpers\gema.py %*') do set "output=%%a"
echo %output%
