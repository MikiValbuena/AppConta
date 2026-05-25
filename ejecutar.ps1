<#
.SYNOPSIS
    AppConta - Contabilidad Personal 2025
.DESCRIPTION
    Script de ejecucion para AppConta. Verifica dependencias y lanza la aplicacion.
#>

$ErrorActionPreference = "Stop"
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   AppConta - Contabilidad Personal 2025" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
try {
    $pyVersion = python --version 2>&1
    Write-Host "[OK] Python detectado: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python no esta instalado." -ForegroundColor Red
    Write-Host "Descargalo desde: https://python.org" -ForegroundColor Yellow
    Read-Host "`nPresiona Enter para salir"
    exit 1
}

# Verificar dependencias
Write-Host "`nVerificando dependencias..." -ForegroundColor Yellow
$paquetes = @("ttkbootstrap", "matplotlib", "openpyxl")
foreach ($pkg in $paquetes) {
    try {
        python -c "import $pkg" 2>&1 | Out-Null
        Write-Host "  [OK] $pkg" -ForegroundColor Green
    } catch {
        Write-Host "  Instalando $pkg..." -ForegroundColor Yellow
        pip install $pkg -q
        Write-Host "  [OK] $pkg instalado" -ForegroundColor Green
    }
}

# Lanzar aplicacion
Write-Host "`nIniciando AppConta..." -ForegroundColor Green
Write-Host ""
python main.py

if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
    Write-Host "`n[ERROR] La aplicacion se cerro inesperadamente." -ForegroundColor Red
    Read-Host "`nPresiona Enter para salir"
}
