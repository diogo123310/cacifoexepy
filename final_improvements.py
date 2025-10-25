#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar melhorias finais à interface profissional
"""

def add_final_professional_touches():
    """Adiciona toques finais profissionais à interface"""
    
    file_path = r"c:\Users\Diogo\OneDrive\Ambiente de Trabalho\cacifoexepy\cacifoexepy-1\lockerscreens.py"
    
    # Ler o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Melhorar textos com mais contexto e informações úteis
    improvements = {
        "Enter your credentials to unlock your reserved locker": 
        "Provide your booking details to securely access your locker",
        
        "Email or Phone (+351 123 456 789)": 
        "Email address or phone number used for booking",
        
        "4-digit PIN": 
        "Enter your 4-digit security PIN",
        
        "Your data is secure and encrypted. We never store personal information.":
        "🔒 Bank-level security • Your data is encrypted and never stored permanently",
        
        "Unlock My Locker":
        "🔓 Unlock My Locker"
    }
    
    # Aplicar melhorias
    for old_text, new_text in improvements.items():
        content = content.replace(old_text, new_text)
    
    # Adicionar mais ícones FontAwesome onde apropriado
    content = content.replace(
        "'🔒 Bank-level security",
        "'[font=FontAwesome]\\uf023[/font] Bank-level security"
    )
    
    # Escrever o arquivo atualizado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ Melhorias finais aplicadas à interface profissional!")

if __name__ == "__main__":
    add_final_professional_touches()