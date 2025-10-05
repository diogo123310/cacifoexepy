import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

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
        self.content_area.add_widget(Label(text="[b]Locker Selection and Booking goes here![/b]", markup=True, font_size='24sp', halign='center', valign='middle', color=(0.2,0.2,0.2,1)))
        self.content_area.add_widget(Label(text="You would see a map or a list of lockers, sizes, and pricing.", font_size='16sp', halign='center', valign='top', color=(0.4,0.4,0.4,1)))
        # Add widgets for actual locker selection, dates, times, etc.


class UnlockLockerScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        super().__init__(manager, title="Unlock Locker", **kwargs)
        self.content_area.add_widget(Label(text="[b]Enter your booking code or tap your RFID card.[/b]", markup=True, font_size='24sp', halign='center', valign='middle', color=(0.2,0.2,0.2,1)))
        self.content_area.add_widget(Label(text="This is where RFID integration would happen!", font_size='16sp', halign='center', valign='top', color=(0.4,0.4,0.4,1)))
        # Add a TextInput for booking code, or an animated prompt for RFID tap.