#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para implementar FontAwesome de forma simples
Apenas converte emojis em títulos, mantendo componentes originais
"""

def simple_fontawesome_implementation():
    """Implementa FontAwesome de forma simples convertendo apenas emojis em títulos"""
    
    file_path = r"c:\Users\Diogo\OneDrive\Ambiente de Trabalho\cacifoexepy\cacifoexepy-1\lockerscreens.py"
    
    # Ler o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Converter apenas os emojis nos títulos e textos para FontAwesome
    # Mantemos os componentes originais (IconTextField, StyledButton) para evitar problemas
    
    emoji_to_fontawesome = {
        '🔓': '[font=FontAwesome]\\uf09c[/font]',  # unlock
        '📧': '[font=FontAwesome]\\uf0e0[/font]',  # envelope
        '🔢': '[font=FontAwesome]\\uf292[/font]',  # hashtag
        '✅': '[font=FontAwesome]\\uf00c[/font]',  # check
        '⚠️': '[font=FontAwesome]\\uf071[/font]',  # warning
        '🔒': '[font=FontAwesome]\\uf023[/font]',  # lock
    }
    
    # Aplicar conversões apenas em textos de títulos e labels
    for emoji, fontawesome in emoji_to_fontawesome.items():
        # Converter nos títulos e labels, mas não nos componentes
        content = content.replace(f"'{emoji}", f"'{fontawesome}")
        content = content.replace(f'"{emoji}', f'"{fontawesome}')
        content = content.replace(f'[b]{emoji}', f'[b]{fontawesome}')
    
    # Escrever o arquivo atualizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ FontAwesome implementado de forma simples e segura!")

if __name__ == "__main__":
    simple_fontawesome_implementation()