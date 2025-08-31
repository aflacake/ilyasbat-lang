@echo off
REM modules/jika.bat

python helpers\jika.py %*
exit /b %ERRORLEVEL%
