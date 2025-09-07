@echo off
REM modules/melompat.bat

python helpers\melompat.py %*
exit /b %ERRORLEVEL%
