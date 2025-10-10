#!/usr/bin/env python3
"""Script para limpar a base de dados e deixar todos os lockers disponíveis"""

import sqlite3
from database import LockerDatabase

def main():
    print("=== LIMPEZA DA BASE DE DADOS ===")
    
    # Conectar à base de dados
    conn = sqlite3.connect('locker_system.db')
    cursor = conn.cursor()
    
    # Verificar estado atual - TODAS as reservas
    print("\n--- Estado Atual (Todas as reservas) ---")
    cursor.execute('SELECT id, locker_number, contact, status, booking_time FROM bookings ORDER BY booking_time DESC')
    all_bookings = cursor.fetchall()
    
    if all_bookings:
        print("Todas as reservas encontradas:")
        for booking in all_bookings:
            print(f"  ID: {booking[0]}, Locker: {booking[1]}, Contact: {booking[2]}, Status: {booking[3]}, Time: {booking[4]}")
    else:
        print("Nenhuma reserva encontrada.")
    
    # Verificar reservas ativas especificamente
    print("\n--- Reservas Ativas ---")
    cursor.execute('SELECT id, locker_number, contact, status, booking_time FROM bookings WHERE status = "active"')
    active_bookings = cursor.fetchall()
    
    if active_bookings:
        print("Reservas ativas encontradas:")
        for booking in active_bookings:
            print(f"  ID: {booking[0]}, Locker: {booking[1]}, Contact: {booking[2]}, Status: {booking[3]}, Time: {booking[4]}")
    else:
        print("Nenhuma reserva ativa encontrada.")
    
    # Limpar TODAS as reservas ativas
    print("\n--- Limpando Reservas ---")
    cursor.execute('UPDATE bookings SET status = "returned" WHERE status = "active"')
    updated_count = cursor.rowcount
    
    if updated_count > 0:
        print(f"✅ {updated_count} reserva(s) marcada(s) como devolvida(s)")
        conn.commit()
    else:
        print("✅ Nenhuma reserva ativa para limpar")
    
    # Limpar TAMBÉM a tabela lockers
    print("\n--- Limpando Tabela Lockers ---")
    cursor.execute('SELECT locker_number, status FROM lockers')
    locker_states = cursor.fetchall()
    
    print("Estados atuais dos lockers:")
    for locker in locker_states:
        print(f"  Locker {locker[0]}: {locker[1]}")
    
    cursor.execute('UPDATE lockers SET status = "available"')
    updated_lockers = cursor.rowcount
    
    if updated_lockers > 0:
        print(f"✅ {updated_lockers} locker(s) marcado(s) como disponível(eis)")
        conn.commit()
    else:
        print("✅ Todos os lockers já estavam disponíveis")
    
    # Verificar estado final
    print("\n--- Estado Final ---")
    cursor.execute('SELECT id, locker_number, contact, status, booking_time FROM bookings WHERE status = "active"')
    remaining_bookings = cursor.fetchall()
    
    if remaining_bookings:
        print("❌ Ainda existem reservas ativas:")
        for booking in remaining_bookings:
            print(f"  ID: {booking[0]}, Locker: {booking[1]}, Contact: {booking[2]}, Status: {booking[3]}, Time: {booking[4]}")
    else:
        print("✅ Todos os lockers estão agora disponíveis!")
    
    conn.close()
    print("\n=== LIMPEZA CONCLUÍDA ===")
    print("Agora pode executar o programa principal - todos os lockers estarão disponíveis (verdes)")

if __name__ == "__main__":
    main()