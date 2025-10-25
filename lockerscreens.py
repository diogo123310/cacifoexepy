import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from translations import translator
from datetime import datetime


class StyledButton(Button):
    def __init__(self, text, button_type='primary', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint_y = None
        self.height = dp(60)
        self.border_radius = [dp(8)]
        
        if button_type == 'primary':
            self.bg_color = (1, 204/255, 0, 1)  # Yellow
            self.text_color = (0/255, 77/255, 122/255, 1)  # Dark blue text
        else:  # secondary
            self.bg_color = (0/255, 77/255, 122/255, 1)  # Blue
            self.text_color = (1, 1, 1, 1)  # White text


class ProfessionalCard(BoxLayout):
    """Professional card container with shadow and rounded corners"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.padding = [dp(25), dp(20)]
        self.spacing = dp(20)
        
        # Add card background with shadow effect
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray shadow
            self.shadow_rect = RoundedRectangle(
                pos=(self.x + dp(2), self.y - dp(2)), 
                size=self.size, 
                radius=[dp(12)]
            )
            Color(1, 1, 1, 1)  # White card background
            self.card_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_graphics(self, *args):
        self.shadow_rect.pos = (self.x + dp(2), self.y - dp(2))
        self.shadow_rect.size = self.size
        self.card_rect.pos = self.pos
        self.card_rect.size = self.size


class IconTextField(BoxLayout):
    """Professional text field with FontAwesome icon"""
    def __init__(self, icon_unicode="", hint_text="", is_password=False, input_filter=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = dp(12)
        
        # Icon container with blue background
        icon_container = BoxLayout(size_hint_x=None, width=dp(50))
        with icon_container.canvas.before:
            Color(0/255, 77/255, 122/255, 1)  # Blue background
            self.icon_bg = RoundedRectangle(pos=icon_container.pos, size=icon_container.size, radius=[dp(8)])
        icon_container.bind(pos=self._update_icon_bg, size=self._update_icon_bg)
        
        # FontAwesome icon
        icon_label = Label(
            text=f'[font=FontAwesome]{icon_unicode}[/font]',
            markup=True,
            font_size=sp(20),
            color=(1, 1, 1, 1),  # White text
            halign='center',
            valign='middle'
        )
        icon_container.add_widget(icon_label)
        self.add_widget(icon_container)
        
        # Professional text input
        self.text_input = TextInput(
            hint_text=hint_text,
            multiline=False,
            password=is_password,
            font_size=sp(18),
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0/255, 77/255, 122/255, 1),
            cursor_color=(1, 204/255, 0, 1),
            selection_color=(1, 204/255, 0, 0.3),
            padding=[dp(15), dp(12)]
        )
        
        if input_filter:
            self.text_input.input_filter = input_filter
        
        # Add professional border
        with self.text_input.canvas.before:
            Color(200/255, 200/255, 200/255, 1)
            self.text_input.border_rect = RoundedRectangle(
                pos=self.text_input.pos, 
                size=self.text_input.size, 
                radius=[dp(8)]
            )
        
        self.text_input.bind(pos=self._update_border, size=self._update_border)
        self.text_input.bind(focus=self._on_focus_change)
        self.add_widget(self.text_input)
    
    def _update_border(self, *args):
        self.text_input.border_rect.pos = self.text_input.pos
        self.text_input.border_rect.size = self.text_input.size
    
    def _update_icon_bg(self, instance, value):
        self.icon_bg.pos = instance.pos
        self.icon_bg.size = instance.size
    
    def _on_focus_change(self, instance, focus):
        """Change border color based on focus"""
        if focus:
            # Yellow border when focused
            with self.text_input.canvas.before:
                Color(1, 204/255, 0, 1)
                self.text_input.border_rect = RoundedRectangle(
                    pos=self.text_input.pos, 
                    size=self.text_input.size, 
                    radius=[dp(8)]
                )
        else:
            # Gray border when not focused
            with self.text_input.canvas.before:
                Color(200/255, 200/255, 200/255, 1)
                self.text_input.border_rect = RoundedRectangle(
                    pos=self.text_input.pos, 
                    size=self.text_input.size, 
                    radius=[dp(8)]
                )

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class LockerBox(BoxLayout):
    locker_number = StringProperty('')
    locker_status = StringProperty('available')  # 'available', 'door_open', 'occupied'
    
    __events__ = ('on_locker_select',)  # Custom event when locker is selected

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, 1)  # Usar tamanho relativo ao container
        self.padding = dp(15)  # Mais padding para formato quadrado
        self.spacing = dp(8)   # Mais espaçamento interno
        
        # Colors for different states
        self.available_color = (46/255, 204/255, 64/255, 1)  # Green - available
        self.door_open_color = (1, 204/255, 0, 1)  # Yellow - door open
        self.occupied_color = (231/255, 76/255, 60/255, 1)  # Red - occupied

        # Current color based on status
        self.current_color = self._get_color_for_status()
        
        # Locker background
        with self.canvas.before:
            Color(*self.current_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.bind(locker_status=self._update_color)
        
        # Locker number (responsive) - ajustado para formato quadrado
        self.number_label = Label(
            text=f'#{self.locker_number}',
            font_size='30sp',  # Ligeiramente maior para formato quadrado
            size_hint_y=0.65,  # 65% da altura do locker
            color=(1, 1, 1, 1),  # White
            bold=True,
            halign='center',
            valign='middle'
        )
        
        # Locker status (responsive) - ajustado para formato quadrado
        self.status_label = Label(
            text=self._get_status_text(),
            font_size='14sp',  # Ligeiramente maior para melhor legibilidade
            size_hint_y=0.35,  # 35% da altura do locker
            color=(1, 1, 1, 1),  # White
            bold=True,
            halign='center',
            valign='middle'
        )
        
        # Add widgets (without icon)
        self.add_widget(self.number_label)
        self.add_widget(self.status_label)
        
        # Bind for property updates
        self.bind(locker_number=self._update_number)

    def _get_color_for_status(self):
        """Get color based on locker status"""
        if self.locker_status == 'available':
            return self.available_color
        elif self.locker_status == 'door_open':
            return self.door_open_color
        elif self.locker_status == 'occupied':
            return self.occupied_color
        else:
            return self.available_color  # Default

    def _get_status_text(self):
        """Get status text based on locker status"""
        if self.locker_status == 'available':
            return translator.get_text('status_available')
        elif self.locker_status == 'door_open':
            return translator.get_text('status_door_open')
        elif self.locker_status == 'occupied':
            return translator.get_text('status_occupied')
        else:
            return translator.get_text('status_available')  # Default

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _update_color(self, instance, value):
        """Update color based on status"""
        self.current_color = self._get_color_for_status()
        with self.canvas.before:
            Color(*self.current_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        
        # Update status text
        self.status_label.text = self._get_status_text()

    def _update_number(self, instance, value):
        """Update the locker number"""
        self.number_label.text = f'#{value}'

    def on_touch_down(self, touch):
        """Detect touches on the locker"""
        if self.collide_point(*touch.pos) and self.locker_status == 'available':
            # Only allow selection if available
            self.dispatch('on_locker_select', self.locker_number)
            return True
        return super().on_touch_down(touch)

    def on_locker_select(self, locker_number):
        """Event triggered when locker is selected"""
        print(f"Locker {locker_number} selected!")


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

        self.back_button = Button(text=f'[b]< {translator.get_text("back_button")}[/b]', markup=True, size_hint_x=None, width=dp(100), font_size='16sp', background_normal='', background_color=(0,0,0,0), color=(1,1,1,1))
        self.back_button.bind(on_release=self.go_back)
        header.add_widget(self.back_button)
        
        self.title_label = Label(text=f'[b]{title}[/b]', markup=True, font_size='22sp', color=(1,1,1,1), valign='middle', halign='center')
        header.add_widget(self.title_label)
        # Removed problematic spacer that was creating a yellow square

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
        # Remover gpio_controller dos kwargs antes de chamar super()
        self.gpio_controller = kwargs.pop('gpio_controller', None)
        super().__init__(manager, title=translator.get_text("find_lockers_title"), **kwargs)
        
        # Armazenar referências dos cacifos para atualização
        self.locker_widgets = {}
        
        # Referência à base de dados
        self.db = self.gpio_controller.db if self.gpio_controller else None
        
        # Container para centralizar o grid - máximo baixo possível
        grid_container = BoxLayout(
            orientation='vertical',
            size_hint_y=0.75,  # 75% da altura disponível
            padding=[dp(60), dp(500), dp(60), dp(30)]  # Padding no topo máximo 500dp
        )
        
        # Grid para os cacifos (2 linhas, 2 colunas - grelha 2x2)
        lockers_grid = GridLayout(
            cols=2,
            rows=2,
            spacing=dp(20), 
            size_hint=(None, None),
            size=(dp(360), dp(320)),  # Tamanho fixo mais quadrado (360x320)
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Centralizar horizontal e verticalmente
        )
        
        # Criar cacifos (apenas os que existem)
        self.create_lockers(lockers_grid)
        
        grid_container.add_widget(lockers_grid)
        
        # Espaçador inicial para empurrar o grid ao máximo para baixo
        spacer = BoxLayout(size_hint_y=None, height=dp(400))
        self.content_area.add_widget(spacer)
        
        self.content_area.add_widget(grid_container)
        
        # Espaçador antes das instruções
        spacer2 = BoxLayout(size_hint_y=None, height=dp(30))
        self.content_area.add_widget(spacer2)
        
        # Instructions
        self.instructions_label = Label(
            text=translator.get_text("find_lockers_instructions"),
            font_size='14sp',
            halign='center',
            valign='middle',
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None,
            height=dp(40)
        )
        self.instructions_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        self.content_area.add_widget(self.instructions_label)
        
        # Button to update status
        self.refresh_button = StyledButton(translator.get_text("refresh_button"), button_type='secondary')
        self.refresh_button.bind(on_press=self.refresh_locker_status)
        self.content_area.add_widget(self.refresh_button)
        
        # Final flexible spacer
        final_spacer = BoxLayout()
        self.content_area.add_widget(final_spacer)
        
        # Schedule automatic update every 2 seconds
        Clock.schedule_interval(self.auto_refresh_status, 2.0)
    
    def update_translations(self):
        """Update all translatable text elements"""
        # Update header elements
        if hasattr(self, 'title_label'):
            self.title_label.text = f'[b]{translator.get_text("find_lockers_title")}[/b]'
        if hasattr(self, 'back_button'):
            self.back_button.text = f'[b]< {translator.get_text("back_button")}[/b]'
        
        # Update content elements
        if hasattr(self, 'instructions_label'):
            self.instructions_label.text = translator.get_text("find_lockers_instructions")
        if hasattr(self, 'refresh_button'):
            self.refresh_button.text = translator.get_text("refresh_button")
        
        # Update all locker status texts
        for locker_widget in self.locker_widgets.values():
            locker_widget._update_color(None, None)  # Trigger status text update

    def create_lockers(self, parent_grid):
        """Create locker widgets - apenas os cacifos definidos no sistema"""
        # Limpar o grid completamente primeiro
        parent_grid.clear_widgets()
        
        # Apenas os 4 cacifos principais do sistema
        locker_numbers = ['001', '002', '003', '004']
        
        # Limpar qualquer referência anterior
        self.locker_widgets.clear()
        
        # Criar cada cacifo individualmente
        for locker_number in locker_numbers:
            # Get complete locker status (available, door_open, occupied)
            locker_status = self.get_locker_status(locker_number)
            
            locker = LockerBox(locker_number=locker_number, locker_status=locker_status)
            locker.bind(on_locker_select=self.on_locker_selected)
            
            # Store reference for later updates
            self.locker_widgets[locker_number] = locker
            
            parent_grid.add_widget(locker)

    def get_locker_status(self, locker_number):
        """Get complete locker status considering GPIO and database"""
        if not self.gpio_controller or not self.db:
            return 'available'  # Default
        
        # Get physical state (door open/closed)
        gpio_state = self.gpio_controller.get_all_locker_states().get(locker_number, {})
        is_physically_occupied = gpio_state.get('occupied', False)  # True means door is closed/occupied
        
        # Get database state (booked/available)
        db_status = self.db.get_locker_status(locker_number)
        
        # Determine complete status based on both physical and database state
        if is_physically_occupied:
            # Door is open (someone is accessing it)
            if db_status == 'available':
                status = 'door_open'  # Yellow - available but door is open (someone exploring)
            else:
                status = 'door_open'  # Yellow - booked and door is open (accessing contents)
        else:
            # Door is closed
            if db_status == 'available':
                status = 'available'  # Green - ready to be booked
            else:
                status = 'occupied'   # Red - booked and door is closed (stuff inside)
        return status
    
    def refresh_locker_status(self, instance=None):
        """Manually update all lockers status"""
        if not self.gpio_controller:
            print("GPIO Controller not available")
            return
            
        # Update each locker with new status
        for locker_number, locker_widget in self.locker_widgets.items():
            new_status = self.get_locker_status(locker_number)
            
            # Only update if status changed
            if locker_widget.locker_status != new_status:
                locker_widget.locker_status = new_status
                status_text = {
                    'available': 'Available',
                    'door_open': 'Door Open', 
                    'occupied': 'Occupied'
                }.get(new_status, 'Available')
                print(f"Locker {locker_number} status updated: {status_text}")

    def auto_refresh_status(self, dt):
        """Automatic status update (called by Clock)"""
        self.refresh_locker_status()

    def on_locker_selected(self, instance, locker_number):
        """Callback when a locker is selected"""
        print(f"User selected locker #{locker_number}")
        
        # Check availability in database
        if self.db:
            db_status = self.db.get_locker_status(locker_number)
            print(f"DEBUG: Locker {locker_number} database status: {db_status}")
            if db_status != 'available':
                print(f"Locker {locker_number} is not available in database! (status: {db_status})")
                self.refresh_locker_status()
                return
        
        # Check if locker is still physically available
        if self.gpio_controller:
            current_states = self.gpio_controller.get_all_locker_states()
            locker_state = current_states.get(locker_number, {})
            is_available = locker_state.get('available', False)
            print(f"DEBUG: Locker {locker_number} physical availability: {is_available}")
            if not is_available:
                print(f"Locker {locker_number} is no longer physically available!")
                self.refresh_locker_status()  # Update display
                return
        
        # Store selected locker for later use
        self.manager.selected_locker = locker_number
        print(f"DEBUG: Navigating to contact_pin for locker {locker_number}")
        # Clear contact input before navigating
        contact_screen = self.manager.get_screen('contact_pin')
        print('########## CLEARING CONTACT FIELDS ##########')
        if hasattr(contact_screen, 'birth_date_input'):
            contact_screen.birth_date_input.text = ''
        if hasattr(contact_screen, 'country_code_input'):
            contact_screen.country_code_input.text = '+351'
        if hasattr(contact_screen, 'phone_input'):
            contact_screen.phone_input.text = ''
        if hasattr(contact_screen, 'email_input'):
            contact_screen.email_input.text = ''
        print('All contact fields cleared before navigation!')

        # Navigate to contact and PIN screen
        if self.manager:
            self.manager.current = 'contact_pin'
            print(f"DEBUG: Navigation completed - current screen: {self.manager.current}")

    
class UnlockLockerScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        # Remove gpio_controller from kwargs before calling super()
        self.gpio_controller = kwargs.pop('gpio_controller', None)
        
        # Initialize with empty content first
        super().__init__(manager, title="Unlock Locker", **kwargs)
        
        # Database reference
        self.db = self.gpio_controller.db if self.gpio_controller else None
        
        # Clear everything and rebuild professionally
        self.clear_widgets()
        self.create_professional_interface()
    
    def create_professional_interface(self):
        """Create the complete professional interface with YELLOW BUTTONS and better positioning"""
        # Main container with proper background
        main_container = BoxLayout(orientation='vertical')
        
        # Main background
        with main_container.canvas.before:
            Color(248/255, 250/255, 252/255, 1)  # Light gray background
            main_container.bg_rect = RoundedRectangle(pos=main_container.pos, size=main_container.size)
        main_container.bind(pos=self._update_main_bg, size=self._update_main_bg)
        
        # HEADER with proper centering
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70))
        header.padding = [dp(20), dp(10)]
        header.spacing = dp(15)
        
        # YELLOW Back button - positioned in top left corner
        back_btn = Button(
            text='[font=FontAwesome]\uf060[/font] Back',
            markup=True,
            font_size='16sp',
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            color=(0, 0, 0, 1),  # Black text
            background_color=(0, 0, 0, 0)  # Transparent to use Canvas background
        )
        
        # YELLOW background for back button
        with back_btn.canvas.before:
            Color(1, 204/255, 0, 1)  # Yellow background
            back_btn.bg_rect = RoundedRectangle(
                pos=back_btn.pos, 
                size=back_btn.size, 
                radius=[dp(8)]
            )
        back_btn.bind(pos=self._update_back_button_bg, size=self._update_back_button_bg)
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        
        # Spacer to center title
        header.add_widget(Widget(size_hint_x=1))
        
        # Title - perfectly centered
        title_container = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(250), dp(50)))
        title_label = Label(
            text='[b]Unlock Locker[/b]',
            markup=True,
            font_size='24sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        title_container.add_widget(title_label)
        header.add_widget(title_container)
        
        # Spacer to balance layout
        header.add_widget(Widget(size_hint_x=1))
        
        # Header background - ONLY on the header
        with header.canvas.before:
            Color(0/255, 77/255, 122/255, 1)  # Professional blue
            header.bg_rect = RoundedRectangle(pos=header.pos, size=header.size)
        header.bind(pos=self._update_header_bg, size=self._update_header_bg)
        
        main_container.add_widget(header)
        
        # CONTENT AREA - remove negative padding and keep compact spacing
        content_scroll = BoxLayout(orientation='vertical')
        content_scroll.padding = [dp(40), dp(0)]  # safe, non-negative top padding
        content_scroll.spacing = dp(5)  # small, consistent spacing
        
        # Hero section with icon and title - compact but not clipped
        hero_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(4))
        hero_section.bind(minimum_height=hero_section.setter('height'))
        
        # Large icon - ensure not clipped
        hero_icon = Label(
            text='[font=FontAwesome]\uf09c[/font]',
            markup=True,
            font_size='60sp',  # Keep normal size
            size_hint_y=None,
            height=dp(70),  # Slightly taller to avoid clipping
            color=(0/255, 77/255, 122/255, 1),
            halign='center',
            valign='middle'
        )
        hero_icon.bind(size=hero_icon.setter('text_size'))
        hero_section.add_widget(hero_icon)
        
        # Main title - normal size and left aligned per feedback
        hero_title = Label(
            text='[size=32sp][b]Access Your Locker[/b][/size]',
            markup=True,
            size_hint_y=None,
            height=dp(30),  # normal height
            color=(0/255, 77/255, 122/255, 1),
            halign='left',
            valign='middle'
        )
        hero_title.bind(size=hero_title.setter('text_size'))
        hero_section.add_widget(hero_title)
        
        # Subtitle with lock icon - normal size and left aligned
        hero_subtitle = Label(
            text='[font=FontAwesome]\uf023[/font] [size=16sp]Enter your booking details below to unlock your reserved locker[/size]',  # Tamanho mantido
            markup=True,
            size_hint_y=None,
            height=dp(20),  # normal height
            color=(100/255, 100/255, 100/255, 1),
            halign='left',
            valign='middle'
        )
        hero_subtitle.bind(size=hero_subtitle.setter('text_size'))
        hero_section.add_widget(hero_subtitle)
        
        content_scroll.add_widget(hero_section)
        # Remove extra spacer between hero and form to tighten layout
        
        # FORM CARD with better styling
        form_card = ProfessionalCard()
        form_card.size_hint_y = None
        form_card.height = dp(280)  # Slightly reduced
        form_card.padding = [dp(25), dp(20)]
        form_card.spacing = dp(18)
        
        # Contact section
        contact_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        contact_section.bind(minimum_height=contact_section.setter('height'))
        
        # Contact label with icon
        contact_label = Label(
            text='[font=FontAwesome]\uf0e0[/font] [b]Contact Information[/b]',
            markup=True,
            font_size='18sp',
            size_hint_y=None,
            height=dp(28),
            color=(0/255, 77/255, 122/255, 1),
            halign='left',
            valign='middle'
        )
        contact_label.bind(size=contact_label.setter('text_size'))
        contact_section.add_widget(contact_label)
        
        # Contact field - FUNCTIONAL input
        self.contact_field = self.create_functional_input(
            icon='\uf0e0',
            placeholder='Email or phone number used for booking'
        )
        contact_section.add_widget(self.contact_field)
        form_card.add_widget(contact_section)
        
        # PIN section
        pin_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        pin_section.bind(minimum_height=pin_section.setter('height'))
        
        # PIN label with icon
        pin_label = Label(
            text='[font=FontAwesome]\uf292[/font] [b]Security PIN[/b]',
            markup=True,
            font_size='18sp',
            size_hint_y=None,
            height=dp(28),
            color=(0/255, 77/255, 122/255, 1),
            halign='left',
            valign='middle'
        )
        pin_label.bind(size=pin_label.setter('text_size'))
        pin_section.add_widget(pin_label)
        
        # PIN field - FUNCTIONAL input with password
        self.pin_field = self.create_functional_input(
            icon='\uf292',
            placeholder='Enter your 4-digit security PIN',
            is_password=True,
            input_filter='int'
        )
        pin_section.add_widget(self.pin_field)
        form_card.add_widget(pin_section)
        
        # Unlock button section - MOVED DOWN
        button_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(12))
        button_section.bind(minimum_height=button_section.setter('height'))
        
        # Add extra spacing to push button down
        button_section.add_widget(Widget(size_hint_y=None, height=dp(40)))
        
        # YELLOW UNLOCK BUTTON!
        self.unlock_button = Button(
            text='[font=FontAwesome]\uf09c[/font] UNLOCK MY LOCKER',
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=dp(60),
            color=(0, 0, 0, 1),  # Black text on yellow
            background_color=(0, 0, 0, 0)  # Transparent to use Canvas background
        )
        
        # YELLOW background for unlock button
        with self.unlock_button.canvas.before:
            Color(1, 204/255, 0, 1)  # Yellow background
            self.unlock_button.bg_rect = RoundedRectangle(
                pos=self.unlock_button.pos, 
                size=self.unlock_button.size, 
                radius=[dp(8)]
            )
        self.unlock_button.bind(pos=self._update_unlock_button_bg, size=self._update_unlock_button_bg)
        self.unlock_button.bind(on_press=self.unlock_locker)
        button_section.add_widget(self.unlock_button)
        
        form_card.add_widget(button_section)
        content_scroll.add_widget(form_card)
        
        # Remove fixed spacer to avoid pushing footer off-screen
        
        # FOOTER SECTION - BOTTOM positioned
        footer_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        footer_section.bind(minimum_height=footer_section.setter('height'))
        
        # Security message - smaller and at bottom
        security_text = Label(
            text='[font=FontAwesome]\uf023[/font] [size=13sp][b]Bank-level security[/b] • Your data is encrypted and protected[/size]',
            markup=True,
            size_hint_y=None,
            height=dp(22),
            color=(0/255, 150/255, 0, 1),
            halign='center',
            valign='middle'
        )
        security_text.bind(size=security_text.setter('text_size'))
        footer_section.add_widget(security_text)
        
        # Trust badges in horizontal layout - COMPACT
        badges_container = BoxLayout(orientation='horizontal', size_hint_y=None)
        badges_container.bind(minimum_height=badges_container.setter('height'))
        badges_container.add_widget(Widget())  # Left spacer
        
        badges_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), spacing=dp(25))
        badges_layout.bind(minimum_height=badges_layout.setter('height'))
        badges_layout.width = dp(220)
        badges_layout.height = dp(30)
        
        # SSL badge - compact
        ssl_badge = Label(
            text='[font=FontAwesome]\uf084[/font]\n[size=11sp]SSL[/size]',
            markup=True,
            size_hint=(None, None),
            size=(dp(45), dp(30)),
            color=(0/255, 150/255, 0, 1),
            halign='center',
            valign='middle'
        )
        ssl_badge.bind(size=ssl_badge.setter('text_size'))
        badges_layout.add_widget(ssl_badge)
        
        # Secure badge - compact
        secure_badge = Label(
            text='[font=FontAwesome]\uf132[/font]\n[size=11sp]SECURE[/size]',
            markup=True,
            size_hint=(None, None),
            size=(dp(65), dp(30)),
            color=(0/255, 150/255, 0, 1),
            halign='center',
            valign='middle'
        )
        secure_badge.bind(size=secure_badge.setter('text_size'))
        badges_layout.add_widget(secure_badge)
        
        # Verified badge - compact
        verified_badge = Label(
            text='[font=FontAwesome]\uf00c[/font]\n[size=11sp]VERIFIED[/size]',
            markup=True,
            size_hint=(None, None),
            size=(dp(65), dp(30)),
            color=(0/255, 150/255, 0, 1),
            halign='center',
            valign='middle'
        )
        verified_badge.bind(size=verified_badge.setter('text_size'))
        badges_layout.add_widget(verified_badge)
        
        badges_container.add_widget(badges_layout)
        badges_container.add_widget(Widget())  # Right spacer
        footer_section.add_widget(badges_container)
        
        content_scroll.add_widget(footer_section)
        
        # Flexible spacer at bottom to push content up (removes big white space above)
        content_scroll.add_widget(Widget(size_hint_y=1))
        
        main_container.add_widget(content_scroll)
        self.add_widget(main_container)
        
        # Set backward compatibility references for form functionality
        self.contact_input = self.contact_field
        self.pin_input = self.pin_field
    
    def create_functional_input(self, icon, placeholder, is_password=False, input_filter=None):
        """Create a functional input field with proper sizing"""
        # Container for the input
        input_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(55))
        input_container.spacing = dp(12)
        input_container.padding = [dp(12), dp(8)]
        
        # Icon container
        icon_container = BoxLayout(size_hint_x=None, width=dp(40))
        icon_label = Label(
            text=f'[font=FontAwesome]{icon}[/font]',
            markup=True,
            font_size='20sp',
            color=(0/255, 77/255, 122/255, 1),
            halign='center',
            valign='middle'
        )
        icon_label.bind(size=icon_label.setter('text_size'))
        icon_container.add_widget(icon_label)
        
        # Input field
        text_input = TextInput(
            hint_text=placeholder,
            font_size='16sp',
            multiline=False,
            password=is_password,
            input_filter=input_filter,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0/255, 77/255, 122/255, 1),
            selection_color=(0/255, 77/255, 122/255, 0.3),
            padding=[dp(12), dp(8), dp(12), dp(8)]
        )
        
        # Container background with border
        with input_container.canvas.before:
            Color(1, 1, 1, 1)  # White background
            input_container.bg_rect = RoundedRectangle(
                pos=input_container.pos, 
                size=input_container.size, 
                radius=[dp(8)]
            )
            Color(200/255, 200/255, 200/255, 1)  # Border color
            input_container.border_rect = RoundedRectangle(
                pos=input_container.pos, 
                size=input_container.size, 
                radius=[dp(8)]
            )
        
        input_container.bind(pos=self._update_input_bg, size=self._update_input_bg)
        
        # Focus change handler - YELLOW FOCUS!
        def on_focus_change(instance, focus):
            with input_container.canvas.before:
                if focus:
                    Color(1, 204/255, 0, 1)  # YELLOW border when focused
                else:
                    Color(200/255, 200/255, 200/255, 1)  # Gray border when not focused
                input_container.border_rect = RoundedRectangle(
                    pos=input_container.pos, 
                    size=input_container.size, 
                    radius=[dp(8)]
                )
        
        text_input.bind(focus=on_focus_change)
        
        input_container.add_widget(icon_container)
        input_container.add_widget(text_input)
        
        # Store the actual TextInput widget as an attribute
        input_container.text_input = text_input
        
        return input_container
    
    def _update_main_bg(self, instance, value):
        """Update main background position"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
    
    def _update_header_bg(self, instance, value):
        """Update header background position"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
    
    def _update_back_button_bg(self, instance, value):
        """Update back button background to keep yellow"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
    
    def _update_unlock_button_bg(self, instance, value):
        """Update unlock button background to keep yellow"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
    
    def _update_input_bg(self, instance, value):
        """Update input background position"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border_rect'):
            instance.border_rect.pos = instance.pos
            instance.border_rect.size = instance.size
    
    def go_back(self, instance):
        """Go back to home screen"""
        print("Going back from unlock_locker")
        if self.manager:
            self.manager.current = 'home'
    
    def reset_form(self, instance):
        """Reset form fields"""
        print("Executing reset_form - clearing fields")
        if hasattr(self, 'contact_field') and hasattr(self.contact_field, 'text_input'):
            self.contact_field.text_input.text = ""
        if hasattr(self, 'pin_field') and hasattr(self.pin_field, 'text_input'):
            self.pin_field.text_input.text = ""
    
    def update_translations(self):
        """Update translations (placeholder)"""
        pass

    def unlock_locker(self, instance):
        """Function to unlock locker using database"""
        # Get text from the functional input fields
        contact = self.contact_field.text_input.text.strip() if hasattr(self.contact_field, 'text_input') else ""
        pin = self.pin_field.text_input.text.strip() if hasattr(self.pin_field, 'text_input') else ""
        
        if not contact or not pin:
            print("Error: Contact and PIN are required")
            self.show_error_message("Contact and PIN are required")
            return
        
        if not pin.isdigit() or len(pin) != 4:
            print("Error: PIN must have 4 digits")
            self.show_error_message("PIN must be 4 digits")
            return
        
        if self.db:
            # Try to unlock using database
            locker_number = self.db.unlock_locker(contact, pin)
            
            if locker_number:
                print(f"Success: Locker {locker_number} unlocked for {contact}")
                # Use GPIO controller to physically unlock
                if self.gpio_controller:
                    success = self.gpio_controller.pulse_locker_unlock(locker_number)
                    if success:
                        self.show_success_message(f"Locker {locker_number} is now open!")
                    else:
                        self.show_error_message("Locker unlocked in system but physical unlock failed")
                else:
                    self.show_success_message(f"Locker {locker_number} unlocked successfully!")
                
                # Clear form after successful unlock
                self.reset_form(None)
            else:
                print(f"Error: No booking found for {contact} with PIN {pin}")
                self.show_error_message("Invalid contact information or PIN. Please check your booking details.")
        else:
            print("Error: Database not available")
            self.show_error_message("System temporarily unavailable. Please try again later.")
    
    def show_error_message(self, message):
        """Show error message to user"""
        print(f"Error message: {message}")
        # Here you could implement a popup or toast message
    
    def show_success_message(self, message):
        """Show success message to user"""
        print(f"Success message: {message}")
        # Here you could implement a popup or toast message

