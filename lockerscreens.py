import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import StringProperty, BooleanProperty


class LockerBox(BoxLayout):
    locker_number = StringProperty('')
    is_available = BooleanProperty(True)  # True = disponível (verde), False = indisponível (vermelho)
    
    __events__ = ('on_locker_select',)  # Evento personalizado quando cacifo é selecionado

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(120), dp(150))
        self.padding = dp(10)
        self.spacing = dp(5)
        
        # Cores baseadas na disponibilidade
        self.available_color = (46/255, 204/255, 64/255, 1)  # Verde
        self.unavailable_color = (231/255, 76/255, 60/255, 1)  # Vermelho
        
        # Cor atual baseada no status
        self.current_color = self.available_color if self.is_available else self.unavailable_color
        
        # Background do cacifo
        with self.canvas.before:
            Color(*self.current_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.bind(is_available=self._update_color)
        
        # Número do cacifo (maior e mais destacado)
        self.number_label = Label(
            text=f'#{self.locker_number}',
            font_size='28sp',
            size_hint_y=None,
            height=dp(80),
            color=(1, 1, 1, 1),  # Branco
            bold=True,
            halign='center',
            valign='middle'
        )
        
        # Status do cacifo
        self.status_label = Label(
            text='Disponível' if self.is_available else 'Ocupado',
            font_size='14sp',
            size_hint_y=None,
            height=dp(40),
            color=(1, 1, 1, 1),  # Branco
            halign='center',
            valign='middle'
        )
        
        # Adiciona os widgets (sem ícone)
        self.add_widget(self.number_label)
        self.add_widget(self.status_label)
        
        # Bind para atualizações de propriedades
        self.bind(locker_number=self._update_number)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _update_color(self, instance, value):
        """Atualiza a cor baseada na disponibilidade"""
        self.current_color = self.available_color if self.is_available else self.unavailable_color
        with self.canvas.before:
            Color(*self.current_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        
        # Atualiza o texto do status
        self.status_label.text = 'Disponível' if self.is_available else 'Ocupado'

    def _update_number(self, instance, value):
        """Atualiza o número do cacifo"""
        self.number_label.text = f'#{value}'

    def on_touch_down(self, touch):
        """Detecta toques no cacifo"""
        if self.collide_point(*touch.pos) and self.is_available:
            # Só permite seleção se estiver disponível
            self.dispatch('on_locker_select', self.locker_number)
            return True
        return super().on_touch_down(touch)

    def on_locker_select(self, locker_number):
        """Evento disparado quando cacifo é selecionado"""
        print(f"Cacifo {locker_number} selecionado!")


class BaseScreen(BoxLayout):
    def __init__(self, manager, title="Screen Title", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.bg_color = (255/255, 255/255, 255/255, 1)
        self.manager = manager
        
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size) # No radius for inner screens
        self.bind(pos=self._update_rect, size=self._update_rect)

        # Header for internal screens
        header = BoxLayout(size_hint_y=None, height=dp(60), padding=[dp(10), dp(10), dp(10), dp(10)], spacing=dp(10)) # Left, Bottom, Right, Top
        header.bg_color = (0/255, 77/255, 122/255, 1) # Dark blue header
        with header.canvas.before:
            Color(*header.bg_color)
            header.rect = RoundedRectangle(pos=header.pos, size=header.size)
        header.bind(pos=self._update_header_rect, size=self._update_header_rect)

        back_button = Button(text='[b]< Back[/b]', markup=True, size_hint_x=None, width=dp(100), font_size='16sp', background_normal='', background_color=(0,0,0,0), color=(1,1,1,1))
        back_button.bind(on_release=self.go_back)
        header.add_widget(back_button)
        header.add_widget(Label(text=f'[b]{title}[/b]', markup=True, font_size='22sp', color=(1,1,1,1), valign='middle', halign='center'))
        header.add_widget(BoxLayout(size_hint_x=None, width=dp(100))) # Spacer for alignment

        self.add_widget(header)

        # Main content area for specific screens
        self.content_area = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))
        self.add_widget(self.content_area)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _update_header_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def go_back(self, instance):
        print(f"Going back from {self.manager.current}")
        self.manager.current = 'home' # Always go back to the home screen


class FindLockersScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(manager, title="Find Available Lockers", **kwargs)
        
        # Container para centralizar o grid
        grid_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(320)  # Altura suficiente para 2 linhas de cacifos
        )
        
        # Espaçador esquerdo
        grid_container.add_widget(BoxLayout())
        
        # Grid para os cacifos (2 colunas, 2 linhas)
        lockers_grid = GridLayout(
            cols=2, 
            rows=2,
            spacing=dp(20), 
            size_hint=(None, None),
            size=(dp(260), dp(320))  # Largura e altura fixas
        )
        
        # Cria alguns cacifos de exemplo
        # Cacifo 1 - Disponível (verde)
        locker1 = LockerBox(locker_number='001', is_available=True)
        locker1.bind(on_locker_select=self.on_locker_selected)
        lockers_grid.add_widget(locker1)
        
        # Cacifo 2 - Disponível (verde) 
        locker2 = LockerBox(locker_number='002', is_available=True)
        locker2.bind(on_locker_select=self.on_locker_selected)
        lockers_grid.add_widget(locker2)
        
        # Cacifo 3 - Indisponível (vermelho) para mostrar a diferença
        locker3 = LockerBox(locker_number='003', is_available=False)
        locker3.bind(on_locker_select=self.on_locker_selected)
        lockers_grid.add_widget(locker3)
        
        # Cacifo 4 - Disponível (verde)
        locker4 = LockerBox(locker_number='004', is_available=True)
        locker4.bind(on_locker_select=self.on_locker_selected)
        lockers_grid.add_widget(locker4)
        
        grid_container.add_widget(lockers_grid)
        
        # Espaçador direito
        grid_container.add_widget(BoxLayout())
        
        self.content_area.add_widget(grid_container)
        
        # Espaçador antes das instruções
        self.content_area.add_widget(BoxLayout(size_hint_y=None, height=dp(30)))
        
        # Instruções
        instructions_label = Label(
            text="Cacifos verdes estão disponíveis. Toque num cacifo para selecioná-lo.",
            font_size='14sp',
            halign='center',
            valign='middle',
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None,
            height=dp(40)
        )
        instructions_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        self.content_area.add_widget(instructions_label)
        
        # Espaçador final flexível
        self.content_area.add_widget(BoxLayout())

    def on_locker_selected(self, instance, locker_number):
        """Callback quando um cacifo é selecionado"""
        print(f"Utilizador selecionou o cacifo #{locker_number}")
        # Aqui você pode adicionar lógica para proceder com a reserva


class UnlockLockerScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(manager, title="Unlock Locker", **kwargs)
        self.content_area.add_widget(Label(text="[b]Enter your booking code or tap your RFID card.[/b]", markup=True, font_size='24sp', halign='center', valign='middle', color=(0.2,0.2,0.2,1)))
        self.content_area.add_widget(Label(text="This is where RFID integration would happen!", font_size='16sp', halign='center', valign='top', color=(0.4,0.4,0.4,1)))
        # Add a TextInput for booking code, or an animated prompt for RFID tap.