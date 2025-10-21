#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Booking Queries - Sistema de Consulta de Reservas Anteriores
============================================================

Script para consultar o histórico de reservas do sistema de cacifos
com várias opções de filtragem e análise.

Uso:
    python booking_queries.py

Funcionalidades:
- Consultar todas as reservas
- Filtrar por locker específico
- Pesquisar por contacto
- Ver reservas recentes
- Obter estatísticas detalhadas
"""

import os
import sys
from datetime import datetime, timedelta
from database import LockerDatabase


class BookingQuerySystem:
    """Sistema de consulta de reservas com interface de menu"""
    
    def __init__(self):
        self.db = LockerDatabase()
        
    def display_menu(self):
        """Mostra o menu principal"""
        print("\n" + "="*60)
        print("  SISTEMA DE CONSULTA DE RESERVAS ANTERIORES")
        print("="*60)
        print("1. Ver todas as reservas")
        print("2. Consultar por locker específico")
        print("3. Pesquisar por contacto")
        print("4. Ver reservas recentes (últimos 7 dias)")
        print("5. Ver reservas ativas")
        print("6. Estatísticas do sistema")
        print("7. Exportar dados para CSV")
        print("0. Sair")
        print("="*60)
        
    def format_booking(self, booking: dict) -> str:
        """Formata uma reserva para exibição"""
        lines = []
        lines.append(f"ID: {booking['id']} | Locker: {booking['locker_number']} | Status: {booking['status']}")
        lines.append(f"Contacto: {booking['contact']}")
        
        # Mostrar PIN se disponível
        if booking.get('pin'):
            lines.append(f"PIN: {booking['pin']}")
        
        lines.append(f"Reservado: {booking['booking_time']}")
        
        if booking['unlock_time']:
            lines.append(f"Desbloqueado: {booking['unlock_time']}")
        if booking['return_time']:
            lines.append(f"Devolvido: {booking['return_time']}")
        if booking['notes']:
            lines.append(f"Notas: {booking['notes']}")
            
        return "\n".join(lines)
    
    def display_bookings(self, bookings: list, title: str = "Reservas"):
        """Exibe uma lista de reservas formatada"""
        print(f"\n{title}")
        print("-" * len(title))
        
        if not bookings:
            print("Nenhuma reserva encontrada.")
            return
            
        print(f"Total: {len(bookings)} reservas\n")
        
        for i, booking in enumerate(bookings, 1):
            print(f"[{i}] {self.format_booking(booking)}")
            print("-" * 40)
    
    def query_all_bookings(self):
        """Consulta todas as reservas"""
        try:
            limit = input("\nLimitar resultados (Enter para todas): ").strip()
            limit = int(limit) if limit.isdigit() else None
            
            bookings = self.db.get_all_bookings(limit=limit)
            title = f"Todas as Reservas{f' (últimas {limit})' if limit else ''}"
            self.display_bookings(bookings, title)
            
        except Exception as e:
            print(f"Erro ao consultar reservas: {e}")
    
    def query_by_locker(self):
        """Consulta reservas por locker específico"""
        try:
            locker_number = input("\nNúmero do locker: ").strip()
            if not locker_number:
                print("Número do locker é obrigatório.")
                return
                
            bookings = self.db.get_bookings_by_locker(locker_number)
            self.display_bookings(bookings, f"Histórico do Locker {locker_number}")
            
        except Exception as e:
            print(f"Erro ao consultar locker: {e}")
    
    def query_by_contact(self):
        """Consulta reservas por contacto"""
        try:
            contact = input("\nContacto (pesquisa parcial): ").strip()
            if not contact:
                print("Contacto é obrigatório.")
                return
                
            bookings = self.db.get_bookings_by_contact(contact)
            self.display_bookings(bookings, f"Reservas para '{contact}'")
            
        except Exception as e:
            print(f"Erro ao pesquisar contacto: {e}")
    
    def query_recent_bookings(self):
        """Consulta reservas recentes"""
        try:
            days_input = input("\nNúmero de dias (padrão 7): ").strip()
            days = int(days_input) if days_input.isdigit() else 7
            
            bookings = self.db.get_recent_bookings(days=days)
            self.display_bookings(bookings, f"Reservas dos Últimos {days} Dias")
            
        except Exception as e:
            print(f"Erro ao consultar reservas recentes: {e}")
    
    def query_active_bookings(self):
        """Consulta reservas ativas"""
        try:
            bookings = self.db.get_all_bookings()
            active_bookings = [b for b in bookings if b['status'] in ['booked', 'unlocked']]
            self.display_bookings(active_bookings, "Reservas Ativas")
            
        except Exception as e:
            print(f"Erro ao consultar reservas ativas: {e}")
    
    def show_statistics(self):
        """Mostra estatísticas do sistema"""
        try:
            stats = self.db.get_booking_statistics()
            
            print("\n" + "="*50)
            print("  ESTATÍSTICAS DO SISTEMA")
            print("="*50)
            
            print(f"Total de reservas: {stats['total_bookings']}")
            print()
            
            print("Distribuição por status:")
            for status, count in stats['status_counts'].items():
                print(f"  {status}: {count}")
            print()
            
            if stats['most_used_locker']:
                most_used = stats['most_used_locker']
                print(f"Locker mais utilizado: {most_used['locker']} ({most_used['count']} reservas)")
                print()
            
            if stats['average_duration_hours'] > 0:
                print(f"Tempo médio de utilização: {stats['average_duration_hours']:.2f} horas")
                print()
            
            if stats['daily_counts']:
                print("Atividade dos últimos 7 dias:")
                for date, count in stats['daily_counts'].items():
                    print(f"  {date}: {count} reservas")
            
            print("="*50)
            
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
    
    def export_to_csv(self):
        """Exporta dados para CSV"""
        try:
            import csv
            from datetime import datetime
            
            filename = f"reservas_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            bookings = self.db.get_all_bookings()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'locker_number', 'contact', 'pin', 'status', 
                             'booking_time', 'unlock_time', 'return_time', 'notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for booking in bookings:
                    writer.writerow(booking)
            
            print(f"\nDados exportados para: {filename}")
            print(f"Total de registos: {len(bookings)}")
            
        except Exception as e:
            print(f"Erro ao exportar dados: {e}")
    
    def run(self):
        """Executa o sistema de consultas"""
        print("Bem-vindo ao Sistema de Consulta de Reservas!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEscolha uma opção: ").strip()
                
                if choice == '0':
                    print("\nObrigado por usar o sistema!")
                    break
                elif choice == '1':
                    self.query_all_bookings()
                elif choice == '2':
                    self.query_by_locker()
                elif choice == '3':
                    self.query_by_contact()
                elif choice == '4':
                    self.query_recent_bookings()
                elif choice == '5':
                    self.query_active_bookings()
                elif choice == '6':
                    self.show_statistics()
                elif choice == '7':
                    self.export_to_csv()
                else:
                    print("\nOpção inválida. Tente novamente.")
                    
                if choice != '0':
                    input("\nPressione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\nSaindo...")
                break
            except Exception as e:
                print(f"\nErro inesperado: {e}")
                input("\nPressione Enter para continuar...")


def main():
    """Função principal"""
    # Verifica se a base de dados existe
    if not os.path.exists('locker_system.db'):
        print("ERRO: Base de dados 'locker_system.db' não encontrada!")
        print("Certifique-se de que está no diretório correto.")
        return
    
    # Inicia o sistema de consultas
    query_system = BookingQuerySystem()
    query_system.run()


if __name__ == "__main__":
    main()