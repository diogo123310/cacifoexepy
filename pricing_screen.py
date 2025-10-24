from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
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


class PricingHeader(BoxLayout):
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


class PriceCard(BoxLayout):
    def __init__(self, duration, prices, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(20), dp(10), dp(20), dp(10)]
        self.spacing = dp(10)
        
        # Background color alternado para melhor leitura
        self.bg_color = (249/255, 249/255, 249/255, 1)  # Very light grey
        
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Duration label
        duration_label = Label(
            text=duration,
            font_size='16sp',
            color=(0/255, 77/255, 122/255, 1),
            size_hint_x=0.2,
            halign='left',
            valign='middle'
        )
        duration_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        self.add_widget(duration_label)
        
        # Price columns
        for price in prices:
            price_label = Label(
                text=price,
                font_size='16sp',
                color=(0/255, 77/255, 122/255, 1),
                size_hint_x=0.266,
                halign='center',
                valign='middle'
            )
            price_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            self.add_widget(price_label)
    
    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class PricingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Header azul
        self.header = PricingHeader()
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
            text=f'[b]{translator.get_text("pricing_title")}[/b]',
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
            text=translator.get_text("pricing_subtitle"),
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
        
        # Header da tabela
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), padding=[dp(20), dp(15), dp(20), dp(15)])
        header_layout.canvas.before.clear()
        with header_layout.canvas.before:
            Color(0/255, 77/255, 122/255, 1)  # Dark blue
            header_layout.bg_rect = RoundedRectangle(pos=header_layout.pos, size=header_layout.size, radius=[dp(8), dp(8), dp(0), dp(0)])
        header_layout.bind(pos=lambda instance, value: setattr(header_layout.bg_rect, 'pos', header_layout.pos))
        header_layout.bind(size=lambda instance, value: setattr(header_layout.bg_rect, 'size', header_layout.size))
        
        # Header labels
        duration_header = Label(
            text='[b]DURATION[/b]',
            markup=True,
            font_size='16sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.2,
            halign='left'
        )
        duration_header.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        header_layout.add_widget(duration_header)
        
        maxi_header = Label(
            text='[b]MAXI[/b]',
            markup=True,
            font_size='16sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.266,
            halign='center'
        )
        maxi_header.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        header_layout.add_widget(maxi_header)
        
        standard_header = Label(
            text='[b]STANDARD[/b]',
            markup=True,
            font_size='16sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.266,
            halign='center'
        )
        standard_header.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        header_layout.add_widget(standard_header)
        
        small_header = Label(
            text='[b]SMALL[/b]',
            markup=True,
            font_size='16sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.266,
            halign='center'
        )
        small_header.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        header_layout.add_widget(small_header)
        
        white_area.add_widget(header_layout)
        
        # Container para as linhas de preços
        prices_container = BoxLayout(orientation='vertical', size_hint_y=None)
        prices_container.bind(minimum_height=prices_container.setter('height'))
        
        # Dados dos preços baseados na imagem
        price_data = [
            ('1 hour', ['3,49 €', '2,49 €', '1,49 €']),
            ('2 hours', ['7,99 €', '4,99 €', '3,49 €']),
            ('3 hours', ['11,99 €', '6,99 €', '4,99 €']),
            ('4 hours', ['15,99 €', '8,99 €', '5,99 €']),
            ('5 hours', ['17,99 €', '10,99 €', '6,99 €']),
            ('6 hours', ['19,99 €', '12,99 €', '7,99 €']),
            ('7 hours', ['20,99 €', '13,99 €', '8,99 €']),
            ('1 day', ['22,99 €', '15,99 €', '10,99 €']),
            ('2 days', ['34,49 €', '23,49 €', '16,49 €']),
            ('3 days', ['48,49 €', '32,49 €', '23,49 €']),
            ('4 days', ['62,99 €', '41,49 €', '30,49 €']),
        ]
        
        # Criar linhas de preços
        for i, (duration, prices) in enumerate(price_data):
            # Alternar cor de fundo
            if i % 2 == 0:
                price_card = PriceCard(duration, prices)
                price_card.bg_color = (255/255, 255/255, 255/255, 1)  # White
            else:
                price_card = PriceCard(duration, prices)
                price_card.bg_color = (249/255, 249/255, 249/255, 1)  # Very light grey
            
            prices_container.add_widget(price_card)
        
        white_area.add_widget(prices_container)
        
        # Espaçador flexível
        white_area.add_widget(Widget())
        
        # Botão voltar
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        button_layout.add_widget(Widget())  # Spacer esquerdo
        
        self.back_button = StyledButton(translator.get_text("back_button"), button_type='secondary', size_hint_x=None, width=dp(200))
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
        self.title_label.text = f'[b]{translator.get_text("pricing_title")}[/b]'
        self.subtitle_label.text = translator.get_text("pricing_subtitle")
        
        # Update button text
        if hasattr(self, 'back_button'):
            self.back_button.text = translator.get_text("back_button")