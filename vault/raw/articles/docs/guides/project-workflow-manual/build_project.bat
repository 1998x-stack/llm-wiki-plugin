@echo off
chcp 65001 >nul
setlocal

REM ============================================
REM UrhoX Project Builder
REM Usage: build_project.bat <project_dir> [--debug]
REM ============================================

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "TOOLS_DIR=%SCRIPT_DIR%\..\..\tools\project-tools"

if "%~1"=="" (
    echo.
    echo ========================================
    echo   UrhoX Project Builder
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

echo.
echo ========================================
echo   Building: %PROJECT_DIR%
echo ========================================
echo.

python "%TOOLS_DIR%\project_builder.py" --project "%PROJECT_DIR%" %2 %3 %4

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   构建完成
    echo ========================================
    echo.
    echo 下一步上传: upload_project.bat %PROJECT_NAME%
    echo.
)

endlocal
pause
