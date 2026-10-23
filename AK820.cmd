@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
if "%~1"=="" if exist "%~dp0AK820.exe" goto standalone
if "%~1"=="" if exist "%~dp0AK820\AK820.exe" goto standalone_folder
if "%~1"=="" if exist "%~dp0dist\AK820\AK820.exe" goto standalone_dist
if not "%~1"=="" if exist "%~dp0AK820-cli\AK820-cli.exe" goto standalone_cli
if not "%~1"=="" if exist "%~dp0dist\AK820-cli\AK820-cli.exe" goto standalone_cli_dist
set "AK820_PYTHON=%~dp0.venv-ak820-installer\Scripts\python.exe"
if not exist "%AK820_PYTHON%" set "AK820_PYTHON=python"
"%AK820_PYTHON%" -B "%~dp0tools\installer\ak820.py" %*
set "AK820_STATUS=%ERRORLEVEL%"
if "%~1"=="" pause
exit /b %AK820_STATUS%

:standalone
start "" /wait "%~dp0AK820.exe"
set "AK820_STATUS=%ERRORLEVEL%"
if "%~1"=="" pause
exit /b %AK820_STATUS%

:standalone_dist
start "" /wait "%~dp0dist\AK820\AK820.exe"
set "AK820_STATUS=%ERRORLEVEL%"
if "%~1"=="" pause
exit /b %AK820_STATUS%

:standalone_folder
start "" /wait "%~dp0AK820\AK820.exe"
exit /b %ERRORLEVEL%

:standalone_cli
"%~dp0AK820-cli\AK820-cli.exe" %*
exit /b %ERRORLEVEL%

:standalone_cli_dist
"%~dp0dist\AK820-cli\AK820-cli.exe" %*
exit /b %ERRORLEVEL%
