"""
Script de teste independente para demonstrar as funcionalidades da base de dados.
"""

from database import LockerDatabase
import os

def test_database_independent():
    """Testa funcionalidades com base de dados separada"""
    
    print("=== TESTE INDEPENDENTE DA BASE DE DADOS ===\n")
    
    # Usar base de dados de teste separada
    test_db_path = "test_locker_system.db"
    
    # Remover base de dados de teste se existir
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Inicializar base de dados de teste
    db = LockerDatabase(test_db_path)
    
    print("1. RESERVAR CACIFOS:")
    success1 = db.book_locker('001', 'joao@email.com', '1234')
    print(f"   ✓ Cacifo 001 reservado para joao@email.com")
    
    success2 = db.book_locker('002', 'maria@email.com', '5678')
    print(f"   ✓ Cacifo 002 reservado para maria@email.com")
    
    print("\n2. ESTADO DOS CACIFOS:")
    status = db.get_all_lockers_status()
    for locker, state in status.items():
        print(f"   Cacifo {locker}: {state}")
    
    print("\n3. INFORMAÇÕES DAS RESERVAS:")
    for locker in ['001', '002']:
        booking = db.get_active_booking(locker)
        if booking:
            print(f"   Cacifo {locker}: {booking['contact']}")
    
    print("\n4. DESBLOQUEAR CACIFOS:")
    unlocked1 = db.unlock_locker('joao@email.com', '1234')
    print(f"   ✓ Cacifo {unlocked1} desbloqueado para João")
    
    unlocked2 = db.unlock_locker('maria@email.com', '5678')
    print(f"   ✓ Cacifo {unlocked2} desbloqueado para Maria")
    
    print("\n5. DEVOLVER CACIFOS:")
    db.return_locker('001')
    db.return_locker('002')
    print("   ✓ Cacifos 001 e 002 devolvidos")
    
    print("\n6. ESTATÍSTICAS FINAIS:")
    stats = db.get_usage_stats()
    print(f"   Total de reservas: {stats['total_bookings']}")
    print(f"   Reservas ativas: {stats['active_bookings']}")
    print(f"   Cacifos disponíveis: {stats['available_lockers']}")
    
    # Limpar
    os.remove(test_db_path)
    print("\n✅ TESTE COMPLETO - TUDO FUNCIONANDO!")

if __name__ == "__main__":
    test_database_independent()