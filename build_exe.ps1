# PowerShell script to build the Kivy app executable with PyInstaller
# Usage:  powershell -ExecutionPolicy Bypass -File build_exe.ps1

$ErrorActionPreference = 'Stop'

Write-Host 'Creating virtual environment (if missing)...'
if (-not (Test-Path .venv)) {
    python -m venv .venv
}

Write-Host 'Activating virtual environment...'
. .\.venv\Scripts\activate.ps1

Write-Host 'Upgrading pip and installing requirements...'
pip install --upgrade pip
pip install -r requirements.txt

Write-Host 'Cleaning previous build artifacts...'
Remove-Item -Recurse -Force dist  -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item *.spec -ErrorAction SilentlyContinue

Write-Host 'Building single-file executable en carpeta raíz...'
# Nombre del script principal (con espacios requiere comillas)
$main = 'Fallo de memoria.py'
# Usamos --onefile y enviamos salida a la carpeta actual (--distpath .)
# No incluimos recordatorios.json empaquetado; la app lo creará junto al .exe si falta.
pyinstaller --noconsole --onefile --name MemoriaApp `
  --distpath . `
  --workpath build `
  --hidden-import kivy_deps.glew `
  --hidden-import kivy_deps.sdl2 `
  --hidden-import kivy_deps.angle `
  "$main"

Write-Host 'Build finalizado. Ejecutable: ./MemoriaApp.exe'
