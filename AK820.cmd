@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
set "AK820_PYTHON=%~dp0.venv-ak820-installer\Scripts\python.exe"
if not exist "%AK820_PYTHON%" set "AK820_PYTHON=python"
"%AK820_PYTHON%" -B "%~dp0tools\installer\ak820.py" %*
set "AK820_STATUS=%ERRORLEVEL%"
if "%~1"=="" pause
exit /b %AK820_STATUS%
