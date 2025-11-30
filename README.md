# POO_Proyecto_3
 Mi memoria me falla  <br /> 
Nuestro caso se trata de Amador, una persona de  74 años que tiene fallos de memoria, el principal objetivo es diseñar una solucion efectiva, reconfortante y intuitiva.

propuesta planteada: Aplicacion de ayuda con las tareas diarias y necesarias para su dia a dia, tales como almorzar, ducharse, tomarse el medicamento entre otros, proponemos una que la app funcione como tipo calendario, siguiendo un horario establecido por un tercero para que pueda el usuario seguirlas completamente, con sistema de alarmas, registro de tareas realizadas y estadisticas del mes, para tambien ir regulando el avance del estado de la personaa medida pasa el tiempo,

## Ejecutar la aplicación (modo desarrollo)

1. Crear (o usar) entorno virtual:
```powershell
python -m venv .venv
```
2. Activar:
```powershell
./.venv/Scripts/activate.ps1
```
3. Instalar dependencias:
```powershell
pip install -r requirements.txt
```
4. Ejecutar:
```powershell
python "Fallo de memoria.py"
```

## Crear ejecutable (Windows)

Usamos PyInstaller. Ahora se genera directamente en la carpeta del proyecto (`./MemoriaApp.exe`).

Opción rápida:
```powershell
./build_exe.ps1
```

Manual (equivalente):
```powershell
pip install --upgrade pip
pip install -r requirements.txt
pyinstaller --noconsole --onefile --name MemoriaApp `
	--distpath . `
	--workpath build `
	--hidden-import kivy_deps.glew `
	--hidden-import kivy_deps.sdl2 `
	--hidden-import kivy_deps.angle `
	"Fallo de memoria.py"
```

Resultado: `./MemoriaApp.exe`

`recordatorios.json` se creará automáticamente junto al `.exe` si no existe.

## Texto a voz (TTS) con RVC (Hatsune Miku)

El lector ahora usa RVC (Retrieval-based Voice Conversion) para convertir la voz base de SAPI al timbre de Hatsune Miku.

### Requisitos
- Windows (usa SAPI/pyttsx3 para generar el audio base).
- RVC WebUI (so-vits-svc / RVC) ejecutándose localmente con un modelo de Hatsune Miku cargado.

### Configuración
Variables de entorno opcionales (ya tienen valores por defecto):

```powershell
$env:RVC_URL = "http://127.0.0.1:7865"   # URL del WebUI
$env:RVC_SPEAKER = "Hatsune Miku"         # Nombre/modelo en el WebUI
$env:RVC_ENDPOINT = "/voice_conversion"   # Endpoint HTTP para convertir
```

Nota: El endpoint exacto depende del WebUI que uses. Ajusta `RVC_ENDPOINT` según tu interfaz (algunas versiones exponen `/api/voice` o similar). El lector enviará el WAV generado por SAPI y esperará recibir WAV convertido.

### Uso
- Arranca el RVC WebUI con el modelo de Miku cargado.
- Ejecuta la app como siempre. Al pulsar "Leer pendientes" o completar tareas, el lector generará TTS neutral y lo convertirá vía RVC.

### Fallback
Si RVC no está disponible, se reproducirá el TTS base de SAPI.

## Notas

- El archivo `Fallo de memoria.py` detecta ejecución congelada (PyInstaller) para ubicar correctamente `recordatorios.json`.
- Para limpiar builds antiguos: borra carpetas `dist`, `build` y el archivo `.spec`.
- Si hay problemas con DLLs de Kivy, instala dependencias gráficas: ya están listadas en `requirements.txt` (angle, glew, sdl2).













 
Documento de google <br /> 
https://docs.google.com/document/d/1wTCVDPMaxmtAMokxY_dopqj6cLcsehnneeyvNG2_0Yc/edit?usp=sharing 

PPT <br /> 
https://1drv.ms/p/c/e5c8ae5506bdcb83/EV8CFwP2q29OpEn6hKiGw9YBXGMHq5PZqBtsRSY8K5TD1w?e=3PegiZ 
