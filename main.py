import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.core.text import LabelBase
from kivy.uix.label import Label  # Import Label for title and description
from kivy.uix.boxlayout import BoxLayout  # Import BoxLayout for content layout
from kivy.graphics import Color, RoundedRectangle  # Import Color and RoundedRectangle for custom drawing
from kivy.uix.gridlayout import GridLayout  # Import GridLayout for options layout

# Import your screen definitions
from homescreen import KioskHomeScreen, OptionCard  # Import OptionCard here
from lockerscreens import FindLockersScreen, UnlockLockerScreen
LabelBase.register(name="FontAwesome", fn_regular="fa-solid-900.ttf.otf")
# Optional: Set window size for desktop testing. Comment out for actual Pi full screen.
# Window.size = (800, 600)
# Window.fullscreen = 'auto' # Uncomment this for full screen on Pi

class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Definir as propriedades title_text e description_text
        self.title_text = "Default Title"  # Substitua pelo valor desejado
        self.description_text = "Default Description"  # Substitua pelo valor desejado

        # Adicione as telas e widgets como antes
        home_screen = Screen(name='home')
        home_screen.add_widget(KioskHomeScreen(manager=self))  # Pass manager for navigation
        self.add_widget(home_screen)

        find_lockers_screen = Screen(name='find_lockers')
        find_lockers_screen.add_widget(FindLockersScreen(manager=self))
        self.add_widget(find_lockers_screen)

        unlock_locker_screen = Screen(name='unlock_locker')
        unlock_locker_screen.add_widget(UnlockLockerScreen(manager=self))
        self.add_widget(unlock_locker_screen)

        # Criar o botão find_lockers_btn
        find_lockers_btn = OptionCard(
            icon_char='[font=FontAwesome][b]\uf002[/b][/font]',  # Ícone de busca
            title_text='Find available lockers',
            description_text='Book a new locker for your bags.',
            size_hint_x=1  # Definindo size_hint_x como 1 aqui
        )

        # DEBUG: forçar e inspecionar após criação
        find_lockers_btn.title_text = 'Find available lockers'
        find_lockers_btn.description_text = 'Book a new locker for your bags.'
        print("MAIN DEBUG: find_lockers_btn.title_text =", repr(find_lockers_btn.title_text),
              " label_text =", repr(getattr(find_lockers_btn, 'title_label').text if hasattr(find_lockers_btn, 'title_label') else None))

        # Criar o GridLayout para os botões
        options_grid = GridLayout(cols=2, spacing=dp(30), size_hint_y=None, height=dp(200))
        options_grid.add_widget(find_lockers_btn)

        # Encapsular o GridLayout em um Screen
        options_screen = Screen(name='options_screen')
        options_screen.add_widget(options_grid)

        # Adicionar o Screen ao ScreenManager
        self.add_widget(options_screen)

    def _update_icon_text(self, instance, value):
        self.icon_label.text = value

    def _update_title_text(self, instance, value):
        self.title_label.text = f'[b]{value}[/b]'

    def _update_description_text(self, instance, value):
        self.description_label.text = value

class LuggageKioskApp(App):
    def build(self):
        # Set default font to ensure icons render if you have a compatible font
        # You'd ideally install a FontAwesome .ttf and load it here.
        # For now, relying on system default for testing.
        # from kivy.core.text import LabelBase
        # LabelBase.register(name="FontAwesome", fn_regular="path/to/fontawesome-free-solid-900.ttf")

        return MainScreenManager()

if __name__ == '__main__':
    LuggageKioskApp().run()