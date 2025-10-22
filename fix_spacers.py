#!/usr/bin/env python3
"""
Script para substituir todos os BoxLayout() espaçadores por Widget() transparentes
para eliminar os quadrados misteriosos que aparecem em diferentes resoluções.
"""

import re

def fix_spacers():
    file_path = "lockerscreens.py"
    
    # Ler o conteúdo do arquivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar import do Widget no topo se não existir
    if "from kivy.uix.widget import Widget" not in content:
        # Procurar por outras importações do kivy
        kivy_import_pattern = r'(from kivy\.uix\.\w+ import \w+)'
        match = re.search(kivy_import_pattern, content)
        if match:
            # Inserir após a primeira importação kivy encontrada
            insert_pos = match.end()
            content = content[:insert_pos] + '\nfrom kivy.uix.widget import Widget' + content[insert_pos:]
    
    # Padrões para substituir
    replacements = [
        # BoxLayout com parâmetros específicos
        (r'BoxLayout\(size_hint_y=None, height=dp\((\d+)\)\)', r'Widget(size_hint_y=None, height=dp(\1))'),
        (r'BoxLayout\(size_hint_y=([\d.]+)\)', r'Widget(size_hint_y=\1)'),
        # BoxLayout vazio
        (r'BoxLayout\(\)', r'Widget()'),
    ]
    
    # Aplicar substituições
    original_content = content
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Contar quantas substituições foram feitas
    changes = len(re.findall(r'Widget\(', content)) - len(re.findall(r'Widget\(', original_content))
    
    # Escrever o conteúdo modificado de volta
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Substituídos {changes} BoxLayout espaçadores por Widget transparentes")
    print("🎯 Quadrados misteriosos devem ter sido eliminados!")
    
    return changes

if __name__ == "__main__":
    fix_spacers()