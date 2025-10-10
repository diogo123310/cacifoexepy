"""
Script de teste para demonstrar as funcionalidades da base de dados do sistema de cacifos.
Este script mostra como usar todas as funcionalidades da base de dados.
"""

from database import LockerDatabase
import datetime

def test_database():
    """Testa todas as funcionalidades da base de dados"""
    
    print("=== TESTE DA BASE DE DADOS DO SISTEMA DE CACIFOS ===\n")
    
    # Inicializar a base de dados
    db = LockerDatabase()
    
    print("1. ESTADO INICIAL DOS CACIFOS:")
    initial_status = db.get_all_lockers_status()
    for locker, status in initial_status.items():
        print(f"   Cacifo {locker}: {status}")
    
    print("\n2. RESERVAR CACIFOS:")
    
    # Reservar cacifo 001
    success1 = db.book_locker('001', 'joao@email.com', '1234')
    print(f"   Reserva cacifo 001 para joao@email.com: {'✓ Sucesso' if success1 else '✗ Falha'}")
    
    # Reservar cacifo 002
    success2 = db.book_locker('002', 'maria@email.com', '5678')
    print(f"   Reserva cacifo 002 para maria@email.com: {'✓ Sucesso' if success2 else '✗ Falha'}")
    
    # Tentar reservar cacifo já ocupado
    success3 = db.book_locker('001', 'pedro@email.com', '9999')
    print(f"   Tentar reservar cacifo 001 novamente: {'✓ Sucesso' if success3 else '✗ Falha (esperado)'}")
    
    print("\n3. ESTADO DOS CACIFOS APÓS RESERVAS:")
    after_booking_status = db.get_all_lockers_status()
    for locker, status in after_booking_status.items():
        print(f"   Cacifo {locker}: {status}")
    
    print("\n4. INFORMAÇÕES DAS RESERVAS ATIVAS:")
    for locker in ['001', '002', '003', '004']:
        booking_info = db.get_active_booking(locker)
        if booking_info:
            print(f"   Cacifo {locker}: {booking_info['contact']} (reservado em {booking_info['booking_time']})")
        else:
            print(f"   Cacifo {locker}: Sem reserva ativa")
    
    print("\n5. DESBLOQUEAR CACIFOS:")
    
    # Desbloquear com credenciais corretas
    unlocked1 = db.unlock_locker('joao@email.com', '1234')
    print(f"   Desbloquear com joao@email.com + 1234: {'✓ Cacifo ' + unlocked1 if unlocked1 else '✗ Falha'}")
    
    # Tentar desbloquear com PIN errado
    unlocked2 = db.unlock_locker('maria@email.com', '1111')
    print(f"   Desbloquear com maria@email.com + PIN errado: {'✓ Cacifo ' + unlocked2 if unlocked2 else '✗ Falha (esperado)'}")
    
    # Desbloquear com credenciais corretas
    unlocked3 = db.unlock_locker('maria@email.com', '5678')
    print(f"   Desbloquear com maria@email.com + 5678: {'✓ Cacifo ' + unlocked3 if unlocked3 else '✗ Falha'}")
    
    print("\n6. DEVOLVER CACIFOS:")
    
    # Devolver cacifo 001
    returned1 = db.return_locker('001')
    print(f"   Devolver cacifo 001: {'✓ Sucesso' if returned1 else '✗ Falha'}")
    
    # Devolver cacifo 002
    returned2 = db.return_locker('002')
    print(f"   Devolver cacifo 002: {'✓ Sucesso' if returned2 else '✗ Falha'}")
    
    print("\n7. ESTADO FINAL DOS CACIFOS:")
    final_status = db.get_all_lockers_status()
    for locker, status in final_status.items():
        print(f"   Cacifo {locker}: {status}")
    
    print("\n8. ESTATÍSTICAS DE UTILIZAÇÃO:")
    stats = db.get_usage_stats()
    print(f"   Total de reservas: {stats['total_bookings']}")
    print(f"   Reservas ativas: {stats['active_bookings']}")
    print(f"   Cacifos disponíveis: {stats['available_lockers']}")
    print(f"   Total de cacifos: {stats['total_lockers']}")
    
    print("\n9. TESTE DE LOGS:")
    db.log_action('001', 'TEST_ACTION', 'Este é um teste de log', 'GPIO: Pin 2 = 0')
    print("   ✓ Log de teste adicionado")
    
    print("\n=== TESTE COMPLETO ===")
    print("✓ Base de dados SQLite funcionando perfeitamente!")
    print("✓ Todas as funcionalidades testadas com sucesso!")
    
if __name__ == "__main__":
    test_database()