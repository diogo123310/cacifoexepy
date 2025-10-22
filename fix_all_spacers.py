#!/usr/bin/env python3
"""
Script para substituir todos os BoxLayout() espaçadores por Widget() transparentes
em todos os arquivos Python para eliminar os quadrados misteriosos.
"""

import re
import os

def fix_spacers_in_file(file_path):
    """Fix spacers in a specific file"""
    # Ler o conteúdo do arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar import do Widget no topo se não existir
    if "from kivy.uix.widget import Widget" not in content and "BoxLayout(" in content:
        # Procurar por outras importações do kivy
        kivy_import_pattern = r'(from kivy\.uix\.\w+ import \w+)'
        match = re.search(kivy_import_pattern, content)
        if match:
            # Inserir após a primeira importação kivy encontrada
            insert_pos = match.end()
            content = content[:insert_pos] + '\nfrom kivy.uix.widget import Widget' + content[insert_pos:]
    
    # Padrões para substituir APENAS espaçadores (BoxLayout sem parâmetros de layout)
    replacements = [
        # BoxLayout usado apenas como espaçador com altura específica
        (r'BoxLayout\(size_hint_y=None, height=dp\((\d+)\)\)', r'Widget(size_hint_y=None, height=dp(\1))'),
        # BoxLayout usado apenas como espaçador com size_hint
        (r'BoxLayout\(size_hint_y=([\d.]+)\)', r'Widget(size_hint_y=\1)'),
        # BoxLayout usado apenas como espaçador com largura
        (r'BoxLayout\(size_hint_x=([\d.]+)\)', r'Widget(size_hint_x=\1)'),
        # BoxLayout vazio - usado como espaçador
        (r'BoxLayout\(\)', r'Widget()'),
    ]
    
    # Aplicar substituições
    original_content = content
    changes = 0
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            changes += len(re.findall(pattern, content))
            content = new_content
    
    # Escrever apenas se houve mudanças
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    
    return 0

def fix_all_spacers():
    """Fix spacers in all relevant files"""
    files_to_fix = [
        "lockerscreens.py",
        "contact_pin_screen.py"
    ]
    
    total_changes = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            changes = fix_spacers_in_file(file_path)
            if changes > 0:
                print(f"✅ {file_path}: Substituídos {changes} BoxLayout espaçadores por Widget transparentes")
                total_changes += changes
    
    if total_changes > 0:
        print(f"\n🎯 Total: {total_changes} espaçadores convertidos para Widget transparentes!")
        print("🚀 Quadrados misteriosos devem ter sido eliminados!")
    else:
        print("ℹ️ Nenhum espaçador BoxLayout encontrado para converter.")
    
    return total_changes

if __name__ == "__main__":
    fix_all_spacers()