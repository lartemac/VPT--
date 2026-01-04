@echo off
REM 同步 Claude Code 全局配置文件
REM 从项目文件夹同步到系统配置位置

set PROJECT_DIR=D:\cc-github
set CONFIG_DIR=%USERPROFILE%\.claude
set PROJECT_CONFIG=%PROJECT_DIR%\CLAUDE-global.md
set SYSTEM_CONFIG=%CONFIG_DIR%\CLAUDE.md

echo 正在同步 Claude Code 配置文件...
echo.

REM 检查项目配置文件是否存在
if not exist "%PROJECT_CONFIG%" (
    echo 错误: 项目配置文件不存在: %PROJECT_CONFIG%
    pause
    exit /b 1
)

REM 备份现有配置
if exist "%SYSTEM_CONFIG%" (
    echo 备份现有配置...
    copy "%SYSTEM_CONFIG%" "%SYSTEM_CONFIG%.backup" >nul
)

REM 复制配置文件
echo 从项目同步配置到系统...
copy "%PROJECT_CONFIG%" "%SYSTEM_CONFIG%" >nul

echo.
echo ✓ 配置文件同步完成！
echo.
echo 源文件: %PROJECT_CONFIG%
echo 目标文件: %SYSTEM_CONFIG%
echo.
timeout /t 2 >nul
