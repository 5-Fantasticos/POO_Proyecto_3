"""Aplicación de recordatorios convertida de Tkinter a Kivy."""

from kivy.config import Config

# Configuración de ventana similar a la antigua app de Tkinter.
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "450")
Config.set("graphics", "resizable", False)

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import json
import os
from datetime import datetime
import threading
from lector import leer_tareas_pendientes
import sys

Window.clearcolor = (0, 0, 0, 1)


class GraficaSemanal(Widget):
    """Widget que simula una pequeña gráfica de progreso."""

    puntos = ListProperty(
        [
            (0.05, 0.45),
            (0.25, 0.5),
            (0.45, 0.5),
            (0.65, 0.75),
            (0.85, 0.35),
        ]
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.actualizar_canvas, size=self.actualizar_canvas, puntos=self.actualizar_canvas)

    def actualizar_canvas(self, *args):
        self.canvas.clear()
        if not self.puntos:
            return

        with self.canvas:
            Color(0, 0, 0, 1)
            puntos_escalados = []
            for x_rel, y_rel in self.puntos:
                x = self.x + x_rel * self.width
                y = self.y + y_rel * self.height
                puntos_escalados.extend([x, y])

            Line(points=puntos_escalados, width=1.5)

            for i in range(0, len(puntos_escalados), 2):
                Ellipse(pos=(puntos_escalados[i] - 4, puntos_escalados[i + 1] - 4), size=(8, 8))


class InicioScreen(Screen):
    pass

class UsuarioScreen(Screen):
    pass

class PrincipalScreen(Screen):
    pass

class RealizadasScreen(Screen):
    pass

    filtro_dia_realizadas = 'todos'
class RecordatorioScreen(Screen):
    pass

class ListaRecordatoriosScreen(Screen):
    pass


KV = r"""
#:import dp kivy.metrics.dp
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition(duration=0.2)
    InicioScreen:
    UsuarioScreen:
    PrincipalScreen:
    RealizadasScreen:
    RecordatorioScreen:
    ListaRecordatoriosScreen:

<ColoredSpacer@Widget>:
    size_hint_y: None
    height: dp(20)

<DarkLabel@Label>:
    color: 1, 1, 1, 1
    text_size: self.width, None
    halign: 'center'

<InfoLabel@Label>:
    color: 1, 1, 1, 1
    text_size: self.width, None
    halign: 'left'

<DayToggle@ToggleButton>:
    size_hint_y: None
    height: dp(34)
    background_normal: ''
    background_down: ''
    background_color: (0.4, 0.0, 0.5, 1) if self.state == 'down' else (0.15, 0.15, 0.15, 1)
    color: 1, 1, 1, 1

<InicioScreen>:
    name: 'inicio'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(20)
        ColoredSpacer:
        DarkLabel:
            text: 'HOLA!!'
            font_size: '24sp'
            bold: True
        GridLayout:
            cols: 2
            spacing: dp(20)
            size_hint_y: None
            height: dp(140)
            Button:
                text: 'Usuario'
                font_size: '18sp'
                color: 1, 1, 1, 1
                background_normal: ''
                background_color: 0.4, 0.0, 0.5, 1
                on_release: app.cambiar_pantalla('usuario')
            Button:
                text: 'Administrador'
                font_size: '18sp'
                color: 1, 1, 1, 1
                background_normal: ''
                background_color: 0.4, 0.0, 0.5, 1
                on_release: app.cambiar_pantalla('principal')
        Widget:
        ColoredSpacer:

<UsuarioScreen>:
    name: 'usuario'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(12)
        DarkLabel:
            text: 'Recordatorios Pendientes'
            font_size: '20sp'
            bold: True
        Widget:
            size_hint_y: None
            height: dp(35)
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: usuario_cont
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(8)
        Button:
            size_hint_y: None
            height: dp(48)
            text: 'Leer pendientes'
            color: 1,1,1,1
            background_normal: ''
            background_color: 0.4,0.0,0.5,1
            on_release: app.leer_pendientes()
        Button:
            size_hint_y: None
            height: dp(48)
            text: 'Volver'
            color: 1,1,1,1
            background_normal: ''
            background_color: 0.4,0.0,0.5,1
            on_release: app.cambiar_pantalla('inicio')

<PrincipalScreen>:
    name: 'principal'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(12)
        Widget:
            size_hint_y: 0.35  # espacio superior
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(380)
            spacing: dp(14)
            Button:
                text: 'Tareas realizadas'
                font_size: '20sp'
                size_hint_y: None
                height: dp(70)
                color: 1, 1, 1, 1
                background_normal: ''
                background_color: 0.4, 0.0, 0.5, 1
                on_release: app.cambiar_pantalla('tareas')
            Button:
                text: 'Crear Recordatorio'
                font_size: '20sp'
                size_hint_y: None
                height: dp(70)
                color: 1, 1, 1, 1
                background_normal: ''
                background_color: 0.4, 0.0, 0.5, 1
                on_release: app.cambiar_pantalla('recordatorio')
            Button:
                text: 'Eliminar Recordatorio'
                font_size: '20sp'
                size_hint_y: None
                height: dp(70)
                color: 1, 1, 1, 1
                background_normal: ''
                background_color: 0.4, 0.0, 0.5, 1
                on_release: app.mostrar_lista('eliminar')
            Button:
                text: 'Modificar Recordatorio'
                font_size: '20sp'
                size_hint_y: None
                height: dp(70)
                color: 1, 1, 1, 1
                background_normal: ''
                background_color: 0.4, 0.0, 0.5, 1
                on_release: app.mostrar_lista('modificar')
            Button:
                text: 'Inicio'
                font_size: '16sp'
                size_hint_y: None
                height: dp(50)
                color: 1,1,1,1
                background_normal: ''
                background_color: 0.4,0.0,0.5,1
                on_release: app.cambiar_pantalla('inicio')
        Widget:
            size_hint_y: 0.65  # espacio inferior mayor para empujar bloque hacia abajo
<ListaRecordatoriosScreen>:
    name: 'lista'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(10)
        DarkLabel:
            id: titulo_lista
            text: 'Selecciona un recordatorio'
            font_size: '18sp'
            bold: True
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: contenedor_lista
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(8)
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            Button:
                text: 'Volver'
                color: 1, 1, 1, 1
                background_normal: ''
                background_color: 0.4, 0.0, 0.5, 1
                on_release: app.cambiar_pantalla('principal')

<RealizadasScreen>:
    name: 'tareas'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(12)
        DarkLabel:
            text: 'Tareas realizadas'
            font_size: '20sp'
            bold: True
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            Button:
                text: 'Prioritarias'
                color: 1,1,1,1
                background_normal: ''
                background_color: (0.4, 0.0, 0.5, 1) if app.filtro_realizadas == 'prioritarias' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_realizadas('prioritarias')
            Button:
                text: 'Secundarias'
                color: 1,1,1,1
                background_normal: ''
                background_color: (0.4, 0.0, 0.5, 1) if app.filtro_realizadas == 'secundarias' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_realizadas('secundarias')
        BoxLayout:
            size_hint_y: None
            height: dp(46)
            spacing: dp(6)
            Button:
                text: 'Todos'
                font_size: '14sp'
                background_normal: ''
                background_color: (0.4,0.0,0.5,1) if app.filtro_dia_realizadas == 'todos' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_dia_realizadas('todos')
            Button:
                text: 'LUN'
                font_size: '14sp'
                background_normal: ''
                background_color: (0.4,0.0,0.5,1) if app.filtro_dia_realizadas == 'LUN' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_dia_realizadas('LUN')
            Button:
                text: 'MAR'
                font_size: '14sp'
                background_normal: ''
                background_color: (0.4,0.0,0.5,1) if app.filtro_dia_realizadas == 'MAR' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_dia_realizadas('MAR')
            Button:
                text: 'MIE'
                font_size: '14sp'
                background_normal: ''
                background_color: (0.4,0.0,0.5,1) if app.filtro_dia_realizadas == 'MIE' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_dia_realizadas('MIE')
            Button:
                text: 'JUE'
                font_size: '14sp'
                background_normal: ''
                background_color: (0.4,0.0,0.5,1) if app.filtro_dia_realizadas == 'JUE' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_dia_realizadas('JUE')
            Button:
                text: 'VIE'
                font_size: '14sp'
                background_normal: ''
                background_color: (0.4,0.0,0.5,1) if app.filtro_dia_realizadas == 'VIE' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_dia_realizadas('VIE')
            Button:
                text: 'SAB'
                font_size: '14sp'
                background_normal: ''
                background_color: (0.4,0.0,0.5,1) if app.filtro_dia_realizadas == 'SAB' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_dia_realizadas('SAB')
            Button:
                text: 'DOM'
                font_size: '14sp'
                background_normal: ''
                background_color: (0.4,0.0,0.5,1) if app.filtro_dia_realizadas == 'DOM' else (0.15,0.15,0.15,1)
                on_release: app.cambiar_filtro_dia_realizadas('DOM')
        BoxLayout:
            size_hint_y: None
            height: dp(46)
            spacing: dp(6)
            Label:
                text: 'Semana:'
                color: 1,1,1,1
                size_hint_x: None
                width: dp(70)
            Spinner:
                id: semana_spn
                text: app.filtro_semana_realizadas if app.filtro_semana_realizadas else 'todas'
                values: ('todas','Semana 1','Semana 2','Semana 3','Semana 4')
                size_hint_y: None
                height: dp(40)
                background_color: (0.4,0.0,0.5,1) if app.filtro_semana_realizadas != 'todas' else (0.15,0.15,0.15,1)
                color: 1,1,1,1
                on_text: app.cambiar_filtro_semana_realizadas(self.text)
        BoxLayout:
            size_hint_y: None
            height: dp(46)
            spacing: dp(10)
            Label:
                text: 'Mes:'
                color: 1,1,1,1
                size_hint_x: None
                width: dp(70)
            Spinner:
                id: mes_spn
                text: app.filtro_mes_realizadas if app.filtro_mes_realizadas else 'todos'
                values: ('todos','enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre')
                size_hint_y: None
                height: dp(40)
                background_color: (0.4,0.0,0.5,1) if app.filtro_mes_realizadas != 'todos' else (0.15,0.15,0.15,1)
                color: 1,1,1,1
                on_text: app.cambiar_filtro_mes_realizadas(self.text)
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: realizadas_cont
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(8)
        Button:
            size_hint_y: None
            height: dp(48)
            text: 'Volver'
            color: 1, 1, 1, 1
            background_normal: ''
            background_color: 0.4, 0.0, 0.5, 1
            on_release: app.cambiar_pantalla('principal')

<RecordatorioScreen>:
    name: 'recordatorio'
    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: dp(10)
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)
                spacing: dp(10)
                DarkLabel:
                    text: 'AÑADIR RECORDATORIO'
                    font_size: '18sp'
                    bold: True
                InfoLabel:
                    text: 'Título'
                TextInput:
                    id: titulo_input
                    size_hint_y: None
                    height: dp(40)
                    multiline: False
                InfoLabel:
                    text: 'Hora (HH:MM)'
                TextInput:
                    id: hora_input
                    size_hint_y: None
                    height: dp(40)
                    text: '10:05'
                    multiline: False
                InfoLabel:
                    text: 'Repetir'
                Spinner:
                    id: repetir_spn
                    size_hint_y: None
                    height: dp(40)
                    text: 'No repetir'
                    values: ('No repetir','Diariamente','Semanalmente','Mensualmente')
                BoxLayout:
                    size_hint_y: None
                    height: dp(30)
                    spacing: dp(10)
                    InfoLabel:
                        text: 'Importante'
                        halign: 'left'
                    CheckBox:
                        id: importante_chk
                        size_hint_x: None
                        width: dp(30)
                InfoLabel:
                    text: 'Días de recordatorio'
                GridLayout:
                    cols: 4
                    spacing: dp(6)
                    size_hint_y: None
                    height: dp(90)
                    DayToggle:
                        id: dia_lun
                        text: 'LUN'
                    DayToggle:
                        id: dia_mar
                        text: 'MAR'
                    DayToggle:
                        id: dia_mie
                        text: 'MIE'
                    DayToggle:
                        id: dia_jue
                        text: 'JUE'
                    DayToggle:
                        id: dia_vie
                        text: 'VIE'
                    DayToggle:
                        id: dia_sab
                        text: 'SAB'
                    DayToggle:
                        id: dia_dom
                        text: 'DOM'
                BoxLayout:
                    size_hint_y: None
                    height: dp(30)
                    spacing: dp(10)
                    InfoLabel:
                        text: 'Mantener'
                        halign: 'left'
                    CheckBox:
                        id: mantener_chk
                        size_hint_x: None
                        width: dp(30)
                BoxLayout:
                    size_hint_y: None
                    height: dp(30)
                    spacing: dp(10)
                    InfoLabel:
                        text: 'Alarma'
                        halign: 'left'
                    CheckBox:
                        id: alarma_chk
                        size_hint_x: None
                        width: dp(30)
                InfoLabel:
                    text: 'Sonido'
                Spinner:
                    id: sonido_spn
                    size_hint_y: None
                    height: dp(40)
                    text: 'JHON CENA SATURED'
                    values: ('JHON CENA SATURED', 'Otro sonido')
                BoxLayout:
                    size_hint_y: None
                    height: dp(30)
                    spacing: dp(10)
                    InfoLabel:
                        text: 'Mantener'
                        halign: 'left'
                    CheckBox:
                        id: mantener_chk
                        size_hint_x: None
                        width: dp(30)
        BoxLayout:
            size_hint_y: None
            height: dp(56)
            spacing: dp(10)
            padding: dp(10), 0
            Button:
                text: 'Crear'
                color: 1, 1, 1, 1
                background_normal: ''
                background_color: 0.4, 0.0, 0.5, 1
                on_release: app.crear_recordatorio()
        Button:
            size_hint_y: None
            height: dp(48)
            text: 'Volver'
            color: 1, 1, 1, 1
            background_normal: ''
            background_color: 0.4, 0.0, 0.5, 1
            on_release: app.cambiar_pantalla('principal')
"""


class MemoriaApp(App):
    """Aplicación principal usando ScreenManager para las vistas."""

    def build(self):
        self.title = "Administrador"
        # Resolver ruta de datos soportando ejecución congelada (PyInstaller)
        if getattr(sys, 'frozen', False):
            # En ejecutable onefile, _MEIPASS es temporal; usar siempre carpeta del .exe para persistencia.
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(__file__)
        self.data_path = os.path.join(base_dir, 'recordatorios.json')
        root = Builder.load_string(KV)
        # Reactivar tareas recurrentes al iniciar
        self.actualizar_recurrencias()
        return root

    # Propiedades reactivas para que el KV actualice colores automáticamente
    filtro_realizadas = StringProperty('prioritarias')
    filtro_dia_realizadas = StringProperty('todos')
    filtro_semana_realizadas = StringProperty('todas')
    filtro_mes_realizadas = StringProperty('todos')

    def cambiar_pantalla(self, nombre):
        if self.root:
            self.root.current = nombre
            # Antes de mostrar pantallas que dependen de pendientes/completadas reactivar recurrencias
            if nombre in ('usuario','tareas'):
                self.actualizar_recurrencias()
            if nombre == 'tareas':
                self.actualizar_realizadas()
            if nombre == 'usuario':
                self.actualizar_usuario()

    # (El método anterior crear_recordatorio simplificado se reemplazó por la versión extendida más abajo.)

    def _cargar_todos(self):
        if not os.path.exists(self.data_path):
            return []
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _guardar_recordatorio(self, rec):
        datos = self._cargar_todos()
        # asignar id simple incremental
        next_id = (max((r.get('id', 0) for r in datos), default=0) + 1) if datos else 1
        rec['id'] = next_id
        if 'completado' not in rec:
            rec['completado'] = False
        datos.append(rec)
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def _actualizar_recordatorio(self, rec_id, rec_update):
        datos = self._cargar_todos()
        for i, r in enumerate(datos):
            if r.get('id') == rec_id:
                rec_update['id'] = rec_id
                if 'completado' not in rec_update:
                    rec_update['completado'] = r.get('completado', False)
                datos[i] = rec_update
                break
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def _eliminar_recordatorio(self, rec_id):
        datos = [r for r in self._cargar_todos() if r.get('id') != rec_id]
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def mostrar_lista(self, modo):
        """Muestra la pantalla de lista con botones por recordatorio.

        modo: 'eliminar' o 'modificar'.
        """
        sm = self.root
        sm.current = 'lista'
        screen = sm.get_screen('lista')
        ids = screen.ids
        # título
        ids['titulo_lista'].text = 'Eliminar: selecciona un recordatorio' if modo == 'eliminar' else 'Modificar: selecciona un recordatorio'
        cont = ids['contenedor_lista']
        cont.clear_widgets()
        for r in self._cargar_todos():
            txt = f"[{r.get('id')}] {r.get('titulo','')} - {r.get('hora','')}"
            btn = Button(text=txt, size_hint_y=None, height=40, color=(1,1,1,1), background_normal='', background_color=(0.15,0.15,0.15,1))
            if modo == 'eliminar':
                btn.bind(on_release=lambda _, rid=r.get('id'): self._accion_eliminar(rid))
            else:
                btn.bind(on_release=lambda _, rec=r: self._accion_modificar(rec))
            cont.add_widget(btn)

    def _accion_eliminar(self, rec_id):
        self._eliminar_recordatorio(rec_id)
        Popup(title='Eliminado', content=Label(text=f'Recordatorio {rec_id} eliminado'), size_hint=(0.7, 0.4)).open()
        # refrescar lista
        self.mostrar_lista('eliminar')

    def _accion_modificar(self, rec):
        """Carga el recordatorio en el formulario para edición."""
        sm = self.root
        sm.current = 'recordatorio'
        screen = sm.get_screen('recordatorio')
        ids = screen.ids
        # Guardar id en app para actualizar luego
        self._rec_edit_id = rec.get('id')
        ids['titulo_input'].text = rec.get('titulo','')
        ids['hora_input'].text = rec.get('hora','')
        ids['mantener_chk'].active = bool(rec.get('mantener', False))
        ids['alarma_chk'].active = bool(rec.get('alarma', False))
        ids['sonido_spn'].text = rec.get('sonido','')
        # Cargar repetición
        rep = rec.get('repetir', 'No repetir')
        if 'repetir_spn' in ids:
            ids['repetir_spn'].text = rep if rep in ['No repetir','Diariamente','Semanalmente','Mensualmente'] else 'No repetir'
        if 'importante_chk' in ids:
            ids['importante_chk'].active = bool(rec.get('importante'))
        # días
        dias_map = {
            'LUN':'dia_lun', 'MAR':'dia_mar', 'MIE':'dia_mie', 'JUE':'dia_jue',
            'VIE':'dia_vie', 'SAB':'dia_sab', 'DOM':'dia_dom'
        }
        for d, did in dias_map.items():
            w = ids.get(did)
            if w:
                w.state = 'down' if d in (rec.get('dias') or []) else 'normal'

    def crear_recordatorio(self):
        """Recoge los campos del formulario y crea o actualiza."""
        sm = self.root
        screen = sm.get_screen('recordatorio')
        ids = screen.ids

        titulo = ids.get('titulo_input').text if ids.get('titulo_input') else ''
        hora = ids.get('hora_input').text if ids.get('hora_input') else ''
        mantener = ids.get('mantener_chk').active if ids.get('mantener_chk') else False
        alarma = ids.get('alarma_chk').active if ids.get('alarma_chk') else False
        sonido = ids.get('sonido_spn').text if ids.get('sonido_spn') else ''
        repetir = ids.get('repetir_spn').text if ids.get('repetir_spn') else 'No repetir'
        importante = ids.get('importante_chk').active if ids.get('importante_chk') else False

        dias_ids = ['dia_lun', 'dia_mar', 'dia_mie', 'dia_jue', 'dia_vie', 'dia_sab', 'dia_dom']
        dias_sel = []
        for did in dias_ids:
            w = ids.get(did)
            if w and getattr(w, 'state', '') == 'down':
                dias_sel.append(w.text)
        # Ajustar según repetición
        if repetir == 'Diariamente':
            dias_sel = ['LUN','MAR','MIE','JUE','VIE','SAB','DOM']
        # Semanalmente: mantener selección actual
        # Mensualmente: mantener selección; se podría extender lógica futura.

        nuevo = {
            'titulo': titulo,
            'hora': hora,
            'dias': dias_sel,
            'mantener': mantener,
            'alarma': alarma,
            'sonido': sonido,
            'importante': importante,
            'repetir': repetir,
        }

        if getattr(self, '_rec_edit_id', None):
            rid = self._rec_edit_id
            self._actualizar_recordatorio(rid, nuevo)
            self._rec_edit_id = None
            Popup(title='Recordatorio actualizado', content=Label(text=f'[{rid}] actualizado'), size_hint=(0.7, 0.4)).open()
        else:
            nuevo['completado'] = False
            self._guardar_recordatorio(nuevo)
            Popup(title='Recordatorio creado', content=Label(text=f'Creado: {titulo}'), size_hint=(0.7, 0.4)).open()
    def actualizar_realizadas(self):
        cont = self.root.get_screen('tareas').ids.get('realizadas_cont')
        if not cont:
            return
        cont.clear_widgets()
        datos = self._cargar_todos()
        for r in datos:
            if not r.get('completado'):
                continue
            # filtro por importancia
            if self.filtro_realizadas == 'prioritarias' and not r.get('importante'):
                continue
            if self.filtro_realizadas == 'secundarias' and r.get('importante'):
                continue
            # filtro por mes (nombres en español)
            mes_sel = self.filtro_mes_realizadas
            if mes_sel != 'todos':
                fecha_comp_m = r.get('fecha_completado')
                if not fecha_comp_m:
                    continue
                try:
                    dtm = datetime.strptime(fecha_comp_m, '%Y-%m-%d')
                    if self._nombre_mes(dtm.month) != mes_sel:
                        continue
                except Exception:
                    continue
            # filtro por día
            dia_sel = self.filtro_dia_realizadas
            if dia_sel != 'todos':
                fecha_comp = r.get('fecha_completado')
                if not fecha_comp:
                    continue
                try:
                    dtc = datetime.strptime(fecha_comp, '%Y-%m-%d')
                    mapa = ['LUN','MAR','MIE','JUE','VIE','SAB','DOM']
                    if mapa[dtc.weekday()] != dia_sel:
                        continue
                except Exception:
                    continue
            # filtro por semana dinámica Semana 1..Semana 4
            semana_sel = self.filtro_semana_realizadas
            if semana_sel != 'todas':
                fecha_comp = r.get('fecha_completado')
                if not fecha_comp:
                    continue
                try:
                    dtc2 = datetime.strptime(fecha_comp, '%Y-%m-%d')
                    sm_label = self._etiqueta_semana(dtc2.day, self._nombre_mes(dtc2.month), dtc2.year)
                    if sm_label != semana_sel:
                        continue
                except Exception:
                    continue
            fila = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=8)
            lbl_txt = f"[{r.get('id')}] {r.get('titulo','(sin título)')} - {r.get('hora','')}"
            lbl = Label(text=lbl_txt, color=(1,1,1,1))
            fila.add_widget(lbl)
            cont.add_widget(fila)

    def cambiar_filtro_realizadas(self, modo):
        self.filtro_realizadas = modo
        self.actualizar_realizadas()

    def cambiar_filtro_dia_realizadas(self, dia):
        self.filtro_dia_realizadas = dia
        self.actualizar_realizadas()

    def cambiar_filtro_semana_realizadas(self, semana):
        self.filtro_semana_realizadas = semana
        self.actualizar_realizadas()

    def cambiar_filtro_mes_realizadas(self, mes):
        self.filtro_mes_realizadas = mes
        # Al cambiar de mes, reiniciar semana y día del mes para evitar inconsistencias.
        self.filtro_semana_realizadas = 'todas'
        self._recalcular_spinners_calendario()
        self.actualizar_realizadas()

    def _marcar_completado(self, rec_id):
        datos = self._cargar_todos()
        for r in datos:
            if r.get('id') == rec_id:
                r['completado'] = True
                if not r.get('fecha_completado'):
                    r['fecha_completado'] = datetime.now().strftime('%Y-%m-%d')
                break
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        # Refrescar pantallas si existen
        try:
            self.actualizar_realizadas()
            self.actualizar_usuario()
        except Exception:
            pass

    # --- Calendario dinámico ---
    def _dias_en_mes(self, mes, anio):
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
        # Febrero
        # Año bisiesto si divisible por 400, o divisible por 4 y no por 100
        bisiesto = (anio % 400 == 0) or (anio % 4 == 0 and anio % 100 != 0)
        return 29 if bisiesto else 28

    def _recalcular_spinners_calendario(self):
        if not self.root:
            return
        screen = self.root.get_screen('tareas')
        ids = screen.ids
        mes = self.filtro_mes_realizadas
        anio_actual = datetime.now().year
        # Semanas siempre 4 segmentos (renombradas)
        sem_spn = ids.get('semana_spn')
        if sem_spn:
            sem_spn.values = ('todas','Semana 1','Semana 2','Semana 3','Semana 4')
            if sem_spn.text not in sem_spn.values:
                sem_spn.text = 'todas'

    def _etiqueta_semana(self, day, mes, anio):
        # Divide el mes en 4 bloques lo más parejos posible.
        total = self._dias_en_mes(mes, anio)
        # Tamaño de segmento base
        seg = (total + 3) // 4  # ceil(total/4)
        # Rangos: Semana 1:1-seg, Semana 2:seg+1-2seg, Semana 3:2seg+1-3seg, Semana 4: resto
        if day <= seg:
            return 'Semana 1'
        if day <= 2*seg:
            return 'Semana 2'
        if day <= 3*seg:
            return 'Semana 3'
        return 'Semana 4'

    def _nombre_mes(self, num):
        nombres = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
        return nombres[num-1] if 1 <= num <= 12 else ''

    def actualizar_usuario(self):
        cont = self.root.get_screen('usuario').ids.get('usuario_cont') if self.root else None
        if not cont:
            return
        cont.clear_widgets()
        datos = self._cargar_todos()
        for r in datos:
            if r.get('completado'):
                continue
            fila = BoxLayout(orientation='horizontal', size_hint_y=None, height=44, spacing=8)
            lbl_txt = f"[{r.get('id')}] {r.get('titulo','(sin título)')} - {r.get('hora','')}"
            if r.get('importante'):
                lbl_txt += "  *"
            lbl = Label(text=lbl_txt, color=(1,1,1,1), halign='left')
            lbl.bind(size=lambda *_: setattr(lbl, 'text_size', (lbl.width, None)))
            btn = Button(text='Completar', size_hint_x=None, width=110, background_normal='', background_color=(0.4,0.0,0.5,1), color=(1,1,1,1))
            btn.bind(on_release=lambda _, rid=r.get('id'): self.marcar_completado_usuario(rid))
            fila.add_widget(lbl)
            fila.add_widget(btn)
            cont.add_widget(fila)

    def marcar_completado_usuario(self, rec_id):
        # Marcar como completado y refrescar lectura de pendientes
        self._marcar_completado(rec_id)
        # Tras completar, reactivar recurrencias si aplica y leer la lista actualizada
        try:
            self.actualizar_recurrencias()
        except Exception:
            pass
        self.leer_pendientes()

    def leer_pendientes(self):
        """Lanza lectura TTS de las tareas pendientes en un hilo separado."""
        datos = [r for r in self._cargar_todos() if not r.get('completado')]
        threading.Thread(target=leer_tareas_pendientes, args=(datos,), daemon=True).start()

    def actualizar_recurrencias(self):
        """Reactiva tareas completadas cuyo periodo de repetición ya pasó.

        Regla:
        - Diariamente: si fecha_completado < hoy -> volver a pendiente.
        - Semanalmente: si semana ISO o año cambió -> volver a pendiente.
        - Mensualmente: si mes o año cambió -> volver a pendiente.
        El campo fecha_completado se elimina al reactivar.
        """
        datos = self._cargar_todos()
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
                # sigue pendiente, no necesita reactivación
                continue
            fecha_txt = r.get('fecha_completado')
            if not fecha_txt:
                continue
            try:
                f = datetime.strptime(fecha_txt, '%Y-%m-%d').date()
            except Exception:
                continue
            # Diaria
            if repetir == 'Diariamente' and f < hoy:
                r['completado'] = False
                r.pop('fecha_completado', None)
                modifico = True
                continue
            # Semanal: cambia semana ISO
            if repetir == 'Semanalmente':
                if (f.isocalendar()[1] != semana_hoy) or (f.year != anio_hoy):
                    r['completado'] = False
                    r.pop('fecha_completado', None)
                    modifico = True
                    continue
            # Mensual: cambia mes
            if repetir == 'Mensualmente':
                if (f.month != hoy.month) or (f.year != anio_hoy):
                    r['completado'] = False
                    r.pop('fecha_completado', None)
                    modifico = True
                    continue
        if modifico:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    MemoriaApp().run()

