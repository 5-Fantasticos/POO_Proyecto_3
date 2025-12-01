from kivy.graphics import Color, Ellipse, Line
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivy.metrics import dp

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
