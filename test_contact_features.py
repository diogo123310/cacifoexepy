#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das novas funcionalidades de contacto
============================================
Script para testar se a base de dados foi atualizada corretamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import LockerDatabase
import sqlite3

def test_database_schema():
    """Testa se o schema da base de dados foi atualizado"""
    print("🔍 Testando schema da base de dados...")
    
    db = LockerDatabase()
    
    # Verificar se as colunas existem
    try:
        conn = sqlite3.connect('locker_system.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(bookings)")
        columns = cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        print(f"📋 Colunas encontradas: {column_names}")
        
        required_columns = ['name', 'email', 'phone', 'birth_date']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"❌ Colunas em falta: {missing_columns}")
            return False
        else:
            print("✅ Todas as colunas necessárias estão presentes")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao verificar schema: {e}")
        return False
    finally:
        conn.close()

def test_booking_functionality():
    """Testa a nova funcionalidade de reserva"""
    print("\n🧪 Testando funcionalidade de reserva...")
    
    db = LockerDatabase()
    
    # Dados de teste
    test_user_data = {
        'name': 'João Teste',
        'email': 'joao.teste@email.com',
        'phone': '+351 912345678',
        'birth_date': '15/03/1990'
    }
    
    try:
        # Verificar cacifos disponíveis
        lockers_status = db.get_all_lockers_status()
        available_lockers = [locker for locker, status in lockers_status.items() if status == 'available']
        
        if not available_lockers:
            print("⚠️ Nenhum cacifo disponível. A libertar cacifo 001 para teste...")
            # Libertar cacifo para teste
            db.return_locker('001', 'Test cleanup')
            test_locker = '001'
        else:
            test_locker = available_lockers[0]
            
        print(f"🔧 Usando cacifo {test_locker} para teste")
        
        # Criar reserva de teste
        result = db.book_locker(test_locker, contact=None, user_data=test_user_data)
        
        if result.get('success'):
            print(f"✅ Reserva criada com sucesso: {result}")
            
            # Verificar se os dados foram salvos corretamente
            bookings = db.get_all_bookings(limit=1)
            if bookings:
                booking = bookings[0]
                print(f"📋 Dados salvos: Nome={booking.get('name')}, Email={booking.get('email')}, Telefone={booking.get('phone')}")
                
                # Testar pesquisa
                search_results = db.get_bookings_by_contact('João')
                if search_results:
                    print("✅ Pesquisa por nome funcionando")
                else:
                    print("❌ Pesquisa por nome não funcionou")
                
                search_results = db.get_bookings_by_contact('joao.teste@email.com')
                if search_results:
                    print("✅ Pesquisa por email funcionando")
                else:
                    print("❌ Pesquisa por email não funcionou")
                    
                return True
            else:
                print("❌ Não foi possível recuperar dados da reserva")
                return False
        else:
            print(f"❌ Falha ao criar reserva: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False

def main():
    print("🧪 TESTE DAS NOVAS FUNCIONALIDADES DE CONTACTO")
    print("=" * 50)
    
    # Teste 1: Schema da base de dados
    schema_ok = test_database_schema()
    
    # Teste 2: Funcionalidade de reserva
    booking_ok = test_booking_functionality()
    
    print("\n📊 RESUMO DOS TESTES")
    print("=" * 50)
    print(f"Schema da base de dados: {'✅ OK' if schema_ok else '❌ FALHOU'}")
    print(f"Funcionalidade de reserva: {'✅ OK' if booking_ok else '❌ FALHOU'}")
    
    if schema_ok and booking_ok:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O sistema está pronto para mostrar informações detalhadas de contacto")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM")
        print("❌ Verifique os erros acima")

if __name__ == "__main__":
    main()