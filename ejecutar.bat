@echo off
title AppConta - Contabilidad Personal
cd /d "%~dp0"

echo ============================================
echo    AppConta - Contabilidad Personal 2025
echo ============================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado.
    echo Descargalo desde: https://python.org
    pause
    exit /b 1
)

echo [OK] Python detectado

REM Verificar/instalar dependencias
echo.
echo Verificando dependencias...
pip install ttkbootstrap matplotlib openpyxl -q 2>&1 | findstr /V "already satisfied requirement"
echo [OK] Dependencias listas

echo.
echo Iniciando AppConta...
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] La aplicacion se cerro inesperadamente.
    pause
)
