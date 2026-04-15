@echo off
chcp 65001 >nul
setlocal

REM ============================================
REM UrhoX Project Creator
REM Usage: create_project.bat [project_name] [--author author_id]
REM ============================================

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "TOOLS_DIR=%SCRIPT_DIR%\..\..\tools\project-tools"

if "%~1"=="" (
    echo.
    echo ========================================
    echo   UrhoX Project Creator
    echo ========================================
    echo.
    python "%TOOLS_DIR%\project_creator.py" --output "%SCRIPT_DIR%"
) else (
    python "%TOOLS_DIR%\project_creator.py" --output "%SCRIPT_DIR%" %*
)

if %ERRORLEVEL% EQU 0 (
    echo --------------------------------------------------
    echo.
    echo 下一步构建: build_project.bat ^<项目目录^>
    echo.
)

endlocal
pause
