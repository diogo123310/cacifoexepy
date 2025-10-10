#!/usr/bin/env python3
"""
Script para limpar e otimizar a base de dados dos cacifos
Resolve locks pendentes e otimiza performance
"""

import sqlite3
import os
import shutil
from datetime import datetime

def cleanup_database(db_path="locker_system.db"):
    """Limpa e otimiza a base de dados"""
    
    print(f"🧹 Iniciando limpeza da base de dados: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Base de dados não encontrada!")
        return False
    
    # Fazer backup
    backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup criado: {backup_path}")
    except Exception as e:
        print(f"⚠️  Falha ao criar backup: {e}")
    
    try:
        # Conectar à base de dados
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.execute('PRAGMA journal_mode = WAL')
        conn.execute('PRAGMA synchronous = NORMAL')
        conn.execute('PRAGMA temp_store = MEMORY')
        conn.execute('PRAGMA mmap_size = 268435456')  # 256MB
        
        cursor = conn.cursor()
        
        print("📊 Estado atual da base de dados:")
        
        # Verificar integrity
        cursor.execute('PRAGMA integrity_check')
        integrity = cursor.fetchone()[0]
        print(f"   Integridade: {integrity}")
        
        # Estatísticas antes da limpeza
        cursor.execute('SELECT COUNT(*) FROM lockers')
        total_lockers = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM bookings WHERE status = "active"')
        active_bookings = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM system_logs')
        total_logs = cursor.fetchone()[0]
        
        print(f"   Total cacifos: {total_lockers}")
        print(f"   Reservas ativas: {active_bookings}")
        print(f"   Logs totais: {total_logs}")
        
        # Operações de limpeza
        print("\n🔧 Executando operações de limpeza...")
        
        # 1. Remover logs antigos (mais de 30 dias)
        cursor.execute('''
            DELETE FROM system_logs 
            WHERE timestamp < datetime('now', '-30 days')
        ''')
        deleted_logs = cursor.rowcount
        print(f"   Removidos {deleted_logs} logs antigos")
        
        # 2. Verificar consistência de dados
        cursor.execute('''
            SELECT l.locker_number, l.status, 
                   (SELECT COUNT(*) FROM bookings b 
                    WHERE b.locker_number = l.locker_number AND b.status = 'active') as active_count
            FROM lockers l
        ''')
        
        inconsistencies = 0
        for row in cursor.fetchall():
            locker_num, status, active_count = row
            if status == 'occupied' and active_count == 0:
                # Cacifo marcado como ocupado mas sem reserva ativa
                cursor.execute('''
                    UPDATE lockers SET status = 'available', updated_at = CURRENT_TIMESTAMP
                    WHERE locker_number = ?
                ''', (locker_num,))
                inconsistencies += 1
                print(f"   Corrigida inconsistência no cacifo {locker_num}")
            elif status == 'available' and active_count > 0:
                # Cacifo marcado como disponível mas com reserva ativa
                cursor.execute('''
                    UPDATE lockers SET status = 'occupied', updated_at = CURRENT_TIMESTAMP
                    WHERE locker_number = ?
                ''', (locker_num,))
                inconsistencies += 1
                print(f"   Corrigida inconsistência no cacifo {locker_num}")
        
        # 3. Confirmar mudanças antes da otimização
        conn.commit()
        
        # 4. Otimização da base de dados (fora da transação)
        print("   Executando VACUUM...")
        conn.execute('VACUUM')
        
        print("   Atualizando estatísticas...")
        conn.execute('ANALYZE')
        
        # Verificar estado final
        cursor.execute('SELECT COUNT(*) FROM system_logs')
        final_logs = cursor.fetchone()[0]
        
        cursor.execute('SELECT locker_number, status FROM lockers ORDER BY locker_number')
        final_status = cursor.fetchall()
        
        print(f"\n📈 Estado final:")
        print(f"   Logs após limpeza: {final_logs}")
        print(f"   Inconsistências corrigidas: {inconsistencies}")
        print(f"   Estado dos cacifos:")
        for locker, status in final_status:
            print(f"     Cacifo {locker}: {status}")
        
        conn.close()
        
        print(f"\n✅ Limpeza concluída com sucesso!")
        print(f"   Backup disponível em: {backup_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a limpeza: {e}")
        return False

def check_database_locks(db_path="locker_system.db"):
    """Verifica se existem locks pendentes na base de dados"""
    
    print(f"🔍 Verificando locks na base de dados: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Base de dados não encontrada!")
        return False
    
    try:
        # Tentar várias conexões para verificar locks
        connections = []
        
        for i in range(5):
            try:
                conn = sqlite3.connect(db_path, timeout=1.0)
                conn.execute('BEGIN IMMEDIATE')
                connections.append(conn)
                print(f"   Conexão {i+1}: ✅ OK")
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    print(f"   Conexão {i+1}: ❌ LOCKED")
                    break
                else:
                    print(f"   Conexão {i+1}: ❌ ERRO: {e}")
                    break
        
        # Fechar todas as conexões
        for conn in connections:
            conn.rollback()
            conn.close()
        
        if len(connections) == 5:
            print("✅ Nenhum lock detectado - base de dados funcional")
            return True
        else:
            print("⚠️  Possíveis locks detectados")
            return False
    
    except Exception as e:
        print(f"❌ Erro ao verificar locks: {e}")
        return False

def reset_database(db_path="locker_system.db"):
    """Reset completo da base de dados (CUIDADO!)"""
    
    response = input(f"⚠️  ATENÇÃO: Isto irá apagar TODOS os dados em {db_path}!\nContinuar? (digite 'SIM' para confirmar): ")
    
    if response != 'SIM':
        print("❌ Operação cancelada")
        return False
    
    try:
        if os.path.exists(db_path):
            # Backup antes do reset
            backup_path = f"{db_path}.pre_reset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(db_path, backup_path)
            print(f"✅ Backup criado: {backup_path}")
            
            # Remover base de dados
            os.remove(db_path)
            print(f"✅ Base de dados removida: {db_path}")
        
        # Recriar base de dados limpa
        from database import LockerDatabase
        db = LockerDatabase(db_path)
        db.init_database()
        
        print("✅ Nova base de dados criada e inicializada")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante reset: {e}")
        return False

def main():
    print("🗄️  UTILITÁRIO DE MANUTENÇÃO DA BASE DE DADOS")
    print("=" * 50)
    
    while True:
        print("\nOpções disponíveis:")
        print("1. Verificar locks")
        print("2. Limpeza e otimização")
        print("3. Reset completo (PERIGOSO!)")
        print("4. Sair")
        
        choice = input("\nEscolha uma opção (1-4): ").strip()
        
        if choice == "1":
            check_database_locks()
        elif choice == "2":
            cleanup_database()
        elif choice == "3":
            reset_database()
        elif choice == "4":
            print("👋 Adeus!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()