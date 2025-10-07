from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.image import Image
import random

class ContactPinHeader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = [dp(20), dp(20), dp(20), dp(20)]
        self.spacing = dp(15)
        self.bg_color = (0/255, 70/255, 122/255, 1)  # Dark blue

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(0), dp(0), dp(15), dp(15)])
        self.bind(pos=self._update_rect, size=self._update_rect)

        # Logo
        try:
            with open('logo.png', 'rb') as f: pass
            logo_widget = Image(source='logo.png', size_hint=(None, None), size=(dp(40), dp(40)))
        except FileNotFoundError:
            logo_widget = Label(text='[b]LS[/b]', markup=True, font_size='24sp', color=(255,1,1,1), size_hint_y=None, height=(dp(40)))

        self.add_widget(logo_widget)
        self.add_widget(Label(text='[b]Luggage Storage auto[/b]', markup=True, font_size='30sp', color=(255/255, 255/255, 255/255, 1), size_hint_y=None, height=dp(40), valign='middle'))
        self.add_widget(BoxLayout(size_hint_x=0.06))

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ContactPinFooter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = dp(15)
        self.spacing = dp(8)
        self.bg_color = (240/255, 242/255, 245/255, 1)

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15), dp(15), dp(0), dp(0)])
        self.bind(pos=self._update_rect, size=self._update_rect)

        self.add_widget(Label(text='Select Language:', font_size='14sp', color=(0.4, 0.4, 0.4, 1), size_hint_x=None, width=dp(120), valign='middle', halign='left'))
        
        flags_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_x=None, width=dp(180))
        for flag_code in ['gb', 'fr', 'de', 'es', 'it']:
            flags_layout.add_widget(Label(text=flag_code.upper(), size_hint_x=None, width=dp(30), font_size='12sp', color=(0.4,0.4,0.4,1)))
        self.add_widget(flags_layout)
        self.add_widget(BoxLayout())

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class StyledButton(Button):
    def __init__(self, text, button_type='primary', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint_y = None
        self.height = dp(50)
        self.border_radius = [dp(8)]
        
        if button_type == 'primary':
            self.bg_color = (1, 204/255, 0, 1)  # Yellow like the cards
            self.text_color = (0/255, 77/255, 122/255, 1)  # Dark blue text
        else:  # secondary
            self.bg_color = (240/255, 242/255, 245/255, 1)  # Light grey
            self.text_color = (0.4, 0.4, 0.4, 1)  # Grey text
        
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.border_radius)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        self.color = self.text_color
        self.background_color = (0, 0, 0, 0)  # Transparent to use custom background

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ContactPinScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Header azul
        main_layout.add_widget(ContactPinHeader())
        
        # Área branca principal - aqui é onde tudo vai ficar
        white_area = BoxLayout(orientation='vertical', padding=[dp(40), dp(40), dp(40), dp(20)])
        
        # Adicionar fundo branco à área principal
        with white_area.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            white_area.bg_rect = RoundedRectangle(pos=white_area.pos, size=white_area.size, radius=[0])
        white_area.bind(pos=lambda instance, value: setattr(white_area.bg_rect, 'pos', white_area.pos))
        white_area.bind(size=lambda instance, value: setattr(white_area.bg_rect, 'size', white_area.size))
        
        # Título
        title = Label(
            text='[b]Book Your Locker[/b]',
            markup=True,
            font_size='32sp',
            color=(0/255, 77/255, 122/255, 1),
            size_hint_y=None,
            height=dp(60),
            halign='center'
        )
        title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        white_area.add_widget(title)
        
        # Espaçador
        white_area.add_widget(BoxLayout(size_hint_y=None, height=dp(40)))
        
        # "Contacto:" encostado à esquerda
        contact_title = Label(
            text='Contacto:',
            font_size='18sp',
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        contact_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        white_area.add_widget(contact_title)
        
        # Input do contacto logo embaixo
        self.contact_input = TextInput(
            hint_text='exemplo@email.com ou +351 123 456 789',
            multiline=False,
            font_size='16sp',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        white_area.add_widget(self.contact_input)
        
        # Espaçador
        white_area.add_widget(BoxLayout(size_hint_y=None, height=dp(30)))
        
        # PIN section
        self.generated_pin = f"{random.randint(1000, 9999)}"
        
        pin_label = Label(
            text='Your PIN has been generated:',
            font_size='18sp',
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='center'
        )
        pin_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        white_area.add_widget(pin_label)
        
        # Container do PIN
        pin_container = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80), padding=dp(10))
        with pin_container.canvas.before:
            Color(1, 204/255, 0, 1)
            pin_container.rect = RoundedRectangle(pos=pin_container.pos, size=pin_container.size, radius=[dp(12)])
        pin_container.bind(pos=lambda instance, value: setattr(pin_container.rect, 'pos', pin_container.pos))
        pin_container.bind(size=lambda instance, value: setattr(pin_container.rect, 'size', pin_container.size))
        
        pin_display = Label(
            text=f'[b]{self.generated_pin}[/b]',
            markup=True,
            font_size='36sp',
            color=(0/255, 77/255, 122/255, 1),
            halign='center',
            valign='middle'
        )
        pin_container.add_widget(pin_display)
        white_area.add_widget(pin_container)
        
        # Instrução
        instruction = Label(
            text='Please note this PIN. You will need it to access your locker.',
            font_size='16sp',
            size_hint_y=None,
            height=dp(40),
            color=(0.4, 0.4, 0.4, 1),
            halign='center'
        )
        instruction.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        white_area.add_widget(instruction)
        
        # Espaçador flexível
        white_area.add_widget(BoxLayout())
        
        # Botões
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(50))
        
        back_button = StyledButton('Back', button_type='secondary', size_hint_x=0.5)
        back_button.bind(on_press=self.go_back)
        
        confirm_button = StyledButton('Confirm Booking', button_type='primary', size_hint_x=0.5)
        confirm_button.bind(on_press=self.confirm_booking)
        
        button_layout.add_widget(back_button)
        button_layout.add_widget(confirm_button)
        white_area.add_widget(button_layout)
        
        # Adicionar área branca ao layout principal
        main_layout.add_widget(white_area)
        
        # Footer
        main_layout.add_widget(ContactPinFooter())
        
        self.add_widget(main_layout)

    def confirm_booking(self, instance):
        contact = self.contact_input.text
        if not contact.strip():
            print("Please enter a contact")
            return
            
        pin = self.generated_pin
        print(f'Booking confirmed - Contact: {contact}, PIN: {pin}')
        
        if self.manager:
            self.manager.current = 'home'

    def go_back(self, instance):
        if self.manager:
            self.manager.current = 'find_lockers'