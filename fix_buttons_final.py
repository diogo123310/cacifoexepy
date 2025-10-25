#!/usr/bin/env python3
"""
Script para corrigir definitivamente as cores dos botões e reduzir espaço em branco
"""

import os

def fix_unlock_screen_final():
    """Corrige cores dos botões e posicionamento final"""
    
    # Ler o arquivo atual
    with open('lockerscreens.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Corrigir o botão de voltar para ter background amarelo consistente
    old_back_button = '''        # YELLOW Back button - positioned in top left corner
        back_btn = Button(
            text='[font=FontAwesome]\\uf060[/font] Back',
            markup=True,
            font_size='16sp',
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            color=(0, 0, 0, 1)  # Black text
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
        back_btn.bind(on_press=self.go_back)'''
    
    new_back_button = '''        # YELLOW Back button - positioned in top left corner
        back_btn = Button(
            text='[font=FontAwesome]\\uf060[/font] Back',
            markup=True,
            font_size='16sp',
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            color=(0, 0, 0, 1),  # Black text
            background_color=(0, 0, 0, 0)  # Transparent default background
        )
        
        # YELLOW background for back button
        with back_btn.canvas.before:
            Color(1, 204/255, 0, 1)  # Bright yellow background
            back_btn.bg_rect = RoundedRectangle(
                pos=back_btn.pos, 
                size=back_btn.size, 
                radius=[dp(8)]
            )
        back_btn.bind(pos=self._update_back_button_bg, size=self._update_back_button_bg)
        back_btn.bind(on_press=self.go_back)'''
    
    content = content.replace(old_back_button, new_back_button)
    
    # 2. Corrigir o botão de unlock para ter background amarelo consistente
    old_unlock_button = '''        # YELLOW UNLOCK BUTTON!
        self.unlock_button = Button(
            text='[font=FontAwesome]\\uf09c[/font] UNLOCK MY LOCKER',
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=dp(60),
            color=(0, 0, 0, 1)  # Black text on yellow
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
        self.unlock_button.bind(on_press=self.unlock_locker)'''
    
    new_unlock_button = '''        # YELLOW UNLOCK BUTTON!
        self.unlock_button = Button(
            text='[font=FontAwesome]\\uf09c[/font] UNLOCK MY LOCKER',
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=dp(60),
            color=(0, 0, 0, 1),  # Black text on yellow
            background_color=(0, 0, 0, 0)  # Transparent default background
        )
        
        # YELLOW background for unlock button
        with self.unlock_button.canvas.before:
            Color(1, 204/255, 0, 1)  # Bright yellow background
            self.unlock_button.bg_rect = RoundedRectangle(
                pos=self.unlock_button.pos, 
                size=self.unlock_button.size, 
                radius=[dp(8)]
            )
        self.unlock_button.bind(pos=self._update_unlock_button_bg, size=self._update_unlock_button_bg)
        self.unlock_button.bind(on_press=self.unlock_locker)'''
    
    content = content.replace(old_unlock_button, new_unlock_button)
    
    # 3. Reduzir espaço em branco removendo o Widget flexível e ajustando heights
    old_spacing = '''        form_card.add_widget(button_section)
        content_scroll.add_widget(form_card)
        
        # Add flexible spacing to push footer down
        content_scroll.add_widget(Widget(size_hint_y=1))  # This will expand to fill space
        
        # FOOTER SECTION - BOTTOM positioned
        footer_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        footer_section.bind(minimum_height=footer_section.setter('height'))'''
    
    new_spacing = '''        form_card.add_widget(button_section)
        content_scroll.add_widget(form_card)
        
        # Add moderate spacing to separate content from footer
        content_scroll.add_widget(Widget(size_hint_y=None, height=dp(40)))
        
        # FOOTER SECTION - positioned closer to content
        footer_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        footer_section.bind(minimum_height=footer_section.setter('height'))'''
    
    content = content.replace(old_spacing, new_spacing)
    
    # 4. Melhorar os métodos de update dos backgrounds
    old_back_method = '''    def _update_back_button_bg(self, instance, value):
        """Update back button background to keep yellow"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size'''
    
    new_back_method = '''    def _update_back_button_bg(self, instance, value):
        """Update back button background to keep yellow"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
            # Ensure yellow color is maintained
            with instance.canvas.before:
                Color(1, 204/255, 0, 1)  # Bright yellow
                instance.bg_rect = RoundedRectangle(
                    pos=instance.pos, 
                    size=instance.size, 
                    radius=[dp(8)]
                )'''
    
    content = content.replace(old_back_method, new_back_method)
    
    old_unlock_method = '''    def _update_unlock_button_bg(self, instance, value):
        """Update unlock button background to keep yellow"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size'''
    
    new_unlock_method = '''    def _update_unlock_button_bg(self, instance, value):
        """Update unlock button background to keep yellow"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
            # Ensure yellow color is maintained
            with instance.canvas.before:
                Color(1, 204/255, 0, 1)  # Bright yellow
                instance.bg_rect = RoundedRectangle(
                    pos=instance.pos, 
                    size=instance.size, 
                    radius=[dp(8)]
                )'''
    
    content = content.replace(old_unlock_method, new_unlock_method)
    
    # Gravar o arquivo corrigido
    with open('lockerscreens.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Correções aplicadas com sucesso!")
    print("   - Botões com background amarelo consistente")
    print("   - Background transparente para evitar sobreposição")
    print("   - Espaço em branco reduzido")
    print("   - Footer mais próximo do conteúdo")

if __name__ == "__main__":
    try:
        fix_unlock_screen_final()
        print("\n🎯 Script executado com sucesso!")
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")