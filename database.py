import sqlite3
import hashlib
import datetime
import os
import threading
import time
from typing import Optional, List, Dict

class LockerDatabase:
    def __init__(self, db_path="locker_system.db"):
        """Inicializa a base de dados SQLite com melhor gestão de locks"""
        self.db_path = db_path
        self.lock = threading.Lock()
        self.timeout = 10.0  # 10 segundos de timeout
        self.init_database()
    
    def _get_connection(self):
        """Cria conexão com timeout e configurações otimizadas"""
        conn = sqlite3.connect(
            self.db_path, 
            timeout=self.timeout,
            check_same_thread=False
        )
        # Configurações para evitar locks
        conn.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging
        conn.execute('PRAGMA synchronous=NORMAL')
        conn.execute('PRAGMA temp_store=MEMORY')
        conn.execute('PRAGMA mmap_size=268435456')  # 256MB
        return conn
    
    def init_database(self):
        """Cria as tabelas se não existirem"""
        with self.lock:
            try:
                conn = self._get_connection()
                cursor = conn.cursor()
                
                # Tabela para os cacifos
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS lockers (
                        locker_number TEXT PRIMARY KEY,
                        status TEXT NOT NULL DEFAULT 'available',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela para reservas/utilizações
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        locker_number TEXT NOT NULL,
                        contact TEXT NOT NULL,
                        pin_hash TEXT NOT NULL,
                        pin_salt TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'active',
                        booking_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        unlock_time DATETIME,
                        return_time DATETIME,
                        notes TEXT,
                        FOREIGN KEY (locker_number) REFERENCES lockers (locker_number)
                    )
                ''')
                
                # Tabela para logs do sistema
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        locker_number TEXT,
                        action TEXT NOT NULL,
                        details TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        gpio_state TEXT
                    )
                ''')
                
                # Inserir cacifos padrão se não existirem
                lockers = ['001', '002', '003', '004']
                for locker in lockers:
                    cursor.execute('''
                        INSERT OR IGNORE INTO lockers (locker_number, status) 
                        VALUES (?, 'available')
                    ''', (locker,))
                
                conn.commit()
                print("Database initialized successfully")
                
            except sqlite3.OperationalError as e:
                print(f"Database initialization error: {e}")
                time.sleep(0.1)  # Pequena pausa antes de tentar novamente
            finally:
                if 'conn' in locals():
                    conn.close()
    
    def _execute_with_retry(self, operation_func, max_retries=3):
        """Executa operação com retry em caso de lock"""
        for attempt in range(max_retries):
            try:
                with self.lock:
                    return operation_func()
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    print(f"Database locked, retry {attempt + 1}/{max_retries}")
                    time.sleep(0.1 * (attempt + 1))  # Backoff exponencial
                    continue
                else:
                    print(f"Database error after {attempt + 1} attempts: {e}")
                    return None
            except Exception as e:
                print(f"Unexpected database error: {e}")
                return None
        return None
    
    def _hash_pin(self, pin: str) -> tuple:
        """Gera hash seguro do PIN com salt"""
        import secrets
        salt = secrets.token_hex(16)
        pin_hash = hashlib.pbkdf2_hmac('sha256', pin.encode(), salt.encode(), 100000)
        return pin_hash.hex(), salt
    
    def _verify_pin(self, pin: str, pin_hash: str, salt: str) -> bool:
        """Verifica se o PIN está correto"""
        test_hash = hashlib.pbkdf2_hmac('sha256', pin.encode(), salt.encode(), 100000)
        return test_hash.hex() == pin_hash
    
    def book_locker(self, locker_number: str, contact: str, pin: str) -> dict:
        """Reserva um cacifo para um utilizador"""
        def operation():
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Verificar se o cacifo está disponível
                cursor.execute('''
                    SELECT status FROM lockers WHERE locker_number = ?
                ''', (locker_number,))
                
                result = cursor.fetchone()
                if not result:
                    return {"success": False, "message": "Cacifo não existe"}
                
                if result[0] != 'available':
                    return {"success": False, "message": "Cacifo não está disponível"}
                
                # Gerar hash do PIN
                pin_hash, salt = self._hash_pin(pin)
                
                # Iniciar transação
                cursor.execute('BEGIN IMMEDIATE')
                
                # Criar reserva
                cursor.execute('''
                    INSERT INTO bookings (locker_number, contact, pin_hash, pin_salt, status)
                    VALUES (?, ?, ?, ?, 'active')
                ''', (locker_number, contact, pin_hash, salt))
                
                # Atualizar status do cacifo
                cursor.execute('''
                    UPDATE lockers SET status = 'occupied', updated_at = CURRENT_TIMESTAMP
                    WHERE locker_number = ?
                ''', (locker_number,))
                
                # Log da ação
                cursor.execute('''
                    INSERT INTO system_logs (locker_number, action, details)
                    VALUES (?, 'BOOKED', ?)
                ''', (locker_number, f'Contact: {contact}'))
                
                conn.commit()
                
                print(f"Cacifo {locker_number} reservado com sucesso para {contact}")
                return {
                    "success": True, 
                    "message": f"Cacifo {locker_number} reservado com sucesso",
                    "locker_number": locker_number,
                    "contact": contact
                }
                
            except Exception as e:
                print(f"Erro ao reservar cacifo: {e}")
                conn.rollback()
                return {"success": False, "message": f"Erro ao reservar: {str(e)}"}
            finally:
                conn.close()
        
        result = self._execute_with_retry(operation)
        if result is None:
            return {"success": False, "message": "Erro na base de dados após várias tentativas"}
        return result
    
    def unlock_locker(self, contact: str, pin: str) -> Optional[str]:
        """Desbloqueia um cacifo usando contacto e PIN"""
        def operation():
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Encontrar reserva ativa
                cursor.execute('''
                    SELECT locker_number, pin_hash, pin_salt, id
                    FROM bookings 
                    WHERE contact = ? AND status = 'active'
                    ORDER BY booking_time DESC
                    LIMIT 1
                ''', (contact,))
                
                result = cursor.fetchone()
                if not result:
                    return None
                
                locker_number, pin_hash, salt, booking_id = result
                
                # Verificar PIN
                if not self._verify_pin(pin, pin_hash, salt):
                    return None
                
                # Atualizar tempo de desbloqueio
                cursor.execute('''
                    UPDATE bookings SET unlock_time = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (booking_id,))
                
                # Log da ação
                cursor.execute('''
                    INSERT INTO system_logs (locker_number, action, details)
                    VALUES (?, 'UNLOCKED', ?)
                ''', (locker_number, f'Contact: {contact}'))
                
                conn.commit()
                return locker_number
                
            except Exception as e:
                print(f"Error unlocking locker: {e}")
                conn.rollback()
                return None
            finally:
                conn.close()
        
        return self._execute_with_retry(operation)
    
    def return_locker(self, locker_number: str) -> bool:
        """Marca um cacifo como devolvido"""
        def operation():
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                # Encontrar reserva ativa
                cursor.execute('''
                    UPDATE bookings 
                    SET status = 'completed', return_time = CURRENT_TIMESTAMP
                    WHERE locker_number = ? AND status = 'active'
                ''', (locker_number,))
                
                # Marcar cacifo como disponível
                cursor.execute('''
                    UPDATE lockers SET status = 'available', updated_at = CURRENT_TIMESTAMP
                    WHERE locker_number = ?
                ''', (locker_number,))
                
                # Log da ação
                cursor.execute('''
                    INSERT INTO system_logs (locker_number, action, details)
                    VALUES (?, 'RETURNED', ?)
                ''', (locker_number, 'Locker returned to available'))
                
                conn.commit()
                return True
                
            except Exception as e:
                print(f"Error returning locker: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()
        
        result = self._execute_with_retry(operation)
        return result if result is not None else False
    
    def get_locker_status(self, locker_number: str) -> str:
        """Obtém o status de um cacifo específico"""
        def operation():
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT status FROM lockers WHERE locker_number = ?
                ''', (locker_number,))
                
                result = cursor.fetchone()
                return result[0] if result else 'unknown'
            finally:
                conn.close()
        
        result = self._execute_with_retry(operation)
        return result if result is not None else 'unknown'
    
    def get_all_lockers_status(self) -> Dict[str, str]:
        """Obtém o status de todos os cacifos"""
        def operation():
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT locker_number, status FROM lockers')
                results = cursor.fetchall()
                return {locker: status for locker, status in results}
            finally:
                conn.close()
        
        result = self._execute_with_retry(operation)
        return result if result is not None else {}
    
    def get_active_booking(self, locker_number: str) -> Optional[Dict]:
        """Obtém informações da reserva ativa de um cacifo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT contact, booking_time, unlock_time, notes
            FROM bookings 
            WHERE locker_number = ? AND status = 'active'
            ORDER BY booking_time DESC
            LIMIT 1
        ''', (locker_number,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'contact': result[0],
                'booking_time': result[1],
                'unlock_time': result[2],
                'notes': result[3]
            }
        return None
    
    def log_action(self, locker_number: str, action: str, details: str = "", gpio_state: str = ""):
        """Adiciona entrada ao log do sistema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_logs (locker_number, action, details, gpio_state)
            VALUES (?, ?, ?, ?)
        ''', (locker_number, action, details, gpio_state))
        
        conn.commit()
        conn.close()
    
    def get_usage_stats(self) -> Dict:
        """Obtém estatísticas de utilização"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total de reservas
        cursor.execute('SELECT COUNT(*) FROM bookings')
        total_bookings = cursor.fetchone()[0]
        
        # Reservas ativas
        cursor.execute('SELECT COUNT(*) FROM bookings WHERE status = "active"')
        active_bookings = cursor.fetchone()[0]
        
        # Cacifos disponíveis
        cursor.execute('SELECT COUNT(*) FROM lockers WHERE status = "available"')
        available_lockers = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_bookings': total_bookings,
            'active_bookings': active_bookings,
            'available_lockers': available_lockers,
            'total_lockers': 4
        }
    
    def cleanup_old_logs(self, days: int = 30):
        """Remove logs antigos para manter a base de dados limpa"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM system_logs 
            WHERE timestamp < datetime('now', '-{} days')
        '''.format(days))
        
        deleted_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"Deleted {deleted_rows} old log entries")
        return deleted_rows