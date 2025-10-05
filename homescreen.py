import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle # For custom drawing
from kivy.core.text import LabelBase
LabelBase.register(name="FontAwesome", fn_regular="fa-solid-900.ttf.otf") # Ensure you have the FontAwesome font file in the same directory


class KioskHeader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = [dp(20), dp(20), dp(20), dp(20)] # Left, Bottom, Right, Top
        self.spacing = dp(15)
        self.bg_color = (0/255, 70/255, 122/255, 1) # Dark blue

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(0), dp(0), dp(15), dp(15)])
        self.bind(pos=self._update_rect, size=self._update_rect)

        # Check if logo.png exists, otherwise use a placeholder text
        try:
            with open('logo.png', 'rb') as f: pass
            logo_widget = Image(source='logo.png', size_hint=(None, None), size=(dp(40), dp(40)))
        except FileNotFoundError:
            logo_widget = Label(text='[b]LS[/b]', markup=True, font_size='24sp', color=(255,1,1,1), size_hint_y=None, height=(dp(40)))

        self.add_widget(logo_widget)
        self.add_widget(Label(text='[b]Luggage Storage auto[/b]', markup=True, font_size='30sp', color=(255/255, 255/255, 255/255, 1), size_hint_y=None, height=dp(40), valign='middle'))
        self.add_widget(BoxLayout(size_hint_x=0.06)) # Spacer

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class OptionCard(Button):
    icon_char = StringProperty('') # Using char code as Kivy Label needs a font that supports it
    title_text = StringProperty('')
    description_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = '' # No default background image
        self.background_color = (0,0,0,0) # Make button itself transparent for custom drawing
        self.color = (0.2, 0.2, 0.2, 1) # Dark text
        self.size_hint_y = None
        self.height = dp(150)
        self.padding = dp(20)
        
        self.border_radius = [dp(12)]
        self.card_color = (1, 204/255, 0, 1) # Bright yellow

        with self.canvas.before:
            # Shadow effect
            Color(0,0,0,0.1) # Shadow color
            self.shadow_rect = RoundedRectangle(size=(self.width-dp(10), self.height-dp(10)), pos=(self.x+dp(5), self.y+dp(5)), radius=self.border_radius)
            # Main card background
            Color(*self.card_color)
            self.card_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=self.border_radius)
        self.bind(pos=self._update_canvas, size=self._update_canvas)

        # Initialize Labels
        self.icon_label = Label(
            text=self.icon_char,
            font_size='50sp',
            color=(0/255, 77/255, 122/255, 1),
            markup=True,
            size_hint_x=None,
            width=dp(80),
            halign='center',
            valign='middle'
        )
        
        self.title_label = Label(
            text=f'[b]{self.title_text}[/b]',
            markup=True,
            font_size='22sp',
            color=(0.2, 0.2, 0.2, 1),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(40)
        )
        
        self.description_label = Label(
            text=self.description_text,
            markup=True,
            font_size='14sp',
            color=(0.4, 0.4, 0.4, 1),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=dp(60)
        )

        # Layout principal horizontal
        content_layout = BoxLayout(
            orientation='horizontal',
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Layout vertical para título e descrição
        text_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5)
        )
        
        # Adiciona os widgets aos layouts
        text_layout.add_widget(self.title_label)
        text_layout.add_widget(self.description_label)
        
        content_layout.add_widget(self.icon_label)
        content_layout.add_widget(text_layout)

        self.add_widget(content_layout)

        # Bind size changes to update description_label and title_label text_size for proper wrapping
        self.bind(size=self._update_text_size)

        # Bind property changes to update label texts
        self.bind(icon_char=self._update_icon_text)
        self.bind(title_text=self._update_title_text)
        self.bind(description_text=self._update_description_text)

    def _update_icon_text(self, instance, value):
        self.icon_label.text = value

    def _update_title_text(self, instance, value):
        self.title_label.text = f'[b]{value}[/b]'

    def _update_description_text(self, instance, value):
        self.description_label.text = value

    def _update_text_size(self, instance, value):
        # Encontra o layout de texto (parent do title_label)
        text_layout = self.title_label.parent
        if not text_layout:
            return

        # Calcula largura disponível
        padding = text_layout.padding if hasattr(text_layout, 'padding') else [0, 0, 0, 0]
        available_width = text_layout.width - (padding[0] + padding[2])
        
        # Define text_size para permitir quebra de linha horizontal
        if available_width > 0:
            self.title_label.text_size = (available_width, None)
            self.description_label.text_size = (available_width, None)
            
            # Debug info
            print(f"DEBUG: Text layout width: {text_layout.width}")
            print(f"DEBUG: Available width for text: {available_width}")
            print(f"DEBUG: Title text size: {self.title_label.text_size}")
            print(f"DEBUG: Description text size: {self.description_label.text_size}")

    def _update_canvas(self, instance, value):
        # Update positions and sizes of the custom drawn rectangles
        
        self.shadow_rect.pos = (self.x + dp(5), self.y + dp(5))
        self.shadow_rect.size = (self.width - dp(10), self.height - dp(10))
        self.card_rect.pos = self.pos
        self.card_rect.size = self.size

    # Handle hover/press effects
    def on_enter(self): # Kivy doesn't have direct hover, usually relies on touch/mouse events
        pass # For mouse, you'd bind to Window.bind(mouse_pos)

    def on_press(self):
        self.card_color = (1, 221/255, 51/255, 1) # Lighter yellow on press
        self._update_canvas(self, None)

    def on_release(self):
        self.card_color = (1, 204/255, 0, 1) # Back to original color
        self._update_canvas(self, None)


class KioskFooter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = dp(15)
        self.spacing = dp(8)
        self.bg_color = (240/255, 242/255, 245/255, 1) # Light grey

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15), dp(15), dp(0), dp(0)])
        self.bind(pos=self._update_rect, size=self._update_rect)

        self.add_widget(Label(text='Select Language:', font_size='14sp', color=(0.4, 0.4, 0.4, 1), size_hint_x=None, width=dp(120), valign='middle', halign='left'))
        
        # Placeholder for flag images or buttons
        # In a real app, these would be Image widgets with actual flag sources
        flags_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_x=None, width=dp(180))
        for flag_code in ['gb', 'fr', 'de', 'es', 'it']:
            # Using a Label as a placeholder for an image to avoid needing actual flag files for this demo
            flags_layout.add_widget(Label(text=flag_code.upper(), size_hint_x=None, width=dp(30), font_size='12sp', color=(0.4,0.4,0.4,1)))
        self.add_widget(flags_layout)
        self.add_widget(BoxLayout()) # Spacer

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class KioskHomeScreen(BoxLayout):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.bg_color = (255/255, 255/255, 255/255, 1)
        self.manager = manager # Reference to the ScreenManager

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
        self.bind(pos=self._update_rect, size=self._update_rect)

        self.add_widget(KioskHeader())

        self.add_widget(BoxLayout(size_hint_y=None, height=dp(80)))  # Spacer between header and welcome label

        main_content = BoxLayout(orientation='vertical', padding=[dp(40), dp(20), dp(40), dp(40)], spacing=dp(50))
        welcome_label = Label(text='[b]Welcome! How can we help you?[/b]', markup=True, font_size='30sp', color=(0/255, 77/255, 122/255, 1), size_hint_y=None, height=dp(80), halign='center', valign='middle')
        welcome_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        main_content.add_widget(welcome_label)

        main_content.add_widget(BoxLayout(size_hint_y=None, height=dp(40)))  # Spacer between welcome label and boxes

        options_grid = GridLayout(cols=2, spacing=dp(30), size_hint_y=None, height=dp(200))
        
        find_lockers_btn = OptionCard(
            icon_char='\uf002',  # FontAwesome search icon
            title_text='Find available lockers',
            description_text='Book a new locker for your bags.'
        )
        find_lockers_btn.bind(on_release=self.go_to_find_lockers)
        options_grid.add_widget(find_lockers_btn)

        unlock_locker_btn = OptionCard(
            icon_char='\uf09c',  # FontAwesome unlock icon
            title_text='Unlock locker',
            description_text='Access your booked locker.'
        )
        unlock_locker_btn.bind(on_release=self.go_to_unlock_locker)
        options_grid.add_widget(unlock_locker_btn)
        

        main_content.add_widget(options_grid)
        main_content.add_widget(BoxLayout(size_hint_y=None, height=dp(50))) # Um es# Spacer to push grid up

        self.add_widget(main_content)
        self.add_widget(KioskFooter())

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def go_to_find_lockers(self, instance):
        print("Navigating to Find Lockers screen.")
        self.manager.current = 'find_lockers'

    def go_to_unlock_locker(self, instance):
        print("Navigating to Unlock Locker screen.")
        self.manager.current = 'unlock_locker'

# For icon display: Kivy's default font (Roboto) often includes FontAwesome glyphs.
# If not, you might need to register FontAwesome.ttf:
# from kivy.core.text import LabelBase
# LabelBase.register(name="FontAwesome", fn_regular="path/to/fontawesome-free-solid-900.ttf")
# And then use '[font=FontAwesome]\uf002[/font]'