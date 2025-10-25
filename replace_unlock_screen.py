#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para substituir completamente a UnlockLockerScreen
"""

def replace_unlock_screen():
    """Substitui a classe UnlockLockerScreen por uma versão profissional"""
    
    # Ler o arquivo atual
    with open('lockerscreens.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nova implementação profissional da UnlockLockerScreen
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
        """Create the complete professional interface"""
        # Main container
        main_container = BoxLayout(orientation='vertical')
        
        # Header with back button
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        header.spacing = dp(10)
        header.padding = [dp(20), dp(10)]
        
        # Back button
        back_btn = StyledButton('< Back', button_type='secondary')
        back_btn.size_hint_x = None
        back_btn.width = dp(100)
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        
        # Title in header
        title_label = Label(
            text='Unlock Locker',
            font_size='24sp',
            color=(1, 1, 1, 1),
            halign='center'
        )
        header.add_widget(title_label)
        header.add_widget(Widget())  # spacer
        
        # Header background
        with header.canvas.before:
            Color(0/255, 77/255, 122/255, 1)  # Blue background
            header.bg_rect = RoundedRectangle(pos=header.pos, size=header.size)
        header.bind(pos=self._update_header_bg, size=self._update_header_bg)
        
        main_container.add_widget(header)
        
        # Content area
        content_scroll = BoxLayout(orientation='vertical')
        content_scroll.padding = [dp(30), dp(30)]
        content_scroll.spacing = dp(30)
        
        # Hero section with big icon
        hero_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(15))
        hero_section.bind(minimum_height=hero_section.setter('height'))
        
        # Big FontAwesome icon
        hero_icon = Label(
            text='[font=FontAwesome]\\uf09c[/font]',
            markup=True,
            font_size='60sp',
            size_hint_y=None,
            height=dp(80),
            color=(0/255, 77/255, 122/255, 1),
            halign='center'
        )
        hero_section.add_widget(hero_icon)
        
        # Main title
        hero_title = Label(
            text='[b]Access Your Locker[/b]',
            markup=True,
            font_size='32sp',
            size_hint_y=None,
            height=dp(40),
            color=(0/255, 77/255, 122/255, 1),
            halign='center'
        )
        hero_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        hero_section.add_widget(hero_title)
        
        # Subtitle
        hero_subtitle = Label(
            text='Enter your booking details below to unlock your reserved locker',
            font_size='16sp',
            size_hint_y=None,
            height=dp(25),
            color=(0.5, 0.5, 0.5, 1),
            halign='center'
        )
        hero_subtitle.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        hero_section.add_widget(hero_subtitle)
        
        content_scroll.add_widget(hero_section)
        
        # Form card
        form_card = ProfessionalCard()
        
        # Contact section
        contact_section = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=None)
        contact_section.bind(minimum_height=contact_section.setter('height'))
        
        # Contact label with icon
        contact_label = Label(
            text='[font=FontAwesome]\\uf0e0[/font] [b]Contact Information[/b]',
            markup=True,
            font_size='18sp',
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        contact_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        contact_section.add_widget(contact_label)
        
        # Contact field
        self.contact_field = IconTextField(
            icon_unicode='\\uf0e0',
            hint_text='Email or phone number used for booking'
        )
        contact_section.add_widget(self.contact_field)
        form_card.add_widget(contact_section)
        
        # PIN section
        pin_section = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=None)
        pin_section.bind(minimum_height=pin_section.setter('height'))
        
        # PIN label with icon
        pin_label = Label(
            text='[font=FontAwesome]\\uf292[/font] [b]Security PIN[/b]',
            markup=True,
            font_size='18sp',
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        pin_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        pin_section.add_widget(pin_label)
        
        # PIN field
        self.pin_field = IconTextField(
            icon_unicode='\\uf292',
            hint_text='Enter your 4-digit security PIN',
            is_password=True,
            input_filter='int'
        )
        pin_section.add_widget(self.pin_field)
        form_card.add_widget(pin_section)
        
        # Unlock button
        button_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(15))
        button_section.bind(minimum_height=button_section.setter('height'))
        
        self.unlock_button = StyledButton(
            '[font=FontAwesome]\\uf09c[/font] UNLOCK MY LOCKER',
            button_type='primary'
        )
        self.unlock_button.height = dp(70)
        self.unlock_button.font_size = '22sp'
        self.unlock_button.markup = True
        self.unlock_button.bind(on_press=self.unlock_locker)
        button_section.add_widget(self.unlock_button)
        
        form_card.add_widget(button_section)
        content_scroll.add_widget(form_card)
        
        # Security section
        security_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(15))
        security_section.bind(minimum_height=security_section.setter('height'))
        
        # Security text
        security_text = Label(
            text='[font=FontAwesome]\\uf023[/font] Bank-level security • Your data is encrypted and protected',
            markup=True,
            font_size='14sp',
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 150/255, 0, 1),
            halign='center'
        )
        security_text.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        security_section.add_widget(security_text)
        
        # Trust badges
        badges_layout = BoxLayout(orientation='horizontal', size_hint_y=None, spacing=dp(30))
        badges_layout.bind(minimum_height=badges_layout.setter('height'))
        
        # SSL badge
        ssl_badge = Label(
            text='[font=FontAwesome]\\uf084[/font]\\nSSL',
            markup=True,
            font_size='14sp',
            size_hint_y=None,
            height=dp(40),
            color=(0/255, 150/255, 0, 1),
            halign='center'
        )
        badges_layout.add_widget(ssl_badge)
        
        # Secure badge
        secure_badge = Label(
            text='[font=FontAwesome]\\uf132[/font]\\nSECURE',
            markup=True,
            font_size='14sp',
            size_hint_y=None,
            height=dp(40),
            color=(0/255, 150/255, 0, 1),
            halign='center'
        )
        badges_layout.add_widget(secure_badge)
        
        # Verified badge
        verified_badge = Label(
            text='[font=FontAwesome]\\uf00c[/font]\\nVERIFIED',
            markup=True,
            font_size='14sp',
            size_hint_y=None,
            height=dp(40),
            color=(0/255, 150/255, 0, 1),
            halign='center'
        )
        badges_layout.add_widget(verified_badge)
        
        security_section.add_widget(badges_layout)
        content_scroll.add_widget(security_section)
        
        main_container.add_widget(content_scroll)
        self.add_widget(main_container)
        
        # Set backward compatibility references
        self.contact_input = self.contact_field.text_input
        self.pin_input = self.pin_field.text_input
    
    def _update_header_bg(self, instance, value):
        """Update header background position"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
    
    def go_back(self, instance):
        """Go back to home screen"""
        print("Going back from unlock_locker")
        if self.manager:
            self.manager.current = 'home'
    
    def reset_form(self, instance):
        """Reset form fields"""
        print("Executing reset_form - clearing fields")
        if hasattr(self, 'contact_input') and self.contact_input:
            self.contact_input.text = ""
        if hasattr(self, 'pin_input') and self.pin_input:
            self.pin_input.text = ""
    
    def update_translations(self):
        """Update translations (placeholder)"""
        pass

    def unlock_locker(self, instance):
        """Function to unlock locker using database"""
        contact = self.contact_input.text.strip() if self.contact_input else ""
        pin = self.pin_input.text.strip() if self.pin_input else ""
        
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
        
        print("✅ UnlockLockerScreen substituída com sucesso!")
        print(f"Classe original: {end_index - start_index} caracteres")
        print(f"Nova classe: {len(new_class)} caracteres")
    else:
        print("❌ Classe UnlockLockerScreen não encontrada")

if __name__ == "__main__":
    replace_unlock_screen()