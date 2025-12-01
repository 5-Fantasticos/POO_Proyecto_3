"""Modelo de la aplicación de recordatorios, sin dependencias de Kivy."""

import json
import os
from datetime import datetime
import threading
from altavoz import leer_tareas_pendientes
import sys

class MemoriaModelo:
    """Lógica y gestión de datos para la aplicación de recordatorios."""

    def __init__(self):
        # Resolver ruta de datos soportando ejecución congelada (PyInstaller)
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(__file__)
        self.data_path = os.path.join(base_dir, 'recordatorios.json')
        # Filtros
        self.filtro_realizadas = 'prioritarias'
        self.filtro_dia_realizadas = 'todos'
        self.filtro_semana_realizadas = 'todas'
        self.filtro_mes_realizadas = 'todos'
        self._rec_edit_id = None

    def cargar_todos(self):
        if not os.path.exists(self.data_path):
            return []
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def guardar_recordatorio(self, rec):
        datos = self.cargar_todos()
        next_id = (max((r.get('id', 0) for r in datos), default=0) + 1) if datos else 1
        rec['id'] = next_id
        if 'completado' not in rec:
            rec['completado'] = False
        datos.append(rec)
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def actualizar_recordatorio(self, rec_id, rec_update):
        datos = self.cargar_todos()
        for i, r in enumerate(datos):
            if r.get('id') == rec_id:
                rec_update['id'] = rec_id
                if 'completado' not in rec_update:
                    rec_update['completado'] = r.get('completado', False)
                datos[i] = rec_update
                break
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def eliminar_recordatorio(self, rec_id):
        datos = [r for r in self.cargar_todos() if r.get('id') != rec_id]
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def marcar_completado(self, rec_id):
        datos = self.cargar_todos()
        for r in datos:
            if r.get('id') == rec_id:
                r['completado'] = True
                if not r.get('fecha_completado'):
                    r['fecha_completado'] = datetime.now().strftime('%Y-%m-%d')
                break
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def leer_pendientes(self):
        """Lanza lectura TTS de las tareas pendientes en un hilo separado."""
        datos = [r for r in self.cargar_todos() if not r.get('completado')]
        threading.Thread(target=leer_tareas_pendientes, args=(datos,), daemon=True).start()

    def actualizar_recurrencias(self):
        """Reactiva tareas completadas cuyo periodo de repetición ya pasó."""
        datos = self.cargar_todos()
        if not datos:
            return
        hoy = datetime.today().date()
        semana_hoy = hoy.isocalendar()[1]
        anio_hoy = hoy.year
        modifico = False
        for r in datos:
            repetir = r.get('repetir', 'No repetir')
            if repetir == 'No repetir':
                continue
            if not r.get('completado'):
                continue
            fecha_txt = r.get('fecha_completado')
            if not fecha_txt:
                continue
            try:
                f = datetime.strptime(fecha_txt, '%Y-%m-%d').date()
            except Exception:
                continue
            if repetir == 'Diariamente' and f < hoy:
                r['completado'] = False
                r.pop('fecha_completado', None)
                modifico = True
                continue
            if repetir == 'Semanalmente':
                if (f.isocalendar()[1] != semana_hoy) or (f.year != anio_hoy):
                    r['completado'] = False
                    r.pop('fecha_completado', None)
                    modifico = True
                    continue
            if repetir == 'Mensualmente':
                if (f.month != hoy.month) or (f.year != anio_hoy):
                    r['completado'] = False
                    r.pop('fecha_completado', None)
                    modifico = True
                    continue
        if modifico:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)

    # Métodos auxiliares para filtros y calendario
    def dias_en_mes(self, mes, anio):
        nombres = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
        if isinstance(mes, int):
            mes_i = mes
        else:
            try:
                mes_i = int(mes)
            except Exception:
                mes_lower = str(mes).lower()
                mes_i = (nombres.index(mes_lower) + 1) if mes_lower in nombres else 1
        if mes_i in [1,3,5,7,8,10,12]:
            return 31
        if mes_i in [4,6,9,11]:
            return 30
        bisiesto = (anio % 400 == 0) or (anio % 4 == 0 and anio % 100 != 0)
        return 29 if bisiesto else 28

    def etiqueta_semana(self, day, mes, anio):
        total = self.dias_en_mes(mes, anio)
        seg = (total + 3) // 4
        if day <= seg:
            return 'Semana 1'
        if day <= 2*seg:
            return 'Semana 2'
        if day <= 3*seg:
            return 'Semana 3'
        return 'Semana 4'

    def nombre_mes(self, num):
        nombres = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
        return nombres[num-1] if 1 <= num <= 12 else ''

