#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar uma versão completamente nova e profissional da UnlockLockerScreen
"""

def create_professional_unlock_screen():
    """Cria uma nova versão profissional da UnlockLockerScreen"""
    
    replacement_code = '''
class UnlockLockerScreen(BaseScreen):
    def __init__(self, manager, **kwargs):
        # Remove gpio_controller from kwargs before calling super()
        self.gpio_controller = kwargs.pop('gpio_controller', None)
        
        # Initialize base screen
        super().__init__(manager, title="Unlock Locker", **kwargs)
        
        # Database reference
        self.db = self.gpio_controller.db if self.gpio_controller else None
        
        # Recreate the entire interface from scratch
        self.rebuild_professional_interface()
        
        # Set references for backward compatibility
        self.contact_input = self.contact_field.text_input if hasattr(self, 'contact_field') else None
        self.pin_input = self.pin_field.text_input if hasattr(self, 'pin_field') else None
    
    def rebuild_professional_interface(self):
        """Build the complete professional interface"""
        # Clear everything and start fresh
        self.clear_widgets()
        
        # Create new main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(20)],
            spacing=dp(25)
        )
        
        # Add professional header with large FontAwesome icon
        header = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(15))
        header.bind(minimum_height=header.setter('height'))
        
        # Large icon and title
        icon_title = Label(
            text='[size=40][font=FontAwesome]\\uf09c[/font][/size]\\n[size=24][b]Unlock Your Locker[/b][/size]',
            markup=True,
            size_hint_y=None,
            height=dp(90),
            halign='center',
            color=(0/255, 77/255, 122/255, 1)
        )
        icon_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        header.add_widget(icon_title)
        
        # Subtitle
        subtitle = Label(
            text='[color=666666]Enter your booking details below[/color]',
            markup=True,
            font_size='16sp',
            size_hint_y=None,
            height=dp(25),
            halign='center'
        )
        subtitle.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        header.add_widget(subtitle)
        
        main_layout.add_widget(header)
        
        # Professional form in a card
        form_card = ProfessionalCard()
        
        # Contact section
        contact_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        contact_section.bind(minimum_height=contact_section.setter('height'))
        
        contact_label = Label(
            text='[font=FontAwesome]\\uf0e0[/font] Contact Information',
            markup=True,
            font_size='18sp',
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        contact_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        contact_section.add_widget(contact_label)
        
        self.contact_field = IconTextField(
            icon_unicode='\\uf0e0',
            hint_text='Email or phone number used for booking'
        )
        contact_section.add_widget(self.contact_field)
        form_card.add_widget(contact_section)
        
        # PIN section
        pin_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        pin_section.bind(minimum_height=pin_section.setter('height'))
        
        pin_label = Label(
            text='[font=FontAwesome]\\uf292[/font] Security PIN',
            markup=True,
            font_size='18sp',
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 77/255, 122/255, 1),
            halign='left'
        )
        pin_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        pin_section.add_widget(pin_label)
        
        self.pin_field = IconTextField(
            icon_unicode='\\uf292',
            hint_text='Enter your 4-digit PIN',
            is_password=True,
            input_filter='int'
        )
        pin_section.add_widget(self.pin_field)
        form_card.add_widget(pin_section)
        
        # Big professional button
        button_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(15))
        button_section.bind(minimum_height=button_section.setter('height'))
        
        self.unlock_button = StyledButton(
            '[font=FontAwesome]\\uf09c[/font] UNLOCK MY LOCKER',
            button_type='primary'
        )
        self.unlock_button.height = dp(65)
        self.unlock_button.font_size = '20sp'
        self.unlock_button.markup = True
        self.unlock_button.bind(on_press=self.unlock_locker)
        button_section.add_widget(self.unlock_button)
        
        form_card.add_widget(button_section)
        main_layout.add_widget(form_card)
        
        # Security badges
        security_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        security_layout.bind(minimum_height=security_layout.setter('height'))
        
        # Security text
        security_text = Label(
            text='[font=FontAwesome]\\uf023[/font] Bank-level encryption • Your data is secure',
            markup=True,
            font_size='14sp',
            size_hint_y=None,
            height=dp(30),
            color=(0/255, 150/255, 0, 1),
            halign='center'
        )
        security_text.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        security_layout.add_widget(security_text)
        
        # Trust badges row
        badges_row = BoxLayout(orientation='horizontal', size_hint_y=None, spacing=dp(20))
        badges_row.bind(minimum_height=badges_row.setter('height'))
        
        badges = [
            ('[font=FontAwesome]\\uf084[/font] SSL', 'SSL Encrypted'),
            ('[font=FontAwesome]\\uf132[/font] SECURE', 'Verified Secure'),
            ('[font=FontAwesome]\\uf00c[/font] TRUSTED', 'Trusted System')
        ]
        
        for icon_text, tooltip in badges:
            badge = Label(
                text=icon_text,
                markup=True,
                font_size='12sp',
                size_hint_y=None,
                height=dp(25),
                color=(0/255, 150/255, 0, 1),
                halign='center'
            )
            badges_row.add_widget(badge)
        
        security_layout.add_widget(badges_row)
        main_layout.add_widget(security_layout)
        
        # Add back button manually since we cleared everything
        back_button = StyledButton('< Back', button_type='secondary')
        back_button.size_hint_y = None
        back_button.height = dp(50)
        back_button.bind(on_press=self.go_back)
        
        # Create final layout with back button at top
        final_layout = BoxLayout(orientation='vertical')
        
        # Header with back button
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        header_layout.add_widget(back_button)
        header_layout.add_widget(Widget())  # spacer
        
        final_layout.add_widget(header_layout)
        final_layout.add_widget(main_layout)
        
        self.add_widget(final_layout)
    
    def go_back(self, instance):
        """Go back to previous screen"""
        print("Going back from unlock_locker")
        if self.manager:
            self.manager.current = 'home'
'''
    
    return replacement_code

if __name__ == "__main__":
    code = create_professional_unlock_screen()
    print("Código gerado com sucesso!")
    print("Tamanho:", len(code), "caracteres")