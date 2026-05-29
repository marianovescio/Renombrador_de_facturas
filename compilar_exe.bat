@echo off
echo ============================================================
echo  Compilando ejecutables de Renombrador de Facturas
echo ============================================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH.
    echo Descargalo desde https://www.python.org/downloads/
    echo Asegurate de tildar "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

REM Instalar dependencias necesarias
echo [1/4] Instalando dependencias...
python -m pip install PyPDF2 pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: Fallo al instalar dependencias.
    pause
    exit /b 1
)
echo       OK
echo.

REM Compilar renombrar_A.exe
echo [2/4] Compilando Renombrar_Facturas_A.exe ...
python -m PyInstaller --onefile --windowed --name "Renombrar_Facturas_A" renombrar_A.py
if errorlevel 1 (
    echo ERROR: Fallo al compilar renombrar_A.py
    pause
    exit /b 1
)
echo       OK
echo.

REM Compilar renombrar_B.exe
echo [3/4] Compilando Renombrar_Facturas_B.exe ...
python -m PyInstaller --onefile --windowed --name "Renombrar_Facturas_B" renombrar_B.py
if errorlevel 1 (
    echo ERROR: Fallo al compilar renombrar_B.py
    pause
    exit /b 1
)
echo       OK
echo.

REM Mover los .exe a una carpeta "dist_final"
echo [4/4] Organizando archivos finales...
if not exist "dist_final" mkdir "dist_final"
copy "dist\Renombrar_Facturas_A.exe" "dist_final\" >nul
copy "dist\Renombrar_Facturas_B.exe" "dist_final\" >nul
echo       OK
echo.

echo ============================================================
echo  LISTO. Los .exe estan en la carpeta: dist_final\
echo  - Renombrar_Facturas_A.exe
echo  - Renombrar_Facturas_B.exe
echo ============================================================
pause
