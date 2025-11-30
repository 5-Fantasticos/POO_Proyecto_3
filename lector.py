import os
import tempfile
import requests
import winsound
import pyttsx3
from typing import List, Dict, Optional

# Configuration
RVC_URL = os.environ.get("RVC_URL", "http://127.0.0.1:7865")  # Common default for RVC WebUI
RVC_SPEAKER = os.environ.get("RVC_SPEAKER", "Hatsune Miku")  # Desired target voice/model name
RVC_ENDPOINT = os.environ.get("RVC_ENDPOINT", "/voice_conversion")  # Hypothetical endpoint
VOICEVOX_SPEAKER = None  # Legacy disabled


def _sapi_tts_to_wav(text: str) -> Optional[bytes]:
    """Generate WAV bytes using a fresh pyttsx3 engine each call."""
    try:
        engine = pyttsx3.init()
        # Select Spanish voice if available
        try:
            voices = engine.getProperty('voices')
            es_voice = None
            for v in voices:
                name = getattr(v, 'name', '') or ''
                lang = ''.join(getattr(v, 'languages', []) or [])
                if ('Spanish' in name) or ('es' in lang.lower()) or ('es_' in lang.lower()):
                    es_voice = v.id
                    break
            if es_voice:
                engine.setProperty('voice', es_voice)
        except Exception:
            pass
        engine.setProperty('rate', 170)
    except Exception:
        return None
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        engine.save_to_file(text, path)
        engine.runAndWait()
        with open(path, 'rb') as f:
            return f.read()
    finally:
        try:
            os.remove(path)
        except Exception:
            pass


def _rvc_available() -> bool:
    try:
        r = requests.get(RVC_URL, timeout=1.5)
        return r.status_code < 500
    except Exception:
        return False


def _rvc_convert(wav_bytes: bytes, speaker: str) -> bytes:
    """
    Send the source WAV to RVC WebUI for conversion.
    This assumes a HTTP API compatible with `so-vits-svc / RVC WebUI`.
    The exact endpoint may differ. Adjust `RVC_ENDPOINT` as needed.
    """
    files = {
        'audio': ('input.wav', wav_bytes, 'audio/wav')
    }
    data = {
        'speaker': speaker,
        'format': 'wav'
    }
    url = RVC_URL.rstrip('/') + RVC_ENDPOINT
    r = requests.post(url, files=files, data=data, timeout=60)
    r.raise_for_status()
    return r.content


def _play_wav_bytes(wav_bytes: bytes) -> None:
    # Ensure any previous sound is stopped/purged to allow replays
    try:
        winsound.PlaySound(None, winsound.SND_PURGE)
    except Exception:
        pass
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        with open(path, 'wb') as f:
            f.write(wav_bytes)
        # Play synchronously; allow OS to use default device
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_NODEFAULT)
    finally:
        try:
            # Purge again to release any handle and allow next playback
            winsound.PlaySound(None, winsound.SND_PURGE)
            os.remove(path)
        except Exception:
            pass


def _normalize_text(text: str) -> str:
    # Minimal normalization for Spanish clarity
    rep = {
        'LUN': 'lunes', 'MAR': 'martes', 'MIE': 'miércoles', 'JUE': 'jueves',
        'VIE': 'viernes', 'SAB': 'sábado', 'DOM': 'domingo',
    }
    for k, v in rep.items():
        text = text.replace(k, v)
    return text


def leer_tareas_pendientes(tareas: List[Dict]) -> None:
    """Lee en voz alta las tareas pendientes. Intenta RVC; si falla, usa SAPI."""
    texto = _construir_texto_tareas(tareas)
    texto = _normalize_text(texto)
    # Generar base WAV con SAPI
    wav_bytes = _sapi_tts_to_wav(texto)
    if not wav_bytes:
        return
    # Convertir con RVC si está disponible
    if _rvc_available():
        try:
            conv = _rvc_convert(wav_bytes, RVC_SPEAKER)
            _play_wav_bytes(conv)
            return
        except Exception:
            pass
    # Reproducir SAPI si RVC no está disponible
    _play_wav_bytes(wav_bytes)

def _construir_texto_tareas(tareas: List[Dict]) -> str:
    if not tareas:
        return "No tienes tareas pendientes."
    partes = []
    for r in tareas:
        titulo = r.get('titulo', '')
        hora = r.get('hora', '')
        importante = r.get('importante', False)
        marcador = " Importante." if importante else ""
        partes.append(f"{titulo} a las {hora}.{marcador}")
    return " ".join(partes)

def _normalize_text(text: str) -> str:
    # Minimal normalization for Spanish clarity
    rep = {
        'LUN': 'lunes', 'MAR': 'martes', 'MIE': 'miércoles', 'JUE': 'jueves',
        'VIE': 'viernes', 'SAB': 'sábado', 'DOM': 'domingo',
    }
    for k, v in rep.items():
        text = text.replace(k, v)
    return text

# Legacy Voicevox functions removed

def _construir_texto_tareas(tareas: List[Dict]) -> str:
    if not tareas:
        return "No tienes tareas pendientes."
    partes = []
    for r in tareas:
        titulo = r.get('titulo', '')
        hora = r.get('hora', '')
        importante = r.get('importante', False)
        marcador = " Importante." if importante else ""
        partes.append(f"{titulo} a las {hora}.{marcador}")
    return " ".join(partes)


def _play_wav_bytes(wav_bytes: bytes) -> None:
    # Ensure any previous sound is stopped/purged to allow replays
    try:
        winsound.PlaySound(None, winsound.SND_PURGE)
    except Exception:
        pass
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        with open(path, 'wb') as f:
            f.write(wav_bytes)
        # Play synchronously; allow OS to use default device
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_NODEFAULT)
    finally:
        try:
            # Purge again to release any handle and allow next playback
            winsound.PlaySound(None, winsound.SND_PURGE)
            os.remove(path)
        except Exception:
            pass


def leer_tareas_pendientes(tareas: List[Dict]) -> None:
    """Lee en voz alta las tareas pendientes. Intenta RVC; si falla, usa SAPI."""
    texto = _construir_texto_tareas(tareas)
    # Generar base WAV con SAPI
    wav_bytes = _sapi_tts_to_wav(texto)
    if not wav_bytes:
        return
    # TODO: Integrar _rvc_convert si está disponible; por ahora reproducimos SAPI
    _play_wav_bytes(wav_bytes)
