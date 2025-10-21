from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
import threading
import time
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
        # Remover gpio_controller dos kwargs antes de chamar super()
        self.gpio_controller = kwargs.pop('gpio_controller', None)
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
        
        # "Contact:" aligned to the left
        contact_title = Label(
            text='Contact:',
            font_size='18sp',
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        contact_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        white_area.add_widget(contact_title)
        
        # Contact input field below
        self.contact_input = TextInput(
            hint_text='example@email.com or +351 123 456 789',
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
        
        # Instrução
        instruction = Label(
            text='Enter your contact information to proceed. A PIN will be generated for your locker.',
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
        contact = self.contact_input.text.strip()
        if not contact:
            self.show_error_popup("Please enter a valid contact")
            return
            
        selected_locker = getattr(self.manager, 'selected_locker', None)
        
        if not selected_locker:
            self.show_error_popup("Error: No locker selected")
            return
        
        # Get database reference through manager
        db = None
        if hasattr(self.manager, 'gpio_controller') and self.manager.gpio_controller:
            db = self.manager.gpio_controller.db
        
        if db:
            # Try to book the locker in the database - PIN será gerado automaticamente
            success = db.book_locker(selected_locker, contact)
            
            if success and success.get('success', False):
                # Obter PIN gerado automaticamente
                generated_pin = success.get('pin', '0000')
                
                # Open the locker physically with 20ms pulse
                if self.manager.gpio_controller:
                    unlock_success = self.manager.gpio_controller.pulse_locker_unlock(selected_locker, 0.02)
                    if unlock_success:
                        print(f'Locker {selected_locker} opened with 20ms pulse! Generated PIN: {generated_pin}')
                    else:
                        print(f'Error sending pulse to locker {selected_locker}')
                
                # Show success popup with generated PIN
                self.show_success_popup(selected_locker, contact, generated_pin)
            else:
                error_msg = success.get('message', f'Error booking locker {selected_locker}') if success else f'Error booking locker {selected_locker}'
                self.show_error_popup(error_msg)
        else:
            # Fallback to simulation mode - usar sistema automático de PIN da database
            if hasattr(self.manager, 'gpio_controller') and self.manager.gpio_controller and self.manager.gpio_controller.db:
                # Usar a database mesmo em modo simulação
                db_fallback = self.manager.gpio_controller.db
                success = db_fallback.book_locker(selected_locker, contact)
                if success and success.get('success', False):
                    generated_pin = success.get('pin', '0000')
                    print(f'Database booking in simulation - Locker: {selected_locker}, Contact: {contact}, PIN: {generated_pin}')
                    
                    # Simulate locker opening with pulse
                    if self.manager.gpio_controller:
                        self.manager.gpio_controller.pulse_locker_unlock(selected_locker, 0.02)
                        print(f'20ms pulse sent to locker {selected_locker} (simulation mode)')
                    
                    # Show success popup
                    self.show_success_popup(selected_locker, contact, generated_pin)
                else:
                    error_msg = success.get('message', f'Error booking locker {selected_locker}') if success else f'Error booking locker {selected_locker}'
                    self.show_error_popup(error_msg)
            else:
                # Modo simulação completo sem database
                import random
                generated_pin = f"{random.randint(1000, 9999)}"
                print(f'Full simulation booking - Locker: {selected_locker}, Contact: {contact}, PIN: {generated_pin}')
                
                # Simulate locker opening with pulse
                if self.manager.gpio_controller:
                    self.manager.gpio_controller.pulse_locker_unlock(selected_locker, 0.02)
                    print(f'20ms pulse sent to locker {selected_locker} (full simulation mode)')
                
                # Show success popup
                self.show_success_popup(selected_locker, contact, generated_pin)
    
    def show_success_popup(self, locker_number, contact, pin):
        """Show confirmation popup with real-time monitoring"""
        
        # Popup layout
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Success title
        self.title_label = Label(
            text=f'[color=2ECC40][b]✅ Locker {locker_number} Opened![/b][/color]',
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        self.title_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        popup_layout.add_widget(self.title_label)
        
        # Real-time status
        self.status_label = Label(
            text='[color=FF851B][b]🔓 LOCKER OPEN - WAITING FOR CLOSURE[/b][/color]',
            markup=True,
            font_size='18sp',
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        self.status_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        popup_layout.add_widget(self.status_label)
        
        # Booking information
        info_text = f'''[b]Booking Details:[/b]
        
• Locker: {locker_number}
• Contact: {contact}
• PIN: [color=FF4136][b]{pin}[/b][/color]

[color=FF851B][b]⚠️ INSTRUCTIONS:[/b][/color]
        
[color=2ECC40]1.[/color] Place your belongings
[color=2ECC40]2.[/color] [b]Close the locker door properly[/b]
[color=2ECC40]3.[/color] Save your PIN: [b]{pin}[/b]

[color=AAAAAA]This popup will close automatically 
when the locker is closed[/color]'''
        
        self.info_label = Label(
            text=info_text,
            markup=True,
            font_size='14sp',
            halign='center',
            valign='middle',
            text_size=(dp(400), None)
        )
        popup_layout.add_widget(self.info_label)
        
        # Button to close manually (if needed)
        self.manual_close_button = Button(
            text='Close Manually',
            size_hint_y=None,
            height=dp(50),
            background_color=(108/255, 117/255, 125/255, 1)  # Gray
        )
        
        # Create popup
        self.monitoring_popup = Popup(
            title=f'Locker {locker_number} - Monitoring',
            content=popup_layout,
            size_hint=(0.8, 0.85),
            auto_dismiss=False
        )
        
        # Function to close popup manually
        def manual_close(button_instance):
            self.stop_monitoring = True
            self.monitoring_popup.dismiss()
            if self.manager:
                self.manager.current = 'home'
        
        self.manual_close_button.bind(on_press=manual_close)
        popup_layout.add_widget(self.manual_close_button)
        
        # Monitoring control variables
        self.stop_monitoring = False
        self.monitoring_locker = locker_number
        self.popup_start_time = time.time()
        
        # Show popup
        self.monitoring_popup.open()
        
        # Start real-time monitoring
        self.start_locker_monitoring(locker_number)
    
    def start_locker_monitoring(self, locker_number):
        """Start real-time locker status monitoring"""
        
        def monitor_locker():
            """Function that runs in separate thread to monitor the locker"""
            
            check_interval = 1.0  # Check every 1 second
            max_monitoring_time = 300  # 5 minutes maximum
            
            while not self.stop_monitoring:
                try:
                    current_time = time.time()
                    elapsed_time = current_time - self.popup_start_time
                    
                    # Stop monitoring after maximum time
                    if elapsed_time > max_monitoring_time:
                        Clock.schedule_once(lambda dt: self.timeout_monitoring(), 0)
                        break
                    
                    # Check locker status
                    if hasattr(self.manager, 'gpio_controller') and self.manager.gpio_controller:
                        # Check if the locker was physically closed
                        is_occupied = self.manager.gpio_controller.is_locker_occupied(locker_number)
                        
                        if not is_occupied:
                            # Locker was closed!
                            Clock.schedule_once(lambda dt: self.on_locker_closed(), 0)
                            break
                        else:
                            # Locker still open, update status
                            elapsed_minutes = int(elapsed_time // 60)
                            elapsed_seconds = int(elapsed_time % 60)
                            Clock.schedule_once(
                                lambda dt: self.update_status_open(elapsed_minutes, elapsed_seconds), 0
                            )
                    
                    time.sleep(check_interval)
                    
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    Clock.schedule_once(lambda dt: self.on_monitoring_error(str(e)), 0)
                    break
        
        # Start monitoring thread
        monitoring_thread = threading.Thread(target=monitor_locker, daemon=True)
        monitoring_thread.start()
    
    def update_status_open(self, minutes, seconds):
        """Update status when locker is still open"""
        
        if hasattr(self, 'status_label') and self.status_label:
            if minutes > 0:
                time_text = f"{minutes}m {seconds}s"
            else:
                time_text = f"{seconds}s"
                
            # Change color based on elapsed time
            if minutes >= 2:  # More than 2 minutes
                color = "FF4136"  # Red
                icon = "⚠️"
                message = f"WARNING: Locker open for {time_text}"
            elif minutes >= 1:  # More than 1 minute
                color = "FF851B"  # Orange
                icon = "⏰"
                message = f"Locker open for {time_text}"
            else:  # Less than 1 minute
                color = "2ECC40"  # Green
                icon = "🔓"
                message = f"Locker open for {time_text}"
            
            self.status_label.text = f'[color={color}][b]{icon} {message.upper()}[/b][/color]'
    
    def on_locker_closed(self):
        """Called when the locker is closed"""
        
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.text = '[color=2ECC40][b]✅ LOCKER CLOSED SUCCESSFULLY![/b][/color]'
        
        if hasattr(self, 'title_label') and self.title_label:
            self.title_label.text = f'[color=2ECC40][b]✅ Locker {self.monitoring_locker} Closed![/b][/color]'
        
        if hasattr(self, 'manual_close_button') and self.manual_close_button:
            self.manual_close_button.text = 'Continue'
            self.manual_close_button.background_color = (46/255, 204/255, 64/255, 1)  # Green
        
        # Close popup automatically after 2 seconds
        Clock.schedule_once(lambda dt: self.auto_close_popup(), 2.0)
    
    def on_monitoring_error(self, error_message):
        """Called when there's a monitoring error"""
        
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.text = f'[color=FF4136][b]❌ ERROR: {error_message}[/b][/color]'
    
    def timeout_monitoring(self):
        """Called when monitoring reaches time limit"""
        
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.text = '[color=FF4136][b]⏰ TIME LIMIT REACHED[/b][/color]'
        
        if hasattr(self, 'manual_close_button') and self.manual_close_button:
            self.manual_close_button.text = 'Close (Timeout)'
            self.manual_close_button.background_color = (255/255, 65/255, 54/255, 1)  # Red
    
    def auto_close_popup(self):
        """Close popup automatically"""
        
        self.stop_monitoring = True
        if hasattr(self, 'monitoring_popup') and self.monitoring_popup:
            self.monitoring_popup.dismiss()
        
        if self.manager:
            self.manager.current = 'home'
    
    def show_error_popup(self, message):
        """Show error popup"""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        error_label = Label(
            text=f'[color=FF4136][b]❌ Error[/b][/color]\n\n{message}',
            markup=True,
            font_size='18sp',
            halign='center',
            valign='middle'
        )
        error_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        popup_layout.add_widget(error_label)
        
        ok_button = Button(
            text='OK',
            size_hint_y=None,
            height=dp(50),
            background_color=(255/255, 65/255, 54/255, 1)  # Red
        )
        
        popup = Popup(
            title='Error',
            content=popup_layout,
            size_hint=(0.6, 0.4),
            auto_dismiss=False
        )
        
        ok_button.bind(on_press=popup.dismiss)
        popup_layout.add_widget(ok_button)
        popup.open()
    
    def auto_lock_locker(self, locker_number):
        """Automatically close the locker after determined time"""
        if hasattr(self.manager, 'gpio_controller') and self.manager.gpio_controller:
            self.manager.gpio_controller.lock_locker(locker_number)
            print(f'Locker {locker_number} automatically closed after 10 seconds')

    def go_back(self, instance):
        if self.manager:
            self.manager.current = 'find_lockers'