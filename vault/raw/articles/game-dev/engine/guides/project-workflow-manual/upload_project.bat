@echo off
chcp 65001 >nul
setlocal

REM ============================================
REM UrhoX Project Uploader
REM Usage: upload_project.bat <project_dir> [--dry-run]
REM ============================================

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "TOOLS_DIR=%SCRIPT_DIR%\..\..\tools\project-tools"
set "DEFAULT_HOST=publisher-alpha.spark.xd.com"

if "%~1"=="" (
    echo.
    echo ========================================
    echo   UrhoX Project Uploader
    echo ========================================
    echo.
    set /p "PROJECT_NAME=请输入项目目录: "
) else (
    set "PROJECT_NAME=%~1"
)

REM If absolute path, use as-is; otherwise look in SCRIPT_DIR
if "%PROJECT_NAME:~1,1%"==":" (
    set "PROJECT_DIR=%PROJECT_NAME%"
) else (
    set "PROJECT_DIR=%SCRIPT_DIR%\%PROJECT_NAME%"
)

REM Get project_id from project.json for test URL
for /f "usebackq tokens=*" %%i in (`python -c "import json; f=open(r'%PROJECT_DIR%\.project\project.json','r',encoding='utf-8'); d=json.load(f); print(d.get('project_id',''))"`) do set "PROJECT_ID=%%i"

echo.
echo ========================================
echo   Uploading: %PROJECT_DIR%
echo   Host: %DEFAULT_HOST%
echo ========================================
echo.

python "%TOOLS_DIR%\project_uploader.py" --project "%PROJECT_DIR%" --host %DEFAULT_HOST% --im_vip %2 %3 %4

if %ERRORLEVEL% EQU 0 (
    if not "%~2"=="--dry-run" (
        echo.
        echo ========================================
        echo   上传完成
        echo ========================================
        echo.
        echo 远端测试:
        echo   https://tapcode-sce.spark.xd.com/src/web/index.html?game_url=https://tapcode-sce.spark.xd.com/src/%PROJECT_ID%/
        echo.
    )
)

endlocal
pause
