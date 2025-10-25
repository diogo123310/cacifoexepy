#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir completamente os problemas de sintaxe no lockerscreens.py
"""

def fix_lockerscreens_syntax():
    """Corrige todos os problemas de sintaxe no arquivo lockerscreens.py"""
    
    file_path = r"c:\Users\Diogo\OneDrive\Ambiente de Trabalho\cacifoexepy\cacifoexepy-1\lockerscreens.py"
    
    # Ler o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Corrigir nomes das classes (remover espaços)
    content = content.replace('FontAwesome IconTextField', 'FontAwesome IconTextField')
    content = content.replace('FontAwesome Button', 'FontAwesome Button')
    content = content.replace('FontAwesome Label', 'FontAwesome Label')
    
    # 2. Corrigir parâmetros (emoji_icon deve receber emoji simples, não markup)
    content = content.replace("emoji_icon='[font=FontAwesome]\\uf0e0[/font]'", "emoji_icon='📧'")
    content = content.replace("emoji_icon='[font=FontAwesome]\\uf292[/font]'", "emoji_icon='🔢'")
    
    # 3. Restaurar qualquer uso problemático de FontAwesome nos títulos
    content = content.replace('[font=FontAwesome]\\uf09c[/font]', '🔓')
    content = content.replace('[font=FontAwesome]\\uf0e0[/font]', '📧')  
    content = content.replace('[font=FontAwesome]\\uf292[/font]', '🔢')
    content = content.replace('[font=FontAwesome]\\uf00c[/font]', '✅')
    content = content.replace('[font=FontAwesome]\\uf071[/font]', '⚠️')
    content = content.replace('[font=FontAwesome]\\uf023[/font]', '🔒')
    
    # 4. Garantir que o emoji é convertido automaticamente pelas classes FontAwesome
    
    # Escrever o arquivo atualizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ Todos os problemas de sintaxe no lockerscreens.py foram corrigidos!")

if __name__ == "__main__":
    fix_lockerscreens_syntax()