import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from translations import translator


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
        
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.border_radius)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        self.color = self.text_color
        self.background_color = (0, 0, 0, 0)  # Transparent to use custom background
        self.bold = True

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
        from kivy.uix.widget import Widget
        spacer = Widget(size_hint_y=None, height=dp(400))  # Espaçador transparente
        self.content_area.add_widget(spacer)
        
        self.content_area.add_widget(grid_container)
        
        # Espaçador antes das instruções
        spacer2 = Widget(size_hint_y=None, height=dp(30))  # Espaçador transparente
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
        final_spacer = Widget()  # Espaçador flexível transparente
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
            if db_status != 'available':
                print(f"Locker {locker_number} is not available in database!")
                self.refresh_locker_status()
                return
        
        # Check if locker is still physically available
        if self.gpio_controller:
            current_states = self.gpio_controller.get_all_locker_states()
            if not current_states.get(locker_number, {}).get('available', False):
                print(f"Locker {locker_number} is no longer available!")
                self.refresh_locker_status()  # Update display
                return
        
        # Store selected locker for later use
        self.manager.selected_locker = locker_number
        
        # Navigate to contact and PIN screen
        if self.manager:
            self.manager.current = 'contact_pin'


class UnlockLockerScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        # Remove gpio_controller from kwargs before calling super()
        self.gpio_controller = kwargs.pop('gpio_controller', None)
        super().__init__(manager, title=translator.get_text("unlock_locker_title"), **kwargs)
        
        # Database reference
        self.db = self.gpio_controller.db if self.gpio_controller else None
        
        # Clear default content_area and recreate with less padding
        self.remove_widget(self.content_area)
        self.content_area = BoxLayout(orientation='vertical', padding=[dp(40), dp(10), dp(40), dp(10)], spacing=dp(20))
        self.add_widget(self.content_area)
        
        # Flexible spacer that takes 80% of available height
        self.content_area.add_widget(Widget(size_hint_y=0.8))
        
        # Contact section
        contact_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        contact_section.bind(minimum_height=contact_section.setter('height'))
        
        # "Contact:" label
        contact_title = Label(
            text='Contact:',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        contact_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        contact_section.add_widget(contact_title)
        
        # Contact input
        self.contact_input = TextInput(
            hint_text='example@email.com or +351 123 456 789',
            multiline=False,
            font_size='16sp',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        contact_section.add_widget(self.contact_input)
        
        self.content_area.add_widget(contact_section)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(30)))
        
        # PIN section
        pin_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        pin_section.bind(minimum_height=pin_section.setter('height'))
        
        # "PIN:" label
        pin_title = Label(
            text='PIN (4 digits):',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        pin_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        pin_section.add_widget(pin_title)
        
        # PIN input
        self.pin_input = TextInput(
            hint_text='Enter your 4-digit PIN',
            multiline=False,
            password=True,
            font_size='16sp',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            input_filter='int'  # Only accepts numbers
        )
        pin_section.add_widget(self.pin_input)
        
        self.content_area.add_widget(pin_section)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(40)))
        
        # Button to unlock locker (using consistent design)
        unlock_button = StyledButton('Unlock Locker', button_type='primary')
        unlock_button.bind(on_press=self.unlock_locker)
        self.content_area.add_widget(unlock_button)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        # Instruction
        instruction = Label(
            text='Enter your contact information and 4-digit PIN to access your locker.',
            font_size='16sp',
            size_hint_y=None,
            height=dp(40),
            color=(0.4, 0.4, 0.4, 1),
            halign='center'
        )
        instruction.bind(size=lambda instance, value: setattr(instruction, 'text_size', (instruction.width, None)))
        self.content_area.add_widget(instruction)
        
        # Very small flexible spacer at the end (5% of height)
        self.content_area.add_widget(Widget(size_hint_y=0.05))
    
    def update_translations(self):
        """Update all translatable text elements"""
        # Update header elements
        if hasattr(self, 'title_label'):
            self.title_label.text = f'[b]{translator.get_text("unlock_locker_title")}[/b]'
        if hasattr(self, 'back_button'):
            self.back_button.text = f'[b]< {translator.get_text("back_button")}[/b]'
        
        # Reset the form to ensure clean translation update
        self.reset_form(None)

    def unlock_locker(self, instance):
        """Function to unlock locker using database"""
        contact = self.contact_input.text.strip()
        pin = self.pin_input.text.strip()
        
        if not contact or not pin:
            print("Error: Contact and PIN are required")
            self.show_error_message(translator.get_text("error_contact_pin_required"))
            return
        
        if not pin.isdigit() or len(pin) != 4:
            print("Error: PIN must have 4 digits")
            self.show_error_message(translator.get_text("error_pin_format"))
            return
        
        if self.db:
            # Try to unlock using database
            locker_number = self.db.unlock_locker(contact, pin)
            
            if locker_number:
                print(f"Database unlock successful for locker {locker_number}")
                
                # Return the locker to available status (complete the cycle)
                if self.db.return_locker(locker_number):
                    print(f"Locker {locker_number} returned to available status - cycle complete")
                
                # Send 20ms pulse to unlock locker physically
                if self.gpio_controller:
                    unlock_success = self.gpio_controller.pulse_locker_unlock(locker_number, 0.02)
                    if unlock_success:
                        print(f"Locker {locker_number} unlocked with 20ms pulse!")
                        self.show_unlock_success_message(locker_number)
                        
                        # Schedule automatic locking after 10 seconds (but it remains available)
                        Clock.schedule_once(lambda dt: self.auto_lock_and_return(locker_number), 10.0)
                        
                        # Refresh locker status in Find Lockers screen if it exists
                        self.refresh_find_lockers_screen()
                        
                    else:
                        print("Error sending pulse to unlock locker physically")
                        self.show_error_message(translator.get_text("error_unlock_physical"))
                else:
                    print(f"Locker {locker_number} unlocked (simulation mode)")
                    self.show_unlock_success_message(locker_number)
                    
                    # Schedule automatic locking after 10 seconds (but it remains available)
                    Clock.schedule_once(lambda dt: self.auto_lock_and_return(locker_number), 10.0)
                    
                    # Refresh locker status in Find Lockers screen if it exists
                    self.refresh_find_lockers_screen()
                    
            else:
                print("Incorrect contact or PIN, or no active booking")
                self.show_error_message(translator.get_text("error_incorrect_credentials"))
        else:
            print("Database not available")
            self.show_error_message(translator.get_text("error_system_unavailable"))
    
    def refresh_find_lockers_screen(self):
        """Refresh the Find Lockers screen status after unlock"""
        try:
            # Find the Find Lockers screen in the manager
            for screen in self.manager.screens:
                if hasattr(screen, 'refresh_locker_status') and screen.name == 'find_lockers':
                    print("Refreshing Find Lockers screen status")
                    screen.refresh_locker_status()
                    break
        except Exception as e:
            print(f"Error refreshing Find Lockers screen: {e}")
    
    def auto_lock_locker(self, locker_number):
        """Automatically lock the locker but keep it occupied until manually unlocked"""
        if self.gpio_controller:
            self.gpio_controller.lock_locker(locker_number)
            print(f'Locker {locker_number} automatically locked')
            
            # Don't auto-return to available - user must unlock via "unlock locker" section
            # The locker should remain "occupied" (red) until explicitly unlocked
            if self.db:
                try:
                    # Log the auto-lock but don't change DB status
                    self.db.log_action(locker_number, 'AUTO_LOCK', 'Locker automatically locked, remains occupied until manual unlock')
                    print(f'Locker {locker_number} auto-locked but remains occupied - must be unlocked manually')
                except Exception as e:
                    print(f"Error logging auto-lock: {e}")
            
            # Refresh Find Lockers screen to show updated status
            self.refresh_find_lockers_screen()
    
    def auto_lock_and_return(self, locker_number):
        """Automatically lock the locker after unlock via PIN - cycle complete"""
        if self.gpio_controller:
            self.gpio_controller.lock_locker(locker_number)
            print(f'Locker {locker_number} automatically locked after PIN unlock - now available')
            
            # This locker was already returned to available status in unlock_locker method
            # Just log the completion
            if self.db:
                try:
                    self.db.log_action(locker_number, 'CYCLE_COMPLETE', 'Unlocked via PIN, auto-locked, cycle complete - now available')
                except Exception as e:
                    print(f"Error logging cycle completion: {e}")
            
            # Refresh Find Lockers screen to show updated status
            self.refresh_find_lockers_screen()
    
    def find_locker_for_contact(self, contact, pin):
        """Simulate finding locker associated with contact/PIN"""
        # This would normally be a database query
        # For now, return a fixed locker for testing
        return '001'  # Simulate that locker 001 belongs to this user
    
    def show_unlock_success_message(self, locker_number):
        """Show success message for unlock"""
        # Clear content area
        self.content_area.clear_widgets()
        
        # Success message
        success_title = Label(
            text=f'[color=2ECC40][b]✅ {translator.get_text("success_locker_opened").format(locker_number=locker_number)}[/b][/color]',
            markup=True,
            font_size='32sp',
            size_hint_y=None,
            height=dp(80),
            halign='center'
        )
        success_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        self.content_area.add_widget(success_title)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(30)))
        
        # Instructions
        instructions_text = translator.get_text("success_instructions")
        
        instructions_label = Label(
            text=instructions_text,
            markup=True,
            font_size='18sp',
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(200)
        )
        instructions_label.bind(size=lambda instance, value: setattr(instructions_label, 'text_size', (instructions_label.width, None)))
        self.content_area.add_widget(instructions_label)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(30)))
        
        # Back button
        back_button = StyledButton(translator.get_text("back_to_home"), button_type='primary')
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.content_area.add_widget(back_button)
        
        # Flexible spacer
        self.content_area.add_widget(Widget())
    
    def show_error_message(self, error_text):
        """Show error message"""
        # Clear content area
        self.content_area.clear_widgets()
        
        # Error message
        error_title = Label(
            text=f'[color=FF4136][b]❌ {translator.get_text("error_title")}[/b][/color]',
            markup=True,
            font_size='32sp',
            size_hint_y=None,
            height=dp(80),
            halign='center'
        )
        error_title.bind(size=lambda instance, value: setattr(error_title, 'text_size', (error_title.width, None)))
        self.content_area.add_widget(error_title)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(30)))
        
        # Error text
        error_label = Label(
            text=error_text,
            font_size='20sp',
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(100),
            color=(255/255, 65/255, 54/255, 1)  # Red
        )
        error_label.bind(size=lambda instance, value: setattr(error_label, 'text_size', (error_label.width, None)))
        self.content_area.add_widget(error_label)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(30)))
        
        # Retry button
        retry_button = StyledButton(translator.get_text("try_again_button"), button_type='secondary')
        retry_button.bind(on_press=self.reset_form)
        self.content_area.add_widget(retry_button)
        
        # Flexible spacer
        self.content_area.add_widget(Widget())
    
    def reset_form(self, instance):
        """Reset the form for new attempt"""
        print("Executing reset_form - clearing and rebuilding interface")
        # Clear content area and rebuild the original form
        self.content_area.clear_widgets()
        
        # Flexible spacer that takes 80% of available height
        self.content_area.add_widget(Widget(size_hint_y=0.8))
        
        # Contact section
        contact_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        contact_section.bind(minimum_height=contact_section.setter('height'))
        
        # "Contact:" label
        contact_title = Label(
            text=translator.get_text("contact_label"),
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        contact_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        contact_section.add_widget(contact_title)
        
        # Contact input
        self.contact_input = TextInput(
            hint_text='example@email.com or +351 123 456 789',
            multiline=False,
            font_size='16sp',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        contact_section.add_widget(self.contact_input)
        
        self.content_area.add_widget(contact_section)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(30)))
        
        # PIN section
        pin_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        pin_section.bind(minimum_height=pin_section.setter('height'))
        
        # "PIN:" label
        pin_title = Label(
            text='PIN (4 digits):',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        pin_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        pin_section.add_widget(pin_title)
        
        # PIN input
        self.pin_input = TextInput(
            hint_text='Enter your 4-digit PIN',
            multiline=False,
            password=True,
            font_size='16sp',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            input_filter='int'  # Only accepts numbers
        )
        pin_section.add_widget(self.pin_input)
        
        self.content_area.add_widget(pin_section)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(40)))
        
        # Button to unlock locker (using consistent design)
        unlock_button = StyledButton('Unlock Locker', button_type='primary')
        unlock_button.bind(on_press=self.unlock_locker)
        self.content_area.add_widget(unlock_button)
        
        # Spacer
        self.content_area.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        # Instruction
        instruction = Label(
            text='Enter your contact information and 4-digit PIN to access your locker.',
            font_size='16sp',
            size_hint_y=None,
            height=dp(40),
            color=(0.4, 0.4, 0.4, 1),
            halign='center'
        )
        instruction.bind(size=lambda instance, value: setattr(instruction, 'text_size', (instruction.width, None)))
        self.content_area.add_widget(instruction)
        
        # Very small flexible spacer at the end (5% of height)
        self.content_area.add_widget(Widget(size_hint_y=0.05))
