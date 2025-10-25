from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from translations import translator


class ImageButton(ButtonBehavior, Image):
    """Botão clicável que usa uma imagem"""
    pass


class HowItWorksHeader(BoxLayout):
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
        self.title_label = Label(text=f'[b]{translator.get_text("app_title")}[/b]', markup=True, font_size='30sp', color=(255/255, 255/255, 255/255, 1), size_hint_y=None, height=dp(40), valign='middle')
        self.add_widget(self.title_label)
        self.add_widget(Widget(size_hint_x=0.06))
    
    def update_translations(self):
        """Update translatable text"""
        self.title_label.text = f'[b]{translator.get_text("app_title")}[/b]'

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
            self.bg_color = (1, 204/255, 0, 1)  # Yellow
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


class StepCard(BoxLayout):
    def __init__(self, step_number, step_title, step_description, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(200)
        self.padding = [dp(20), dp(20), dp(20), dp(20)]
        self.spacing = dp(15)
        
        # Background with rounded corners
        self.bg_color = (255/255, 255/255, 255/255, 1)  # White background
        self.border_color = (240/255, 242/255, 245/255, 1)  # Light grey border
        
        with self.canvas.before:
            # Border
            Color(*self.border_color)
            self.border_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            # Background
            Color(*self.bg_color)
            self.bg_rect = RoundedRectangle(
                pos=(self.x + dp(2), self.y + dp(2)), 
                size=(self.width - dp(4), self.height - dp(4)), 
                radius=[dp(8)]
            )
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Step number circle
        step_number_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        step_number_layout.add_widget(Widget())  # Left spacer
        
        step_circle = Label(
            text=f'[b]{step_number}[/b]',
            markup=True,
            font_size='24sp',
            color=(1, 1, 1, 1),  # White text
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            halign='center',
            valign='middle'
        )
        
        # Add circle background
        with step_circle.canvas.before:
            Color(1, 204/255, 0, 1)  # Yellow background
            step_circle.circle = RoundedRectangle(
                pos=step_circle.pos, 
                size=step_circle.size, 
                radius=[dp(20)]
            )
        step_circle.bind(pos=lambda instance, value: setattr(step_circle.circle, 'pos', step_circle.pos))
        step_circle.bind(size=lambda instance, value: setattr(step_circle.circle, 'size', step_circle.size))
        step_circle.bind(size=lambda instance, value: setattr(instance, 'text_size', step_circle.size))
        
        step_number_layout.add_widget(step_circle)
        step_number_layout.add_widget(Widget())  # Right spacer
        self.add_widget(step_number_layout)
        
        # Step title
        self.step_title_label = Label(
            text=f'[b]{step_title}[/b]',
            markup=True,
            font_size='20sp',
            color=(0/255, 77/255, 122/255, 1),
            size_hint_y=None,
            height=dp(30),
            halign='center',
            valign='middle'
        )
        self.step_title_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        self.add_widget(self.step_title_label)
        
        # Step description
        self.step_description_label = Label(
            text=step_description,
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1),
            halign='center',
            valign='top',
            text_size=(None, None)
        )
        self.step_description_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        self.add_widget(self.step_description_label)
    
    def _update_rect(self, instance, value):
        self.border_rect.pos = self.pos
        self.border_rect.size = self.size
        self.bg_rect.pos = (self.x + dp(2), self.y + dp(2))
        self.bg_rect.size = (self.width - dp(4), self.height - dp(4))
    
    def update_content(self, step_title, step_description):
        """Update step content for translations"""
        self.step_title_label.text = f'[b]{step_title}[/b]'
        self.step_description_label.text = step_description


class HowItWorksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Header azul
        self.header = HowItWorksHeader()
        main_layout.add_widget(self.header)
        
        # Área branca principal
        white_area = BoxLayout(orientation='vertical', padding=[dp(40), dp(40), dp(40), dp(20)])
        
        # Adicionar fundo branco à área principal
        with white_area.canvas.before:
            Color(1, 1, 1, 1)  # White background
            white_area.bg_rect = Rectangle(pos=white_area.pos, size=white_area.size)
        
        white_area.bind(pos=lambda instance, value: setattr(white_area.bg_rect, 'pos', white_area.pos))
        white_area.bind(size=lambda instance, value: setattr(white_area.bg_rect, 'size', white_area.size))
        
        # Título principal
        self.title_label = Label(
            text=f'[b]{translator.get_text("how_it_works_title")}[/b]',
            markup=True,
            font_size='34sp',
            size_hint_y=None,
            height=dp(50),
            color=(0/255, 77/255, 122/255, 1),
            halign='center'
        )
        self.title_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        white_area.add_widget(self.title_label)
        
        # Subtitle
        self.subtitle_label = Label(
            text=translator.get_text("how_it_works_subtitle"),
            font_size='18sp',
            size_hint_y=None,
            height=dp(40),
            color=(0.4, 0.4, 0.4, 1),
            halign='center'
        )
        self.subtitle_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        white_area.add_widget(self.subtitle_label)
        
        # Espaçador
        white_area.add_widget(Widget(size_hint_y=None, height=dp(30)))
        
        # Container para os passos
        steps_container = BoxLayout(orientation='vertical', spacing=dp(20), size_hint_y=None)
        steps_container.bind(minimum_height=steps_container.setter('height'))
        
        # Step 1: Book your locker
        self.step1_card = StepCard(
            step_number="1",
            step_title=translator.get_text("step1_title"),
            step_description=translator.get_text("step1_description")
        )
        steps_container.add_widget(self.step1_card)
        
        # Step 2: Deposit your baggage
        self.step2_card = StepCard(
            step_number="2",
            step_title=translator.get_text("step2_title"),
            step_description=translator.get_text("step2_description")
        )
        steps_container.add_widget(self.step2_card)
        
        # Step 3: Reopen and retrieve your baggage
        self.step3_card = StepCard(
            step_number="3",
            step_title=translator.get_text("step3_title"),
            step_description=translator.get_text("step3_description")
        )
        steps_container.add_widget(self.step3_card)
        
        white_area.add_widget(steps_container)
        
        # Espaçador flexível
        white_area.add_widget(Widget())
        
        # Botão voltar
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        button_layout.add_widget(Widget())  # Spacer esquerdo
        
        self.back_button = StyledButton(translator.get_text("back_button"), button_type='primary', size_hint_x=None, width=dp(200))
        self.back_button.bind(on_press=self.go_back)
        button_layout.add_widget(self.back_button)
        
        button_layout.add_widget(Widget())  # Spacer direito
        white_area.add_widget(button_layout)
        
        # Adicionar área branca ao layout principal
        main_layout.add_widget(white_area)
        
        self.add_widget(main_layout)

    def go_back(self, instance):
        """Voltar à tela principal"""
        self.manager.current = 'home'
    
    def update_translations(self):
        """Update all translatable text elements"""
        self.header.update_translations()
        self.title_label.text = f'[b]{translator.get_text("how_it_works_title")}[/b]'
        self.subtitle_label.text = translator.get_text("how_it_works_subtitle")
        
        # Update step cards
        self.step1_card.update_content(
            translator.get_text("step1_title"),
            translator.get_text("step1_description")
        )
        self.step2_card.update_content(
            translator.get_text("step2_title"),
            translator.get_text("step2_description")
        )
        self.step3_card.update_content(
            translator.get_text("step3_title"),
            translator.get_text("step3_description")
        )
        
        # Update button text
        if hasattr(self, 'back_button'):
            self.back_button.text = translator.get_text("back_button")