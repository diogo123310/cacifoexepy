#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote Database Client - Acesso Remoto ao Sistema de Cacifos
===========================================================

Cliente para acessar a API do sistema de cacifos remotamente.
Permite consultar reservas, estatísticas e exportar dados de qualquer computador na rede.

Uso:
    python remote_client.py

Configuração:
    1. Altere a variável RASPBERRY_PI_IP para o IP do seu Raspberry Pi
    2. Certifique-se que o servidor API está rodando (python database_api.py)
    3. Execute este script para acessar os dados remotamente
"""

import requests
import json
from datetime import datetime, timedelta
import csv
import os
from typing import List, Dict, Optional

# ============================================
# CONFIGURAÇÃO - ALTERE PARA O SEU RASPBERRY PI
# ============================================
RASPBERRY_PI_IP = "192.168.1.100"  # ⚠️ ALTERE PARA O IP DO SEU RASPBERRY PI
API_PORT = 5000
TIMEOUT = 10  # segundos

class RemoteLockerClient:
    """Cliente para acesso remoto ao sistema de cacifos"""
    
    def __init__(self, host_ip: str = RASPBERRY_PI_IP, port: int = API_PORT):
        """
        Inicializa o cliente remoto
        
        Args:
            host_ip: IP do Raspberry Pi onde está rodando a API
            port: Porta da API (padrão: 5000)
        """
        self.base_url = f"http://{host_ip}:{port}/api"
        self.web_url = f"http://{host_ip}:{port}"
        
    def test_connection(self) -> bool:
        """
        Testa a conexão com o servidor
        
        Returns:
            True se conectado, False caso contrário
        """
        try:
            response = requests.get(f"{self.base_url}/status", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Conectado ao sistema!")
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Database: {data.get('database', 'unknown')}")
                print(f"   Total de reservas: {data.get('total_bookings', 0)}")
                return True
            else:
                print(f"❌ Servidor retornou status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conexão: {e}")
            print(f"   Tentando conectar a: {self.base_url}")
            print("   Verifique se:")
            print("   • O servidor API está rodando no Raspberry Pi")
            print("   • O IP está correto")
            print("   • A rede está acessível")
            return False
    
    def get_all_bookings(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Consulta todas as reservas
        
        Args:
            limit: Limite de resultados (None para todos)
            
        Returns:
            Lista de reservas
        """
        try:
            params = {'limit': limit} if limit else {}
            response = requests.get(f"{self.base_url}/bookings", params=params, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao consultar reservas: {e}")
            return []
    
    def get_active_bookings(self) -> List[Dict]:
        """
        Consulta reservas ativas (booked, unlocked)
        
        Returns:
            Lista de reservas ativas
        """
        try:
            response = requests.get(f"{self.base_url}/bookings/active", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao consultar reservas ativas: {e}")
            return []
    
    def get_recent_bookings(self, days: int = 7) -> List[Dict]:
        """
        Consulta reservas recentes
        
        Args:
            days: Número de dias para considerar "recente"
            
        Returns:
            Lista de reservas recentes
        """
        try:
            params = {'days': days}
            response = requests.get(f"{self.base_url}/bookings/recent", params=params, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao consultar reservas recentes: {e}")
            return []
    
    def search_by_contact(self, contact: str) -> List[Dict]:
        """
        Pesquisa reservas por contacto
        
        Args:
            contact: Termo de pesquisa (busca parcial)
            
        Returns:
            Lista de reservas encontradas
        """
        try:
            response = requests.get(f"{self.base_url}/bookings/contact/{contact}", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao pesquisar contacto: {e}")
            return []
    
    def get_locker_history(self, locker_number: str) -> List[Dict]:
        """
        Consulta histórico de um locker específico
        
        Args:
            locker_number: Número do locker (ex: "A1")
            
        Returns:
            Lista de reservas do locker
        """
        try:
            response = requests.get(f"{self.base_url}/bookings/locker/{locker_number}", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao consultar locker: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        Consulta estatísticas do sistema
        
        Returns:
            Dicionário com estatísticas
        """
        try:
            response = requests.get(f"{self.base_url}/stats", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao consultar estatísticas: {e}")
            return {}
    
    def export_csv(self, filename: Optional[str] = None) -> bool:
        """
        Exporta todos os dados para CSV
        
        Args:
            filename: Nome do arquivo (None para auto-gerar)
            
        Returns:
            True se exportou com sucesso
        """
        try:
            response = requests.get(f"{self.base_url}/export", timeout=TIMEOUT)
            response.raise_for_status()
            
            if not filename:
                filename = f"locker_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Dados exportados para: {filename}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao exportar dados: {e}")
            return False
    
    def format_booking(self, booking: Dict) -> str:
        """Formata uma reserva para exibição"""
        lines = []
        lines.append(f"🆔 ID: {booking['id']} | 🔒 Locker: {booking['locker_number']} | 📊 Status: {booking['status']}")
        lines.append(f"👤 Contacto: {booking['contact']}")
        lines.append(f"📅 Reservado: {booking['booking_time']}")
        
        if booking.get('unlock_time'):
            lines.append(f"🔓 Desbloqueado: {booking['unlock_time']}")
        if booking.get('return_time'):
            lines.append(f"🔄 Devolvido: {booking['return_time']}")
        if booking.get('notes'):
            lines.append(f"📝 Notas: {booking['notes']}")
            
        return "\n".join(lines)
    
    def display_bookings(self, bookings: List[Dict], title: str = "Reservas") -> None:
        """Exibe uma lista de reservas formatada"""
        print(f"\n{'='*60}")
        print(f"  {title.upper()}")
        print('='*60)
        
        if not bookings:
            print("📭 Nenhuma reserva encontrada.")
            return
            
        print(f"📊 Total: {len(bookings)} reservas\n")
        
        for i, booking in enumerate(bookings, 1):
            print(f"[{i}] {self.format_booking(booking)}")
            print("-" * 60)
    
    def display_statistics(self, stats: Dict) -> None:
        """Exibe estatísticas formatadas"""
        print(f"\n{'='*60}")
        print("  📊 ESTATÍSTICAS DO SISTEMA")
        print('='*60)
        
        if not stats:
            print("❌ Sem dados de estatísticas disponíveis")
            return
        
        print(f"📋 Total de reservas: {stats.get('total_bookings', 0)}")
        print(f"🔴 Reservas ativas: {stats.get('active_bookings', 0)}")
        print()
        
        if 'status_counts' in stats:
            print("📊 Distribuição por status:")
            for status, count in stats['status_counts'].items():
                print(f"   • {status}: {count}")
            print()
        
        if stats.get('most_used_locker'):
            most_used = stats['most_used_locker']
            print(f"🏆 Locker mais utilizado: {most_used['locker']} ({most_used['count']} reservas)")
            print()
        
        if stats.get('average_duration_hours', 0) > 0:
            print(f"⏱️  Tempo médio de utilização: {stats['average_duration_hours']:.2f} horas")
            print()
        
        print('='*60)


class RemoteClientMenu:
    """Menu interativo para o cliente remoto"""
    
    def __init__(self, client: RemoteLockerClient):
        self.client = client
    
    def display_menu(self) -> None:
        """Exibe o menu principal"""
        print(f"\n{'='*60}")
        print("  🔒 LOCKER SYSTEM - CLIENTE REMOTO")
        print('='*60)
        print("1. 📋 Ver todas as reservas")
        print("2. 🔴 Consultar reservas ativas")
        print("3. 📅 Ver reservas recentes")
        print("4. 🔍 Pesquisar por contacto")
        print("5. 🔒 Histórico de locker específico")
        print("6. 📊 Estatísticas do sistema")
        print("7. 📄 Exportar dados para CSV")
        print("8. 🌐 Abrir interface web")
        print("9. 🔄 Testar conexão")
        print("0. 🚪 Sair")
        print('='*60)
    
    def run(self) -> None:
        """Executa o menu interativo"""
        print("🚀 Bem-vindo ao Cliente Remoto do Sistema de Cacifos!")
        
        # Testar conexão inicial
        if not self.client.test_connection():
            print("\n❌ Não foi possível conectar ao servidor.")
            print("🔧 Verifique a configuração e tente novamente.")
            return
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\n🎯 Escolha uma opção: ").strip()
                
                if choice == '0':
                    print("\n👋 Obrigado por usar o sistema!")
                    break
                elif choice == '1':
                    self._query_all_bookings()
                elif choice == '2':
                    self._query_active_bookings()
                elif choice == '3':
                    self._query_recent_bookings()
                elif choice == '4':
                    self._search_by_contact()
                elif choice == '5':
                    self._query_locker_history()
                elif choice == '6':
                    self._show_statistics()
                elif choice == '7':
                    self._export_data()
                elif choice == '8':
                    self._open_web_interface()
                elif choice == '9':
                    self.client.test_connection()
                else:
                    print("\n❌ Opção inválida. Tente novamente.")
                    
                if choice != '0':
                    input("\n⏸️  Pressione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Saindo...")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                input("\n⏸️  Pressione Enter para continuar...")
    
    def _query_all_bookings(self) -> None:
        """Consulta todas as reservas"""
        try:
            limit_input = input("\n🔢 Limitar resultados (Enter para todas, recomendado 50): ").strip()
            limit = int(limit_input) if limit_input.isdigit() else 50
            
            print("⏳ Consultando reservas...")
            bookings = self.client.get_all_bookings(limit=limit)
            title = f"Todas as Reservas{f' (últimas {limit})' if limit else ''}"
            self.client.display_bookings(bookings, title)
            
        except Exception as e:
            print(f"❌ Erro ao consultar reservas: {e}")
    
    def _query_active_bookings(self) -> None:
        """Consulta reservas ativas"""
        try:
            print("⏳ Consultando reservas ativas...")
            bookings = self.client.get_active_bookings()
            self.client.display_bookings(bookings, "Reservas Ativas")
            
        except Exception as e:
            print(f"❌ Erro ao consultar reservas ativas: {e}")
    
    def _query_recent_bookings(self) -> None:
        """Consulta reservas recentes"""
        try:
            days_input = input("\n📅 Número de dias (padrão 7): ").strip()
            days = int(days_input) if days_input.isdigit() else 7
            
            print(f"⏳ Consultando reservas dos últimos {days} dias...")
            bookings = self.client.get_recent_bookings(days=days)
            self.client.display_bookings(bookings, f"Reservas dos Últimos {days} Dias")
            
        except Exception as e:
            print(f"❌ Erro ao consultar reservas recentes: {e}")
    
    def _search_by_contact(self) -> None:
        """Pesquisa por contacto"""
        try:
            contact = input("\n👤 Contacto (pesquisa parcial): ").strip()
            if not contact:
                print("❌ Contacto é obrigatório.")
                return
            
            print(f"⏳ Pesquisando por '{contact}'...")
            bookings = self.client.search_by_contact(contact)
            self.client.display_bookings(bookings, f"Reservas para '{contact}'")
            
        except Exception as e:
            print(f"❌ Erro ao pesquisar contacto: {e}")
    
    def _query_locker_history(self) -> None:
        """Consulta histórico de locker"""
        try:
            locker = input("\n🔒 Número do locker (ex: A1): ").strip().upper()
            if not locker:
                print("❌ Número do locker é obrigatório.")
                return
            
            print(f"⏳ Consultando histórico do locker {locker}...")
            bookings = self.client.get_locker_history(locker)
            self.client.display_bookings(bookings, f"Histórico do Locker {locker}")
            
        except Exception as e:
            print(f"❌ Erro ao consultar locker: {e}")
    
    def _show_statistics(self) -> None:
        """Mostra estatísticas"""
        try:
            print("⏳ Consultando estatísticas...")
            stats = self.client.get_statistics()
            self.client.display_statistics(stats)
            
        except Exception as e:
            print(f"❌ Erro ao consultar estatísticas: {e}")
    
    def _export_data(self) -> None:
        """Exporta dados"""
        try:
            filename = input("\n📄 Nome do arquivo (Enter para auto): ").strip()
            filename = filename if filename else None
            
            print("⏳ Exportando dados...")
            if self.client.export_csv(filename):
                print("✅ Exportação concluída com sucesso!")
            else:
                print("❌ Falha na exportação.")
                
        except Exception as e:
            print(f"❌ Erro ao exportar: {e}")
    
    def _open_web_interface(self) -> None:
        """Abre interface web"""
        try:
            import webbrowser
            webbrowser.open(self.client.web_url)
            print(f"🌐 Interface web aberta: {self.client.web_url}")
        except Exception as e:
            print(f"❌ Erro ao abrir navegador: {e}")
            print(f"🔗 Acesse manualmente: {self.client.web_url}")


def main():
    """Função principal"""
    print("🔧 Configurando cliente remoto...")
    
    # Verificar se IP está configurado
    if RASPBERRY_PI_IP == "192.168.1.100":
        print("⚠️  ATENÇÃO: IP do Raspberry Pi ainda não foi configurado!")
        print("   Edite a variável RASPBERRY_PI_IP no início deste arquivo.")
        print("   Exemplo: RASPBERRY_PI_IP = \"192.168.1.50\"")
        
        # Permitir configurar IP temporariamente
        new_ip = input("\n🔧 Digite o IP do Raspberry Pi (ou Enter para usar padrão): ").strip()
        if new_ip:
            global RASPBERRY_PI_IP
            RASPBERRY_PI_IP = new_ip
        else:
            print("⚠️  Usando IP padrão - pode não funcionar...")
    
    # Inicializar cliente e menu
    client = RemoteLockerClient(RASPBERRY_PI_IP, API_PORT)
    menu = RemoteClientMenu(client)
    menu.run()


if __name__ == "__main__":
    main()