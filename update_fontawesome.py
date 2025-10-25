#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar lockerscreens.py com componentes FontAwesome
"""

import re

def update_lockerscreens_with_fontawesome():
    """Atualiza o arquivo lockerscreens.py para usar FontAwesome"""
    
    file_path = r"c:\Users\Diogo\OneDrive\Ambiente de Trabalho\cacifoexepy\cacifoexepy-1\lockerscreens.py"
    
    # Ler o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Atualizar o título para usar FontAwesome
    content = content.replace(
        "text='[color=004D7A][b]🔓 Access Your Locker[/b][/color]'",
        "text='[color=004D7A][b][font=FontAwesome]\\uf09c[/font] Access Your Locker[/b][/color]'"
    )
    
    # 2. Substituir IconTextField por FontAwesome IconTextField - Contact field
    content = content.replace(
        "self.contact_field = IconTextField(\n            icon_text='@',\n            hint_text='Email or Phone (+351 123 456 789)'\n        )",
        "self.contact_field = FontAwesome IconTextField(\n            emoji_icon='📧',\n            hint_text='Email or Phone (+351 123 456 789)'\n        )"
    )
    
    # Variação mais simples para o contact field
    content = content.replace(
        "IconTextField(\n            icon_text='@',",
        "FontAwesome IconTextField(\n            emoji_icon='�',"
    )
    
    # 3. Substituir PIN field
    content = content.replace(
        "IconTextField(\n            icon_text='PIN',",
        "FontAwesome IconTextField(\n            emoji_icon='🔢',"
    )
    
    # 4. Atualizar botões para usar FontAwesome
    content = content.replace(
        "StyledButton(\n            'Unlock My Locker', \n            button_type='primary'\n        )",
        "FontAwesome Button(\n            emoji_text='🔓',\n            button_text='Unlock My Locker',\n            button_type='primary'\n        )"
    )
    
    # Variação mais simples para botões
    content = content.replace(
        "StyledButton(\n            'Unlock My Locker',",
        "FontAwesome Button(\n            emoji_text='🔓',\n            button_text='Unlock My Locker',"
    )
    
    # 5. Atualizar outros emojis e ícones encontrados usando replacement direto
    emoji_replacements = {
        '🔓': '[font=FontAwesome]\\uf09c[/font]',
        '📧': '[font=FontAwesome]\\uf0e0[/font]', 
        '🔢': '[font=FontAwesome]\\uf292[/font]',
        '✅': '[font=FontAwesome]\\uf00c[/font]',
        '⚠️': '[font=FontAwesome]\\uf071[/font]',
        '🔒': '[font=FontAwesome]\\uf023[/font]',
    }
    
    for emoji, fontawesome in emoji_replacements.items():
        content = content.replace(emoji, fontawesome)
    
    # Escrever o arquivo atualizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ lockerscreens.py atualizado com FontAwesome!")

if __name__ == "__main__":
    update_lockerscreens_with_fontawesome()