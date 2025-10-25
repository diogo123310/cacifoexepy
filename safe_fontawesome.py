#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para implementar FontAwesome apenas em títulos e textos
Mantém componentes originais para garantir funcionalidade
"""

def implement_safe_fontawesome():
    """Implementa FontAwesome apenas em títulos, sem alterar componentes"""
    
    file_path = r"c:\Users\Diogo\OneDrive\Ambiente de Trabalho\cacifoexepy\cacifoexepy-1\lockerscreens.py"
    
    # Ler o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Mapeamento de emojis para FontAwesome
    emoji_to_fontawesome = {
        '🔓': '[font=FontAwesome]\\uf09c[/font]',  # unlock
        '📧': '[font=FontAwesome]\\uf0e0[/font]',  # envelope
        '🔢': '[font=FontAwesome]\\uf292[/font]',  # hashtag/number
        '✅': '[font=FontAwesome]\\uf00c[/font]',  # check
        '⚠️': '[font=FontAwesome]\\uf071[/font]',  # warning
        '🔒': '[font=FontAwesome]\\uf023[/font]',  # lock
        '💰': '[font=FontAwesome]\\uf155[/font]',  # dollar
        '🏠': '[font=FontAwesome]\\uf015[/font]',  # home
    }
    
    # Converter emojis em textos de labels, títulos e hints
    for emoji, fontawesome in emoji_to_fontawesome.items():
        # Converter em strings entre aspas (títulos, hints, etc)
        content = content.replace(f'"{emoji}', f'"{fontawesome}')
        content = content.replace(f"'{emoji}", f"'{fontawesome}")
        
        # Converter em markup específico (títulos com formatação)
        content = content.replace(f'[b]{emoji}', f'[b]{fontawesome}')
        content = content.replace(f'{emoji} ', f'{fontawesome} ')
    
    # Escrever o arquivo atualizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ FontAwesome implementado com segurança em títulos e textos!")

if __name__ == "__main__":
    implement_safe_fontawesome()