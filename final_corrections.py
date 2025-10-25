#!/usr/bin/env python3
"""
Correções específicas pedidas pelo usuário:
1. Manter subtítulo com cadeado na posição boa
2. Mover botão Unlock My Locker mais para baixo
3. Corrigir cores dos botões para amarelo definitivamente
"""

import os

def fix_final_issues():
    """Aplicar correções finais específicas"""
    
    # Ler o arquivo atual
    with open('lockerscreens.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. CORRIGIR CORES DOS BOTÕES definitivamente
    # Adicionar background_color transparente para sobrescrever cor padrão
    
    # Botão Back
    old_back_def = '''        # YELLOW Back button - positioned in top left corner
        back_btn = Button(
            text='[font=FontAwesome]\\uf060[/font] Back',
            markup=True,
            font_size='16sp',
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            color=(0, 0, 0, 1)  # Black text
        )'''
    
    new_back_def = '''        # YELLOW Back button - positioned in top left corner
        back_btn = Button(
            text='[font=FontAwesome]\\uf060[/font] Back',
            markup=True,
            font_size='16sp',
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            color=(0, 0, 0, 1),  # Black text
            background_color=(0, 0, 0, 0)  # Transparent to use Canvas background
        )'''
    
    content = content.replace(old_back_def, new_back_def)
    
    # Botão Unlock
    old_unlock_def = '''        # YELLOW UNLOCK BUTTON!
        self.unlock_button = Button(
            text='[font=FontAwesome]\\uf09c[/font] UNLOCK MY LOCKER',
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=dp(60),
            color=(0, 0, 0, 1)  # Black text on yellow
        )'''
    
    new_unlock_def = '''        # YELLOW UNLOCK BUTTON!
        self.unlock_button = Button(
            text='[font=FontAwesome]\\uf09c[/font] UNLOCK MY LOCKER',
            markup=True,
            font_size='20sp',
            size_hint_y=None,
            height=dp(60),
            color=(0, 0, 0, 1),  # Black text on yellow
            background_color=(0, 0, 0, 0)  # Transparent to use Canvas background
        )'''
    
    content = content.replace(old_unlock_def, new_unlock_def)
    
    # 2. MOVER BOTÃO UNLOCK MY LOCKER MAIS PARA BAIXO
    # Adicionar mais espaço antes do botão
    
    old_button_section = '''        # Unlock button section
        button_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(12))
        button_section.bind(minimum_height=button_section.setter('height'))'''
    
    new_button_section = '''        # Unlock button section - MOVED DOWN
        button_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(12))
        button_section.bind(minimum_height=button_section.setter('height'))
        
        # Add extra spacing to push button down
        button_section.add_widget(Widget(size_hint_y=None, height=dp(40)))'''
    
    content = content.replace(old_button_section, new_button_section)
    
    # 3. MELHORAR MÉTODOS DE UPDATE PARA GARANTIR COR AMARELA
    old_back_update = '''    def _update_back_button_bg(self, instance, value):
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
    
    new_back_update = '''    def _update_back_button_bg(self, instance, value):
        """Update back button background to keep yellow"""
        with instance.canvas.before:
            instance.canvas.before.clear()
            Color(1, 204/255, 0, 1)  # Force bright yellow
            instance.bg_rect = RoundedRectangle(
                pos=instance.pos, 
                size=instance.size, 
                radius=[dp(8)]
            )'''
    
    content = content.replace(old_back_update, new_back_update)
    
    old_unlock_update = '''    def _update_unlock_button_bg(self, instance, value):
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
    
    new_unlock_update = '''    def _update_unlock_button_bg(self, instance, value):
        """Update unlock button background to keep yellow"""
        with instance.canvas.before:
            instance.canvas.before.clear()
            Color(1, 204/255, 0, 1)  # Force bright yellow
            instance.bg_rect = RoundedRectangle(
                pos=instance.pos, 
                size=instance.size, 
                radius=[dp(8)]
            )'''
    
    content = content.replace(old_unlock_update, new_unlock_update)
    
    # Salvar o arquivo corrigido
    with open('lockerscreens.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Correções aplicadas:")
    print("   🔴 Subtítulo com cadeado mantido na posição correta")
    print("   🔻 Botão 'Unlock My Locker' movido mais para baixo")
    print("   🟡 Botões corrigidos para amarelo definitivamente")
    print("   🎨 Background transparente + Canvas amarelo forçado")

if __name__ == "__main__":
    try:
        fix_final_issues()
        print("\n🎯 Correções aplicadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro: {e}")