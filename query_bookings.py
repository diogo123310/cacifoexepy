#!/usr/bin/env python3
"""Script para consultar reservas anteriores na base de dados SQLite"""

import sqlite3
from datetime import datetime, timedelta

def query_all_bookings():
    """Consulta todas as reservas"""
    conn = sqlite3.connect('locker_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            id,
            locker_number,
            contact,
            status,
            booking_time,
            unlock_time,
            return_time,
            notes
        FROM bookings 
        ORDER BY booking_time DESC
    ''')
    
    results = cursor.fetchall()
    
    print("=== TODAS AS RESERVAS ===")
    print(f"{'ID':<4} {'Locker':<8} {'Contact':<25} {'Status':<12} {'Booking Time':<20} {'Unlock Time':<20} {'Return Time':<20}")
    print("-" * 120)
    
    for row in results:
        id_val, locker, contact, status, booking_time, unlock_time, return_time, notes = row
        unlock_str = unlock_time[:19] if unlock_time else "N/A"
        return_str = return_time[:19] if return_time else "N/A"
        
        print(f"{id_val:<4} {locker:<8} {contact:<25} {status:<12} {booking_time[:19]:<20} {unlock_str:<20} {return_str:<20}")
    
    conn.close()
    return results

def query_bookings_by_locker(locker_number):
    """Consulta reservas de um locker específico"""
    conn = sqlite3.connect('locker_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            id,
            contact,
            status,
            booking_time,
            unlock_time,
            return_time,
            notes
        FROM bookings 
        WHERE locker_number = ?
        ORDER BY booking_time DESC
    ''', (locker_number,))
    
    results = cursor.fetchall()
    
    print(f"=== RESERVAS DO LOCKER {locker_number} ===")
    for row in results:
        id_val, contact, status, booking_time, unlock_time, return_time, notes = row
        print(f"\nID: {id_val}")
        print(f"Contact: {contact}")
        print(f"Status: {status}")
        print(f"Booking Time: {booking_time}")
        print(f"Unlock Time: {unlock_time or 'N/A'}")
        print(f"Return Time: {return_time or 'N/A'}")
        if notes:
            print(f"Notes: {notes}")
        print("-" * 40)
    
    conn.close()
    return results

def query_recent_bookings(days=7):
    """Consulta reservas dos últimos X dias"""
    conn = sqlite3.connect('locker_system.db')
    cursor = conn.cursor()
    
    date_limit = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        SELECT 
            id,
            locker_number,
            contact,
            status,
            booking_time,
            unlock_time,
            return_time
        FROM bookings 
        WHERE booking_time >= ?
        ORDER BY booking_time DESC
    ''', (date_limit,))
    
    results = cursor.fetchall()
    
    print(f"=== RESERVAS DOS ÚLTIMOS {days} DIAS ===")
    for row in results:
        id_val, locker, contact, status, booking_time, unlock_time, return_time = row
        print(f"ID: {id_val} | Locker: {locker} | Contact: {contact} | Status: {status} | Time: {booking_time}")
    
    conn.close()
    return results

def query_by_contact(contact_search):
    """Consulta reservas por contacto"""
    conn = sqlite3.connect('locker_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            id,
            locker_number,
            contact,
            status,
            booking_time,
            unlock_time,
            return_time
        FROM bookings 
        WHERE contact LIKE ?
        ORDER BY booking_time DESC
    ''', (f'%{contact_search}%',))
    
    results = cursor.fetchall()
    
    print(f"=== RESERVAS PARA CONTACTO: {contact_search} ===")
    for row in results:
        id_val, locker, contact, status, booking_time, unlock_time, return_time = row
        print(f"ID: {id_val} | Locker: {locker} | Contact: {contact} | Status: {status}")
        print(f"   Booking: {booking_time}")
        print(f"   Unlock: {unlock_time or 'N/A'}")
        print(f"   Return: {return_time or 'N/A'}")
        print()
    
    conn.close()
    return results

def query_active_bookings():
    """Consulta apenas reservas ativas"""
    conn = sqlite3.connect('locker_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            id,
            locker_number,
            contact,
            booking_time,
            unlock_time
        FROM bookings 
        WHERE status = 'active'
        ORDER BY booking_time DESC
    ''')
    
    results = cursor.fetchall()
    
    print("=== RESERVAS ATIVAS ===")
    if results:
        for row in results:
            id_val, locker, contact, booking_time, unlock_time = row
            print(f"ID: {id_val} | Locker: {locker} | Contact: {contact}")
            print(f"   Booked: {booking_time}")
            print(f"   Unlocked: {unlock_time or 'Não desbloqueado'}")
            print()
    else:
        print("Nenhuma reserva ativa encontrada.")
    
    conn.close()
    return results

def get_booking_statistics():
    """Estatísticas das reservas"""
    conn = sqlite3.connect('locker_system.db')
    cursor = conn.cursor()
    
    # Total de reservas
    cursor.execute('SELECT COUNT(*) FROM bookings')
    total_bookings = cursor.fetchone()[0]
    
    # Reservas por status
    cursor.execute('SELECT status, COUNT(*) FROM bookings GROUP BY status')
    status_counts = cursor.fetchall()
    
    # Locker mais utilizado
    cursor.execute('''
        SELECT locker_number, COUNT(*) as count 
        FROM bookings 
        GROUP BY locker_number 
        ORDER BY count DESC 
        LIMIT 1
    ''')
    most_used = cursor.fetchone()
    
    # Reservas por dia (últimos 7 dias)
    cursor.execute('''
        SELECT DATE(booking_time) as date, COUNT(*) as count
        FROM bookings 
        WHERE booking_time >= date('now', '-7 days')
        GROUP BY DATE(booking_time)
        ORDER BY date DESC
    ''')
    daily_counts = cursor.fetchall()
    
    print("=== ESTATÍSTICAS DAS RESERVAS ===")
    print(f"Total de reservas: {total_bookings}")
    print("\nReservas por status:")
    for status, count in status_counts:
        print(f"  {status}: {count}")
    
    if most_used:
        print(f"\nLocker mais utilizado: {most_used[0]} ({most_used[1]} reservas)")
    
    print("\nReservas por dia (últimos 7 dias):")
    for date, count in daily_counts:
        print(f"  {date}: {count} reservas")
    
    conn.close()

def main():
    """Menu principal para consultas"""
    while True:
        print("\n" + "="*50)
        print("CONSULTA DE RESERVAS - SISTEMA DE CACIFOS")
        print("="*50)
        print("1. Todas as reservas")
        print("2. Reservas por locker")
        print("3. Reservas recentes (últimos 7 dias)")
        print("4. Reservas por contacto")
        print("5. Reservas ativas")
        print("6. Estatísticas")
        print("0. Sair")
        print("="*50)
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == '1':
            query_all_bookings()
        elif choice == '2':
            locker = input("Número do locker (001-004): ").strip()
            query_bookings_by_locker(locker)
        elif choice == '3':
            days = input("Número de dias (default 7): ").strip()
            days = int(days) if days.isdigit() else 7
            query_recent_bookings(days)
        elif choice == '4':
            contact = input("Contacto a procurar: ").strip()
            query_by_contact(contact)
        elif choice == '5':
            query_active_bookings()
        elif choice == '6':
            get_booking_statistics()
        elif choice == '0':
            break
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()