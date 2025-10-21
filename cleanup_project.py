#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleanup_project.py - Remove ficheiros de teste desnecessários
============================================================
Script para limpar o projeto, removendo ficheiros de teste e temporários,
mantendo apenas os ficheiros essenciais do sistema.
"""

import os
import shutil
from datetime import datetime

def cleanup_test_files():
    """Remove ficheiros de teste e temporários"""
    
    # Ficheiros de teste para remover
    test_files = [
        'test_pin_display.py',
        'test_api.py', 
        'demo_pin_queries.py',
        'update_old_pins.py',
        'test_auto_pin_system.py',
        'test_database_independent.py',
        'test_database_lock_fix.py',
        'test_database.py',
        'test_final_application.py',
        'test_final_production.py',
        'test_pin_display.py',
        'test_popup_realtime.py',
        'test_pulse_gpio.py',
        'test_pulse_integration.py',
        'gpio_simulation_demo.py',
        'database_demo.py',
        'database_maintenance.py',
        'start_web_interface.py'
    ]
    
    # Ficheiros de backup antigos para remover
    backup_files = [
        file for file in os.listdir('.') 
        if file.startswith('locker_system.db.backup_') and file.endswith('.db')
    ]
    
    # Pastas de teste para remover
    test_folders = [
        '__pycache__',
        '.pytest_cache',
        'tests',
        'temp'
    ]
    
    print("🧹 LIMPEZA DO PROJETO LOCKER SYSTEM")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    removed_files = []
    removed_folders = []
    
    # Remover ficheiros de teste
    print("📁 Removendo ficheiros de teste...")
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                removed_files.append(file)
                print(f"   ✅ {file}")
            except Exception as e:
                print(f"   ❌ Erro ao remover {file}: {e}")
        else:
            print(f"   ℹ️  {file} (já não existe)")
    
    # Remover backups antigos
    print("\n🗄️  Removendo backups antigos...")
    for file in backup_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                removed_files.append(file)
                print(f"   ✅ {file}")
            except Exception as e:
                print(f"   ❌ Erro ao remover {file}: {e}")
    
    # Remover pastas de cache
    print("\n📂 Removendo pastas de cache...")
    for folder in test_folders:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                removed_folders.append(folder)
                print(f"   ✅ {folder}/")
            except Exception as e:
                print(f"   ❌ Erro ao remover pasta {folder}: {e}")
        else:
            print(f"   ℹ️  {folder}/ (já não existe)")
    
    return removed_files, removed_folders

def list_remaining_files():
    """Lista ficheiros que permanecem no projeto"""
    
    # Ficheiros essenciais do núcleo
    essential_files = {
        'main.py': 'Aplicação principal do sistema',
        'homescreen.py': 'Tela inicial da aplicação', 
        'lockerscreens.py': 'Interface dos cacifos',
        'contact_pin_screen.py': 'Tela de reserva/contacto',
        'database.py': 'Gestão da base de dados',
        'locker_system.db': 'Base de dados SQLite'
    }
    
    # Ficheiros da interface web
    web_files = {
        'database_api.py': 'Servidor web e API REST',
        'start_web.bat': 'Script de início automático'
    }
    
    # Ficheiros úteis de administração
    admin_files = {
        'booking_queries.py': 'Sistema de consulta de reservas',
        'query_bookings.py': 'Consultas da base de dados',
        'clear_database.py': 'Limpeza da base de dados',
        'remote_client.py': 'Cliente de acesso remoto'
    }
    
    # Ficheiros de documentação
    doc_files = {
        'requirements.txt': 'Dependências do Python',
        'README.md': 'Documentação do projeto',
        'REMOTE_ACCESS_GUIDE.md': 'Guia de acesso remoto',
        'AUTO_PIN_IMPLEMENTATION.md': 'Documentação de PINs',
        'DATABASE_LOCK_SOLUTION.md': 'Soluções de base de dados',
        'FUNCIONALIDADES_IMPLEMENTADAS.py': 'Lista de funcionalidades',
        'PULSE_IMPLEMENTATION.md': 'Implementação de pulsos',
        'REALTIME_POPUP_IMPLEMENTATION.md': 'Pop-ups em tempo real'
    }
    
    # Recursos
    resource_files = {
        'logo.png': 'Logotipo da aplicação',
        'fa-solid-900.ttf.otf': 'Fonte de ícones'
    }
    
    print("\n📋 FICHEIROS DO PROJETO:")
    print("=" * 50)
    
    def show_category(title, files, icon):
        print(f"\n{icon} {title}:")
        for file, description in files.items():
            status = "✅" if os.path.exists(file) else "❌"
            size = ""
            if os.path.exists(file):
                size_bytes = os.path.getsize(file)
                if size_bytes > 1024*1024:
                    size = f"({size_bytes/(1024*1024):.1f} MB)"
                elif size_bytes > 1024:
                    size = f"({size_bytes/1024:.1f} KB)"
                else:
                    size = f"({size_bytes} bytes)"
            print(f"   {status} {file:<25} {size:<12} - {description}")
    
    show_category("NÚCLEO ESSENCIAL", essential_files, "🎯")
    show_category("INTERFACE WEB", web_files, "🌐")
    show_category("ADMINISTRAÇÃO", admin_files, "🔧")
    show_category("DOCUMENTAÇÃO", doc_files, "📖")
    show_category("RECURSOS", resource_files, "🎨")

def create_backup_info():
    """Cria ficheiro com informação sobre a limpeza"""
    
    backup_info = f"""# Limpeza do Projeto - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Ficheiros Removidos
Esta limpeza removeu ficheiros de teste e temporários, mantendo apenas os essenciais.

## Estrutura Final do Projeto
```
cacifoexepy/
├── 🎯 NÚCLEO ESSENCIAL
│   ├── main.py                 # Aplicação principal
│   ├── homescreen.py          # Tela inicial  
│   ├── lockerscreens.py       # Interface dos cacifos
│   ├── contact_pin_screen.py  # Tela de reserva
│   ├── database.py            # Base de dados
│   └── locker_system.db       # Dados SQLite
│
├── 🌐 INTERFACE WEB
│   ├── database_api.py        # Servidor web
│   └── start_web.bat         # Início automático
│
├── 🔧 ADMINISTRAÇÃO
│   ├── booking_queries.py     # Consultas
│   ├── query_bookings.py      # Queries DB
│   ├── clear_database.py      # Limpeza DB
│   └── remote_client.py       # Cliente remoto
│
├── 📖 DOCUMENTAÇÃO
│   ├── requirements.txt       # Dependências
│   ├── REMOTE_ACCESS_GUIDE.md # Guia remoto
│   └── *.md                  # Outras docs
│
└── 🎨 RECURSOS
    ├── logo.png              # Logotipo
    └── fa-solid-900.ttf.otf  # Fonte
```

## Como Usar o Sistema

### Executar Aplicação Principal:
```bash
python main.py
```

### Iniciar Interface Web:
```bash
python database_api.py
```

### Consultar Reservas:
```bash
python booking_queries.py
```

### Acesso Web:
http://localhost:5000

## Restaurar Ficheiros
Se precisar de restaurar ficheiros removidos, verifique:
- Backup do git: `git checkout HEAD~1 -- nome_do_ficheiro.py`
- Lixeira do sistema operacional
"""
    
    with open('CLEANUP_INFO.md', 'w', encoding='utf-8') as f:
        f.write(backup_info)
    
    print("📄 Criado: CLEANUP_INFO.md (informação sobre a limpeza)")

def main():
    """Função principal"""
    
    print("🧹 LIMPEZA DO PROJETO LOCKER SYSTEM")
    print("=" * 50)
    print("Este script irá remover ficheiros de teste e temporários,")
    print("mantendo apenas os ficheiros essenciais do sistema.")
    print()
    
    # Mostrar ficheiros atuais
    all_files = [f for f in os.listdir('.') if f.endswith('.py')]
    print(f"📊 Ficheiros Python encontrados: {len(all_files)}")
    
    test_files_found = [f for f in all_files if f.startswith('test_') or f in [
        'demo_pin_queries.py', 'update_old_pins.py', 'gpio_simulation_demo.py',
        'database_demo.py', 'database_maintenance.py'
    ]]
    
    print(f"🗑️  Ficheiros de teste identificados: {len(test_files_found)}")
    
    if test_files_found:
        print("\nFicheiros de teste encontrados:")
        for file in test_files_found:
            print(f"   • {file}")
    
    print("\n" + "="*50)
    response = input("\n❓ Deseja proceder com a limpeza? (s/N): ").lower().strip()
    
    if response in ['s', 'sim', 'y', 'yes']:
        print("\n🚀 Iniciando limpeza...")
        removed_files, removed_folders = cleanup_test_files()
        
        print(f"\n📊 RESUMO DA LIMPEZA:")
        print(f"   • {len(removed_files)} ficheiros removidos")
        print(f"   • {len(removed_folders)} pastas removidas")
        
        if removed_files:
            create_backup_info()
        
        list_remaining_files()
        
        print(f"\n🎯 Projeto limpo com sucesso!")
        print(f"💡 Para executar: python main.py")
        print(f"🌐 Interface web: python database_api.py")
        
    else:
        print("\n❌ Limpeza cancelada pelo utilizador")
        list_remaining_files()
    
    print(f"\n📁 Total de ficheiros no diretório: {len(os.listdir('.'))}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Limpeza interrompida pelo utilizador")
    except Exception as e:
        print(f"\n❌ Erro durante a limpeza: {e}")
    
    print(f"\n👋 Limpeza finalizada!")