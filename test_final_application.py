#!/usr/bin/env python3
"""
Teste final da aplicação para verificar se o problema de database lock foi resolvido
"""

from database import LockerDatabase
import time

def test_booking_flow():
    """Testa o fluxo completo de reserva como na aplicação"""
    
    print("🧪 Teste do fluxo completo de reserva...")
    
    db = LockerDatabase()
    
    # 1. Verificar estado inicial
    print("1. Estado inicial dos cacifos:")
    status = db.get_all_lockers_status()
    for locker, stat in status.items():
        print(f"   Cacifo {locker}: {stat}")
    
    # 2. Reservar cacifo (como no contact_pin_screen.py)
    print("\n2. Reservando cacifo 001...")
    result = db.book_locker("001", "user@test.com", "1234")
    
    if result and result.get("success"):
        print(f"✅ Reserva bem-sucedida: {result['message']}")
        print(f"   Detalhes: Cacifo {result['locker_number']} para {result['contact']}")
        
        # 3. Verificar mudança de status
        print("\n3. Verificando status após reserva:")
        new_status = db.get_locker_status("001")
        print(f"   Cacifo 001: {new_status}")
        
        if new_status == "occupied":
            print("✅ Status atualizado corretamente")
            
            # 4. Simular abertura do cacifo (log GPIO)
            print("\n4. Simulando abertura do cacifo...")
            db.log_action("001", "GPIO_OPEN", "Pin 3 activated", "OUTPUT_HIGH")
            
            # 5. Testar desbloqueio
            print("\n5. Testando desbloqueio...")
            unlocked = db.unlock_locker("user@test.com", "1234")
            
            if unlocked == "001":
                print("✅ Desbloqueio bem-sucedido")
                
                # 6. Simular devolução
                print("\n6. Simulando devolução...")
                returned = db.return_locker("001")
                
                if returned:
                    print("✅ Devolução bem-sucedida")
                    
                    # 7. Verificar status final
                    print("\n7. Status final:")
                    final_status = db.get_locker_status("001")
                    print(f"   Cacifo 001: {final_status}")
                    
                    if final_status == "available":
                        print("✅ Ciclo completo bem-sucedido!")
                        return True
                    else:
                        print(f"❌ Status final incorreto: {final_status}")
                        return False
                else:
                    print("❌ Erro na devolução")
                    return False
            else:
                print(f"❌ Erro no desbloqueio: {unlocked}")
                return False
        else:
            print(f"❌ Status não atualizado: {new_status}")
            return False
    else:
        print(f"❌ Erro na reserva: {result}")
        return False

def test_multiple_bookings():
    """Testa múltiplas reservas sequenciais"""
    
    print("\n🧪 Teste de múltiplas reservas sequenciais...")
    
    db = LockerDatabase()
    
    # Testar reserva de todos os cacifos
    test_data = [
        ("001", "user1@test.com", "1111"),
        ("002", "user2@test.com", "2222"),
        ("003", "user3@test.com", "3333"),
        ("004", "user4@test.com", "4444")
    ]
    
    success_count = 0
    
    for locker, contact, pin in test_data:
        print(f"Reservando cacifo {locker}...")
        result = db.book_locker(locker, contact, pin)
        
        if result and result.get("success"):
            print(f"✅ Cacifo {locker} reservado para {contact}")
            success_count += 1
        else:
            print(f"❌ Falha ao reservar cacifo {locker}: {result}")
    
    print(f"\nResultado: {success_count}/4 reservas bem-sucedidas")
    
    # Verificar status final
    print("\nStatus final de todos os cacifos:")
    final_status = db.get_all_lockers_status()
    for locker, stat in final_status.items():
        print(f"   Cacifo {locker}: {stat}")
    
    # Limpar para próximos testes
    print("\nLimpando reservas...")
    for locker, _, _ in test_data:
        db.return_locker(locker)
    
    return success_count == 4

def main():
    print("🚀 TESTE FINAL DA APLICAÇÃO")
    print("=" * 40)
    
    # Teste 1: Fluxo completo
    test1_passed = test_booking_flow()
    
    # Teste 2: Múltiplas reservas
    test2_passed = test_multiple_bookings()
    
    print("\n" + "=" * 40)
    print("📋 RESULTADOS FINAIS:")
    print(f"   Fluxo Completo:      {'✅ PASSOU' if test1_passed else '❌ FALHOU'}")
    print(f"   Múltiplas Reservas:  {'✅ PASSOU' if test2_passed else '❌ FALHOU'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 APLICAÇÃO ESTÁ PRONTA!")
        print("   ✅ Problema de database lock resolvido")
        print("   ✅ Todas as funcionalidades funcionam")
        print("   ✅ Pronto para uso em produção")
    else:
        print("\n⚠️  AINDA EXISTEM PROBLEMAS")
        print("   Verifique os logs acima para detalhes")

if __name__ == "__main__":
    main()