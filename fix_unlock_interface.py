#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o posicionamento e funcionalidade da UnlockLockerScreen
"""

def fix_unlock_screen():
    """Corrige a classe UnlockLockerScreen com melhor posicionamento e funcionalidade"""
    
    # Ler o arquivo atual
    with open('lockerscreens.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nova implementação corrigida da UnlockLockerScreen
    new_class = '''class UnlockLockerScreen(BaseScreen):
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
        """Create the complete professional interface with proper positioning"""
        # Main container with proper background
        main_container = BoxLayout(orientation='vertical')
        
        # Main background
        with main_container.canvas.before:
            Color(248/255, 250/255, 252/255, 1)  # Light gray background
            main_container.bg_rect = RoundedRectangle(pos=main_container.pos, size=main_container.size)
        main_container.bind(pos=self._update_main_bg, size=self._update_main_bg)
        
        # HEADER with proper positioning
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80))
        header.padding = [dp(20), dp(15)]
        header.spacing = dp(15)
        
        # Back button - positioned in top left corner
        back_btn = StyledButton('[font=FontAwesome]\\uf060[/font] Back', button_type='secondary')
        back_btn.size_hint = (None, None)
        back_btn.size = (dp(120), dp(50))
        back_btn.markup = True
        back_btn.font_size = '16sp'
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        
        # Spacer to center title
        header.add_widget(Widget(size_hint_x=1))
        
        # Title - centered in header
        title_label = Label(
            text='[b]Unlock Locker[/b]',
            markup=True,
            font_size='26sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(None, None),
            size=(dp(200), dp(50))
        )
        title_label.bind(size=title_label.setter('text_size'))
        header.add_widget(title_label)
        
        # Spacer to balance layout
        header.add_widget(Widget(size_hint_x=1))
        
        # Header background - professional blue gradient
        with header.canvas.before:
            Color(0/255, 77/255, 122/255, 1)  # Professional blue
            header.bg_rect = RoundedRectangle(pos=header.pos, size=header.size)
        header.bind(pos=self._update_header_bg, size=self._update_header_bg)
        
        main_container.add_widget(header)
        
        # CONTENT AREA with scroll
        content_scroll = BoxLayout(orientation='vertical')
        content_scroll.padding = [dp(40), dp(40)]
        content_scroll.spacing = dp(35)
        
        # Hero section with icon and title
        hero_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(20))
        hero_section.bind(minimum_height=hero_section.setter('height'))
        
        # Large icon - properly displayed
        hero_icon = Label(
            text='[font=FontAwesome]\\uf09c[/font]',
            markup=True,
            font_size='80sp',
            size_hint_y=None,
            height=dp(100),
            color=(0/255, 77/255, 122/255, 1),
            halign='center',
            valign='middle'
        )
        hero_icon.bind(size=hero_icon.setter('text_size'))
        hero_section.add_widget(hero_icon)
        
        # Main title
        hero_title = Label(
            text='[size=36sp][b]Access Your Locker[/b][/size]',
            markup=True,
            size_hint_y=None,
            height=dp(50),
            color=(0/255, 77/255, 122/255, 1),
            halign='center',
            valign='middle'
        )
        hero_title.bind(size=hero_title.setter('text_size'))
        hero_section.add_widget(hero_title)
        
        # Subtitle
        hero_subtitle = Label(
            text='[size=18sp]Enter your booking details below to unlock your reserved locker[/size]',
            markup=True,
            size_hint_y=None,
            height=dp(30),
            color=(100/255, 100/255, 100/255, 1),
            halign='center',
            valign='middle'
        )
        hero_subtitle.bind(size=hero_subtitle.setter('text_size'))
        hero_section.add_widget(hero_subtitle)
        
        content_scroll.add_widget(hero_section)
        
        # FORM CARD with better styling
        form_card = ProfessionalCard()
        form_card.size_hint_y = None
        form_card.height = dp(320)
        form_card.padding = [dp(25), dp(25)]
        form_card.spacing = dp(25)
        
        # Contact section
        contact_section = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        contact_section.bind(minimum_height=contact_section.setter('height'))
        
        # Contact label with icon
        contact_label = Label(
            text='[font=FontAwesome]\\uf0e0[/font] [b]Contact Information[/b]',
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=dp(35),
            color=(0/255, 77/255, 122/255, 1),
            halign='left',
            valign='middle'
        )
        contact_label.bind(size=contact_label.setter('text_size'))
        contact_section.add_widget(contact_label)
        
        # Contact field - FUNCTIONAL input
        self.contact_field = self.create_functional_input(
            icon='\\uf0e0',
            placeholder='Email or phone number used for booking'
        )
        contact_section.add_widget(self.contact_field)
        form_card.add_widget(contact_section)
        
        # PIN section
        pin_section = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        pin_section.bind(minimum_height=pin_section.setter('height'))
        
        # PIN label with icon
        pin_label = Label(
            text='[font=FontAwesome]\\uf292[/font] [b]Security PIN[/b]',
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=dp(35),
            color=(0/255, 77/255, 122/255, 1),
            halign='left',
            valign='middle'
        )
        pin_label.bind(size=pin_label.setter('text_size'))
        pin_section.add_widget(pin_label)
        
        # PIN field - FUNCTIONAL input with password
        self.pin_field = self.create_functional_input(
            icon='\\uf292',
            placeholder='Enter your 4-digit security PIN',
            is_password=True,
            input_filter='int'
        )
        pin_section.add_widget(self.pin_field)
        form_card.add_widget(pin_section)
        
        # Unlock button section
        button_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(20))
        button_section.bind(minimum_height=button_section.setter('height'))
        
        self.unlock_button = StyledButton(
            '[font=FontAwesome]\\uf09c[/font] UNLOCK MY LOCKER',
            button_type='primary'
        )
        self.unlock_button.size_hint_y = None
        self.unlock_button.height = dp(70)
        self.unlock_button.font_size = '22sp'
        self.unlock_button.markup = True
        self.unlock_button.bind(on_press=self.unlock_locker)
        button_section.add_widget(self.unlock_button)
        
        form_card.add_widget(button_section)
        content_scroll.add_widget(form_card)
        
        # Add some spacing
        content_scroll.add_widget(Widget(size_hint_y=None, height=dp(30)))
        
        # FOOTER SECTION with security badges
        footer_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(20))
        footer_section.bind(minimum_height=footer_section.setter('height'))
        
        # Security message
        security_text = Label(
            text='[font=FontAwesome]\\uf023[/font] [size=16sp][b]Bank-level security[/b] • Your data is encrypted and protected[/size]',
            markup=True,
            size_hint_y=None,
            height=dp(35),
            color=(0/255, 150/255, 0, 1),
            halign='center',
            valign='middle'
        )
        security_text.bind(size=security_text.setter('text_size'))
        footer_section.add_widget(security_text)
        
        # Trust badges in horizontal layout
        badges_layout = BoxLayout(orientation='horizontal', size_hint_y=None, spacing=dp(40))
        badges_layout.bind(minimum_height=badges_layout.setter('height'))
        badges_layout.size_hint_x = None
        badges_layout.width = dp(300)
        
        # Center the badges
        badges_container = BoxLayout(orientation='horizontal', size_hint_y=None)
        badges_container.bind(minimum_height=badges_container.setter('height'))
        badges_container.add_widget(Widget())  # Left spacer
        
        # SSL badge
        ssl_badge = Label(
            text='[font=FontAwesome]\\uf084[/font]\\n[size=14sp]SSL[/size]',
            markup=True,
            size_hint=(None, None),
            size=(dp(60), dp(50)),
            color=(0/255, 150/255, 0, 1),
            halign='center',
            valign='middle'
        )
        ssl_badge.bind(size=ssl_badge.setter('text_size'))
        badges_layout.add_widget(ssl_badge)
        
        # Secure badge
        secure_badge = Label(
            text='[font=FontAwesome]\\uf132[/font]\\n[size=14sp]SECURE[/size]',
            markup=True,
            size_hint=(None, None),
            size=(dp(80), dp(50)),
            color=(0/255, 150/255, 0, 1),
            halign='center',
            valign='middle'
        )
        secure_badge.bind(size=secure_badge.setter('text_size'))
        badges_layout.add_widget(secure_badge)
        
        # Verified badge
        verified_badge = Label(
            text='[font=FontAwesome]\\uf00c[/font]\\n[size=14sp]VERIFIED[/size]',
            markup=True,
            size_hint=(None, None),
            size=(dp(80), dp(50)),
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
        
        # Add final spacing
        content_scroll.add_widget(Widget(size_hint_y=None, height=dp(40)))
        
        main_container.add_widget(content_scroll)
        self.add_widget(main_container)
        
        # Set backward compatibility references for form functionality
        self.contact_input = self.contact_field
        self.pin_input = self.pin_field
    
    def create_functional_input(self, icon, placeholder, is_password=False, input_filter=None):
        """Create a functional input field that actually works"""
        # Container for the input
        input_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(65))
        input_container.spacing = dp(15)
        input_container.padding = [dp(15), dp(10)]
        
        # Icon container
        icon_container = BoxLayout(size_hint_x=None, width=dp(50))
        icon_label = Label(
            text=f'[font=FontAwesome]{icon}[/font]',
            markup=True,
            font_size='22sp',
            color=(0/255, 77/255, 122/255, 1),
            halign='center',
            valign='middle'
        )
        icon_label.bind(size=icon_label.setter('text_size'))
        icon_container.add_widget(icon_label)
        
        # Input field - THIS IS THE IMPORTANT PART
        text_input = TextInput(
            hint_text=placeholder,
            font_size='18sp',
            multiline=False,
            password=is_password,
            input_filter=input_filter,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0/255, 77/255, 122/255, 1),
            selection_color=(0/255, 77/255, 122/255, 0.3),
            padding=[dp(15), dp(15)]
        )
        
        # Container background with border
        with input_container.canvas.before:
            Color(1, 1, 1, 1)  # White background
            input_container.bg_rect = RoundedRectangle(
                pos=input_container.pos, 
                size=input_container.size, 
                radius=[dp(12)]
            )
            Color(200/255, 200/255, 200/255, 1)  # Border color
            input_container.border_rect = RoundedRectangle(
                pos=input_container.pos, 
                size=input_container.size, 
                radius=[dp(12)],
                source=''
            )
        
        input_container.bind(pos=self._update_input_bg, size=self._update_input_bg)
        
        # Focus change handler
        def on_focus_change(instance, focus):
            with input_container.canvas.before:
                if focus:
                    Color(0/255, 77/255, 122/255, 1)  # Blue border when focused
                else:
                    Color(200/255, 200/255, 200/255, 1)  # Gray border when not focused
                input_container.border_rect = RoundedRectangle(
                    pos=input_container.pos, 
                    size=input_container.size, 
                    radius=[dp(12)]
                )
        
        text_input.bind(focus=on_focus_change)
        
        input_container.add_widget(icon_container)
        input_container.add_widget(text_input)
        
        # Store the actual TextInput widget as an attribute
        input_container.text_input = text_input
        input_container.text = property(lambda self: text_input.text, lambda self, value: setattr(text_input, 'text', value))
        
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

'''
    
    # Encontrar onde começa e termina a classe atual
    start_marker = 'class UnlockLockerScreen(BaseScreen):'
    start_index = content.find(start_marker)
    
    if start_index != -1:
        # Encontrar o fim da classe (próxima classe)
        remaining_content = content[start_index:]
        next_class_index = remaining_content.find('\\nclass ', 1)
        
        if next_class_index != -1:
            end_index = start_index + next_class_index
        else:
            end_index = len(content)
        
        # Substituir a classe
        new_content = content[:start_index] + new_class + content[end_index:]
        
        # Escrever o arquivo atualizado
        with open('lockerscreens.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ UnlockLockerScreen corrigida com sucesso!")
        print(f"Classe anterior: {end_index - start_index} caracteres")
        print(f"Nova classe: {len(new_class)} caracteres")
        print("🔧 Corrigido:")
        print("   - Posicionamento do botão Back no canto superior esquerdo")
        print("   - Título centralizado no header")
        print("   - Cores profissionais ajustadas")
        print("   - Footer bem posicionado com badges")
        print("   - Campos de input FUNCIONAIS para digitação")
    else:
        print("❌ Classe UnlockLockerScreen não encontrada")

if __name__ == "__main__":
    fix_unlock_screen()