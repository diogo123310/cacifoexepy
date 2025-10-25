#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir nomes das classes FontAwesome
"""

def fix_fontawesome_class_names():
    """Corrige os nomes das classes FontAwesome removendo espaços"""
    
    file_path = r"c:\Users\Diogo\OneDrive\Ambiente de Trabalho\cacifoexepy\cacifoexepy-1\lockerscreens.py"
    
    # Ler o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Corrigir nomes de classes com espaço
    content = content.replace("FontAwesome IconTextField", "FontAwesome IconTextField")
    content = content.replace("FontAwesome Button", "FontAwesome Button")  
    content = content.replace("FontAwesome Label", "FontAwesome Label")
    
    # Escrever o arquivo atualizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ Nomes das classes FontAwesome corrigidos!")

if __name__ == "__main__":
    fix_fontawesome_class_names()