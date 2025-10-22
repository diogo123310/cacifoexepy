import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import time

# Import your screen definitions
from homescreen import KioskHomeScreen, OptionCard
from lockerscreens import FindLockersScreen, UnlockLockerScreen
from contact_pin_screen import ContactPinScreen
from database import LockerDatabase

# GPIO imports - only import if running on Raspberry Pi
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
    print("GPIO library loaded successfully")
except ImportError:
    GPIO_AVAILABLE = False
    print("GPIO library not available - running in development mode")
    # Create a mock GPIO class for development
    class MockGPIO:
        HIGH = 1
        LOW = 0
        IN = 'in'
        OUT = 'out'
        PUD_DOWN = 'pud_down'
        PUD_UP = 'pud_up'
        
        def __init__(self):
            # Simulate pin states (can be changed for testing)
            self.pin_states = {
                2: 0,   # PIN_INPUT_BOX1 - Locker 001 available (door closed)
                4: 0,   # PIN_INPUT_BOX2 - Locker 002 available (door closed)
                27: 0,  # PIN_INPUT_BOX3 - Locker 003 available (door closed)
                10: 0   # PIN_INPUT_BOX4 - Locker 004 available (door closed)
            }
            # To simulate automatic locker closing after time
            self.locker_auto_close_timers = {}
        
        @staticmethod
        def setmode(mode):
            print(f"Mock GPIO: setmode({mode})")
        
        @staticmethod
        def setup(pin, mode, pull_up_down=None):
            print(f"Mock GPIO: setup pin {pin}, mode {mode}, pull_up_down {pull_up_down}")
        
        @staticmethod
        def output(pin, value):
            state_text = "HIGH" if value == 1 else "LOW"
            print(f"Mock GPIO: output pin {pin} = {state_text}")
        
        def input(self, pin):
            state = self.pin_states.get(pin, 0)
            print(f"Mock GPIO: reading pin {pin} = {state}")
            return state
        
        @staticmethod
        def cleanup():
            print("Mock GPIO: cleanup")
        
        def simulate_pin_change(self, pin, new_state):
            """Método para simular mudanças nos pinos durante teste"""
            self.pin_states[pin] = new_state
            print(f"Mock GPIO: Pin {pin} simulado como {new_state}")
        
        def simulate_pulse(self, pin, duration=0.02):
            """Simulate a pulse in development mode"""
            print(f"Mock GPIO: Simulating pulse on pin {pin} for {duration*1000:.0f}ms")
            print(f"Mock GPIO: Pin {pin} HIGH")
            import time
            time.sleep(duration)
            print(f"Mock GPIO: Pin {pin} LOW - pulse complete")
        
        def simulate_locker_opening(self, locker_number, auto_close_after=15):
            """Simulate locker opening and automatic closing after X seconds"""
            import threading
            import time
            
            # Map locker to input pin
            locker_to_input_pin = {
                '001': 2,   # PIN_INPUT_BOX1
                '002': 4,   # PIN_INPUT_BOX2  
                '003': 27,  # PIN_INPUT_BOX3
                '004': 10   # PIN_INPUT_BOX4
            }
            
            if locker_number in locker_to_input_pin:
                input_pin = locker_to_input_pin[locker_number]
                
                # Simulate locker open (pin HIGH = occupied/open)
                self.pin_states[input_pin] = 1
                print(f"Mock GPIO: Locker {locker_number} simulated as OPEN")
                
                # Cancel previous timer if exists
                if locker_number in self.locker_auto_close_timers:
                    self.locker_auto_close_timers[locker_number].cancel()
                
                # Schedule automatic closing
                def auto_close():
                    self.pin_states[input_pin] = 0
                    print(f"Mock GPIO: Locker {locker_number} simulated as CLOSED automatically")
                    if locker_number in self.locker_auto_close_timers:
                        del self.locker_auto_close_timers[locker_number]
                
                timer = threading.Timer(auto_close_after, auto_close)
                self.locker_auto_close_timers[locker_number] = timer
                timer.start()
                
                print(f"Mock GPIO: Locker {locker_number} will close automatically in {auto_close_after}s")
        
        def simulate_locker_closing(self, locker_number):
            """Simulate manual locker closing"""
            locker_to_input_pin = {
                '001': 2, '002': 4, '003': 27, '004': 10
            }
            
            if locker_number in locker_to_input_pin:
                input_pin = locker_to_input_pin[locker_number]
                self.pin_states[input_pin] = 0
                print(f"Mock GPIO: Locker {locker_number} simulated as CLOSED manually")
                
                # Cancel automatic closing timer
                if locker_number in self.locker_auto_close_timers:
                    self.locker_auto_close_timers[locker_number].cancel()
                    del self.locker_auto_close_timers[locker_number]
    
    GPIO = MockGPIO()

LabelBase.register(name="FontAwesome", fn_regular="fa-solid-900.ttf.otf")

# GPIO Pin Configuration
PIN_INPUT_BOX1 = 2
PIN_OUTPUT_BOX1 = 3
PIN_INPUT_BOX2 = 4
PIN_OUTPUT_BOX2 = 17
PIN_INPUT_BOX3 = 27
PIN_OUTPUT_BOX3 = 22
PIN_INPUT_BOX4 = 10
PIN_OUTPUT_BOX4 = 9

# GPIO Initialization
def initialize_gpio():
    """Initialize GPIO pins for locker control"""
    if GPIO_AVAILABLE:
        GPIO.setmode(GPIO.BCM)
    
    # Setup pins for each locker
    GPIO.setup(PIN_INPUT_BOX1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_OUTPUT_BOX1, GPIO.OUT)
    GPIO.output(PIN_OUTPUT_BOX1, GPIO.LOW)

    GPIO.setup(PIN_INPUT_BOX2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_OUTPUT_BOX2, GPIO.OUT)
    GPIO.output(PIN_OUTPUT_BOX2, GPIO.LOW)

    GPIO.setup(PIN_INPUT_BOX3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_OUTPUT_BOX3, GPIO.OUT)
    GPIO.output(PIN_OUTPUT_BOX3, GPIO.LOW)

    GPIO.setup(PIN_INPUT_BOX4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_OUTPUT_BOX4, GPIO.OUT)
    GPIO.output(PIN_OUTPUT_BOX4, GPIO.LOW)

class GPIOController:
    """Class to handle GPIO operations for lockers"""
    
    def __init__(self):
        self.locker_pins = {
            '001': {'input': PIN_INPUT_BOX1, 'output': PIN_OUTPUT_BOX1},
            '002': {'input': PIN_INPUT_BOX2, 'output': PIN_OUTPUT_BOX2},
            '003': {'input': PIN_INPUT_BOX3, 'output': PIN_OUTPUT_BOX3},
            '004': {'input': PIN_INPUT_BOX4, 'output': PIN_OUTPUT_BOX4}
        }
        
        # Integrar com a base de dados
        self.db = LockerDatabase()
    
    def is_locker_occupied(self, locker_number):
        """Check if a locker is occupied using input pin"""
        if locker_number in self.locker_pins:
            input_pin = self.locker_pins[locker_number]['input']
            pin_state = GPIO.input(input_pin)
            is_occupied = pin_state == GPIO.HIGH
            
            # Log do estado GPIO
            gpio_state = f"Pin {input_pin}: {pin_state}"
            
            # Sincronizar com a base de dados
            db_status = self.db.get_locker_status(locker_number)
            
            # If physical state doesn't match database, correct it
            if is_occupied and db_status == 'available':
                # Locker physically occupied but marked as available
                self.db.log_action(locker_number, 'GPIO_SYNC', 
                                 'Physical state: occupied, DB state: available', gpio_state)
                
            elif not is_occupied and db_status == 'occupied':
                # Locker physically closed but still marked as occupied in DB
                # Keep it occupied until manually unlocked via "unlock locker" section
                pass  # Don't auto-return, wait for manual unlock
            
            print(f"Locker {locker_number} - Pin {input_pin}: {pin_state} ({'OCCUPIED' if is_occupied else 'AVAILABLE'}) - DB: {db_status}")
            return is_occupied
        return False
    
    def unlock_locker(self, locker_number):
        """Unlock a specific locker using output pin"""
        if locker_number in self.locker_pins:
            output_pin = self.locker_pins[locker_number]['output']
            GPIO.output(output_pin, GPIO.HIGH)
            
            # Log na base de dados
            self.db.log_action(locker_number, 'UNLOCK_GPIO', 
                             f'GPIO pin {output_pin} set HIGH')
            
            print(f"Locker {locker_number} unlocked (GPIO pin {output_pin} HIGH)")
            return True
        return False
    
    def lock_locker(self, locker_number):
        """Lock a specific locker using output pin"""
        if locker_number in self.locker_pins:
            output_pin = self.locker_pins[locker_number]['output']
            GPIO.output(output_pin, GPIO.LOW)
            
            # Log na base de dados
            self.db.log_action(locker_number, 'LOCK_GPIO', 
                             f'GPIO pin {output_pin} set LOW')
            
            print(f"Locker {locker_number} locked (GPIO pin {output_pin} LOW)")
            return True
        return False
    
    # --- pulse 20 ms ---
    def pulse_output(self, pin_out, pulse_duration=0.02):
        """
        Gera um pulso de 20ms (por padrão) no pin especificado
        pin_out: número do pin GPIO
        pulse_duration: duração do pulso em segundos (padrão 0.02 = 20ms)
        """
        try:
            # Ativar pin (HIGH)
            GPIO.output(pin_out, GPIO.HIGH)
            print(f"Pin {pin_out} set HIGH - pulse started")
            
            # Aguardar duração do pulso (20ms por padrão)
            time.sleep(pulse_duration)
            
            # Desativar pin (LOW)
            GPIO.output(pin_out, GPIO.LOW)
            print(f"Pin {pin_out} set LOW - pulse completed ({pulse_duration*1000:.0f}ms)")
            
            return True
        except Exception as e:
            print(f"Erro no pulso do pin {pin_out}: {e}")
            return False
    
    def pulse_locker_unlock(self, locker_number, pulse_duration=0.02):
        """
        Send 20ms pulse to open a specific locker
        locker_number: locker number ('001', '002', etc.)
        pulse_duration: pulse duration in seconds (default 0.02 = 20ms)
        """
        if locker_number in self.locker_pins:
            output_pin = self.locker_pins[locker_number]['output']
            
            print(f"Sending {pulse_duration*1000:.0f}ms pulse to locker {locker_number} (pin {output_pin})")
            
            # Executar pulso
            success = self.pulse_output(output_pin, pulse_duration)
            
            if success:
                # Log na base de dados
                self.db.log_action(locker_number, 'PULSE_UNLOCK', 
                                 f'Pulse {pulse_duration*1000:.0f}ms sent to pin {output_pin}')
                
                # Simular abertura do cacifo (apenas no MockGPIO)
                if hasattr(GPIO, 'simulate_locker_opening'):
                    GPIO.simulate_locker_opening(locker_number, auto_close_after=15)  # Fecha automaticamente em 15s
                
                print(f"Locker {locker_number} pulse unlock completed")
                return True
            else:
                print(f"Falha no pulso do cacifo {locker_number}")
                return False
        else:
            print(f"Cacifo {locker_number} não encontrado")
            return False
    
    def pulse_all_lockers(self, pulse_duration=0.02):
        """
        Envia pulso para todos os cacifos (para teste)
        pulse_duration: duração do pulso em segundos (padrão 0.02 = 20ms)
        """
        print(f"Enviando pulso de {pulse_duration*1000:.0f}ms para todos os cacifos...")
        
        results = {}
        for locker_number in self.locker_pins.keys():
            results[locker_number] = self.pulse_locker_unlock(locker_number, pulse_duration)
            time.sleep(0.1)  # Pequena pausa entre cacifos
        
        return results
    
    def get_all_locker_states(self):
        """Get the state of all lockers with database sync"""
        states = {}
        for locker_number in self.locker_pins:
            is_physically_occupied = self.is_locker_occupied(locker_number)
            db_status = self.db.get_locker_status(locker_number)
            
            states[locker_number] = {
                'occupied': is_physically_occupied,
                'available': not is_physically_occupied,
                'db_status': db_status,
                'booking_info': self.db.get_active_booking(locker_number)
            }
        return states
    
    def refresh_locker_states(self):
        """Refresh and return updated locker states"""
        return self.get_all_locker_states()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # Initialize your widgets and layout here
        # Example: self.add_widget(Label(text='Welcome to the Main Screen'))

class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__(**kwargs)
        
        # Initialize GPIO controller and database
        self.gpio_controller = GPIOController()
        self.db = LockerDatabase()
        
        # Variável para armazenar o cacifo selecionado
        self.selected_locker = None
        
        self.add_widget(MainScreen(name='main'))
        self.add_widget(LockerAccessScreen(name='locker_access'))

        # Definir as propriedades title_text e description_text
        self.title_text = "Default Title"  # Substitua pelo valor desejado
        self.description_text = "Default Description"  # Substitua pelo valor desejado

        # Adicione as telas e widgets como antes
        home_screen = Screen(name='home')
        home_screen.add_widget(KioskHomeScreen(manager=self))  # Pass manager for navigation
        self.add_widget(home_screen)

        find_lockers_screen = Screen(name='find_lockers')
        find_lockers_widget = FindLockersScreen(manager=self)
        find_lockers_widget.gpio_controller = self.gpio_controller
        find_lockers_widget.db = self.db
        find_lockers_screen.add_widget(find_lockers_widget)
        self.add_widget(find_lockers_screen)

        class UnlockLockerScreenWrapper(Screen):
            def __init__(self, screen_manager, **kwargs):
                super().__init__(**kwargs)
                self.unlock_widget = UnlockLockerScreen(manager=screen_manager, gpio_controller=screen_manager.gpio_controller)
                self.add_widget(self.unlock_widget)
            
            def on_enter(self, *args):
                """Reset screen when entering"""
                print("Resetting unlock locker screen to initial state")
                if hasattr(self.unlock_widget, 'reset_form'):
                    self.unlock_widget.reset_form(None)
        
        unlock_locker_screen = UnlockLockerScreenWrapper(self, name='unlock_locker')
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

        # Criar a tela ContactPinScreen e depois configurar o gpio_controller
        contact_pin_screen = ContactPinScreen(name='contact_pin')
        contact_pin_screen.gpio_controller = self.gpio_controller
        self.add_widget(contact_pin_screen)
        
        # Definir a tela inicial
        self.current = 'home'
    
    def update_all_translations(self):
        """Atualizar traduções em todas as telas"""
        # Atualizar tela home
        home_screen = self.get_screen('home')
        if hasattr(home_screen, 'children') and len(home_screen.children) > 0:
            home_widget = home_screen.children[0]
            if hasattr(home_widget, 'update_translations'):
                home_widget.update_translations()
        
        # Atualizar tela Find Lockers
        try:
            find_lockers_screen = self.get_screen('find_lockers')
            if find_lockers_screen.children:
                find_lockers_widget = find_lockers_screen.children[0]
                if hasattr(find_lockers_widget, 'update_translations'):
                    find_lockers_widget.update_translations()
        except:
            pass
        
        # Atualizar tela Unlock Locker
        try:
            unlock_locker_screen = self.get_screen('unlock_locker')
            if unlock_locker_screen.children:
                unlock_locker_widget = unlock_locker_screen.children[0]
                if hasattr(unlock_locker_widget, 'update_translations'):
                    unlock_locker_widget.update_translations()
        except:
            pass
        
        # Atualizar tela Contact PIN
        try:
            contact_pin_screen = self.get_screen('contact_pin')
            if contact_pin_screen.children:
                contact_pin_widget = contact_pin_screen.children[0]
                if hasattr(contact_pin_widget, 'update_translations'):
                    contact_pin_widget.update_translations()
        except:
            pass
        
        print("Traduções atualizadas em todas as telas")

    def _update_icon_text(self, instance, value):
        self.icon_label.text = value

    def _update_title_text(self, instance, value):
        self.title_label.text = f'[b]{value}[/b]'

    def _update_description_text(self, instance, value):
        self.description_label.text = value

class LockerAccessScreen(Screen):
    def __init__(self, **kwargs):
        super(LockerAccessScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.contact_input = TextInput(hint_text='Insira seu contato')
        self.pin_input = TextInput(hint_text='Insira seu PIN de 4 dígitos', password=True, multiline=False)
        self.open_locker_button = Button(text='Abrir Cacifo')

        layout.add_widget(self.contact_input)
        layout.add_widget(self.pin_input)
        layout.add_widget(self.open_locker_button)

        self.open_locker_button.bind(on_press=self.open_locker)

        self.add_widget(layout)

    def open_locker(self, instance):
        contact = self.contact_input.text
        pin = self.pin_input.text
        # Aqui você pode adicionar a lógica para abrir o cacifo usando o contato e o PIN
        print(f'Abrindo cacifo para {contact} com PIN {pin}')  
        # Voltar para a tela inicial ou outra lógica
        self.manager.current = 'home'

class LuggageKioskApp(App):
    def build(self):
        # Initialize GPIO when app starts
        initialize_gpio()
        self.screen_manager = MainScreenManager()
        return self.screen_manager
    
    def on_stop(self):
        """Clean up GPIO when app closes"""
        if GPIO_AVAILABLE:
           
            print("GPIO cleanup completed")

if __name__ == '__main__':
    LuggageKioskApp().run()