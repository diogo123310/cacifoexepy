#!/usr/bin/env python3
"""
Teste para verificar se o problema de database lock foi resolvido
"""

import os
import time
import threading
from database import LockerDatabase
import tempfile

def test_concurrent_bookings():
    """Testa reservas concorrentes para verificar locks"""
    
    # Usar base de dados temporária
    temp_db = tempfile.mktemp(suffix='.db')
    
    try:
        db = LockerDatabase(temp_db)
        db.init_database()
        
        print("🔧 Teste de reservas concorrentes iniciado...")
        
        # Resultados das threads
        results = []
        
        def book_locker_thread(thread_id, locker_num, contact, pin):
            """Função para executar numa thread"""
            try:
                result = db.book_locker(locker_num, f"{contact}_{thread_id}", f"{pin}{thread_id}")
                results.append((thread_id, result))
                print(f"Thread {thread_id}: {result}")
            except Exception as e:
                results.append((thread_id, {"success": False, "error": str(e)}))
                print(f"Thread {thread_id} erro: {e}")
        
        # Criar múltiplas threads para tentar reservar o mesmo cacifo
        threads = []
        for i in range(10):
            thread = threading.Thread(
                target=book_locker_thread, 
                args=(i, "001", "test@email.com", "123")
            )
            threads.append(thread)
        
        # Iniciar todas as threads ao mesmo tempo
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Esperar que todas terminem
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        print(f"\n📊 Resultados após {end_time - start_time:.2f} segundos:")
        
        success_count = 0
        error_count = 0
        
        for thread_id, result in results:
            if isinstance(result, dict) and result.get("success"):
                success_count += 1
                print(f"✅ Thread {thread_id}: Reserva bem-sucedida")
            else:
                error_count += 1
                if isinstance(result, dict) and "message" in result:
                    print(f"❌ Thread {thread_id}: {result['message']}")
                else:
                    print(f"❌ Thread {thread_id}: Erro desconhecido - {result}")
        
        print(f"\n📈 Resumo:")
        print(f"   Sucessos: {success_count}")
        print(f"   Erros: {error_count}")
        
        # Verificar estado da base de dados
        status = db.get_all_lockers_status()
        print(f"\n🗄️  Estado dos cacifos:")
        for locker, stat in status.items():
            print(f"   Cacifo {locker}: {stat}")
        
        # Deve haver apenas 1 sucesso (primeiro a conseguir reservar)
        if success_count == 1 and error_count == 9:
            print("\n✅ TESTE PASSOU: Apenas uma reserva foi bem-sucedida")
            return True
        else:
            print(f"\n❌ TESTE FALHOU: Esperava 1 sucesso e 9 erros, obteve {success_count} sucessos e {error_count} erros")
            return False
    
    finally:
        # Limpar ficheiro temporário
        if os.path.exists(temp_db):
            os.remove(temp_db)

def test_sequential_operations():
    """Testa operações sequenciais para verificar funcionalidade básica"""
    
    temp_db = tempfile.mktemp(suffix='.db')
    
    try:
        db = LockerDatabase(temp_db)
        db.init_database()
        
        print("\n🔧 Teste de operações sequenciais...")
        
        # Teste 1: Reservar cacifo
        print("1. Reservando cacifo 002...")
        result = db.book_locker("002", "user@test.com", "4567")
        if result and result.get("success"):
            print("✅ Reserva bem-sucedida")
        else:
            print(f"❌ Falha na reserva: {result}")
            return False
        
        # Teste 2: Verificar status
        print("2. Verificando status...")
        status = db.get_locker_status("002")
        if status == "occupied":
            print("✅ Status correto: occupied")
        else:
            print(f"❌ Status incorreto: {status}")
            return False
        
        # Teste 3: Desbloquear cacifo
        print("3. Desbloqueando cacifo...")
        unlocked = db.unlock_locker("user@test.com", "4567")
        if unlocked == "002":
            print("✅ Desbloqueio bem-sucedido")
        else:
            print(f"❌ Falha no desbloqueio: {unlocked}")
            return False
        
        # Teste 4: Devolver cacifo
        print("4. Devolvendo cacifo...")
        returned = db.return_locker("002")
        if returned:
            print("✅ Devolução bem-sucedida")
        else:
            print("❌ Falha na devolução")
            return False
        
        # Teste 5: Verificar status final
        print("5. Verificando status final...")
        final_status = db.get_locker_status("002")
        if final_status == "available":
            print("✅ Status final correto: available")
            return True
        else:
            print(f"❌ Status final incorreto: {final_status}")
            return False
    
    finally:
        if os.path.exists(temp_db):
            os.remove(temp_db)

def test_database_recovery():
    """Testa recuperação da base de dados após erro"""
    
    temp_db = tempfile.mktemp(suffix='.db')
    
    try:
        print("\n🔧 Teste de recuperação da base de dados...")
        
        # Criar primeira instância
        db1 = LockerDatabase(temp_db)
        db1.init_database()
        
        # Reservar um cacifo
        result = db1.book_locker("003", "recovery@test.com", "9999")
        if not (result and result.get("success")):
            print("❌ Falha na reserva inicial")
            return False
        
        # Criar segunda instância (simular crash e reinício)
        db2 = LockerDatabase(temp_db)
        
        # Verificar se os dados persistiram
        status = db2.get_locker_status("003")
        if status == "occupied":
            print("✅ Dados persistiram após reinício")
        else:
            print(f"❌ Dados não persistiram: {status}")
            return False
        
        # Verificar se ainda conseguimos desbloquear
        unlocked = db2.unlock_locker("recovery@test.com", "9999")
        if unlocked == "003":
            print("✅ Desbloqueio funciona após reinício")
            return True
        else:
            print(f"❌ Falha no desbloqueio após reinício: {unlocked}")
            return False
    
    finally:
        if os.path.exists(temp_db):
            os.remove(temp_db)

def main():
    print("🚀 Iniciando testes da base de dados...")
    print("=" * 50)
    
    test1_passed = test_sequential_operations()
    test2_passed = test_concurrent_bookings() 
    test3_passed = test_database_recovery()
    
    print("=" * 50)
    print("📋 RESULTADOS FINAIS:")
    print(f"   Operações Sequenciais: {'✅ PASSOU' if test1_passed else '❌ FALHOU'}")
    print(f"   Reservas Concorrentes: {'✅ PASSOU' if test2_passed else '❌ FALHOU'}")
    print(f"   Recuperação da BD:     {'✅ PASSOU' if test3_passed else '❌ FALHOU'}")
    
    all_passed = test1_passed and test2_passed and test3_passed
    
    if all_passed:
        print("\n🎉 TODOS OS TESTES PASSARAM! A base de dados está a funcionar corretamente.")
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM. Verifique a implementação da base de dados.")
    
    return all_passed

if __name__ == "__main__":
    main()