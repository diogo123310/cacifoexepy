#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database API - Acesso Remoto ao SQLite
======================================
API REST simples para consultar a base de dados remotamente
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import json
from database import LockerDatabase
from datetime import datetime
import os
import webbrowser
import threading
import time

app = Flask(__name__)
CORS(app)  # Permite acesso de outros computadores

# Inicializar database
db = LockerDatabase()

# Template HTML simples para interface web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Locker System - Database Viewer</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .header h1 { margin: 0; font-size: 2.5em; text-align: center; }
        .header p { margin: 10px 0 0 0; text-align: center; opacity: 0.9; }
        .section { background: white; padding: 25px; margin-bottom: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
        .booking { border: 1px solid #e1e8ed; padding: 15px; margin: 10px 0; border-radius: 8px; transition: all 0.3s ease; }
        .booking:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .booking.booked { border-left: 4px solid #f39c12; background: #fef9e7; }
        .booking.unlocked { border-left: 4px solid #e74c3c; background: #fdedec; }
        .booking.completed { border-left: 4px solid #27ae60; background: #eafaf1; }
        .booking.available { border-left: 4px solid #95a5a6; background: #f8f9fa; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .stat-box { background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #3498db; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .stat-box h3 { margin: 0 0 10px 0; color: #2c3e50; font-size: 1.1em; }
        .stat-box p { margin: 0; font-size: 2em; font-weight: bold; color: #3498db; }
        .controls { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
        .btn { padding: 12px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; transition: all 0.3s ease; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
        .btn.secondary { background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); }
        .btn.success { background: linear-gradient(135deg, #55efc4 0%, #00b894 100%); }
        .btn.warning { background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%); }
        .search-box { padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 14px; width: 200px; transition: border-color 0.3s ease; }
        .search-box:focus { outline: none; border-color: #667eea; }
        .loading { text-align: center; padding: 40px; color: #74b9ff; font-size: 1.2em; }
        .error { text-align: center; padding: 40px; color: #e74c3c; font-size: 1.2em; }
        .no-data { text-align: center; padding: 40px; color: #95a5a6; font-size: 1.2em; }
        .status-badge { display: inline-block; padding: 4px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold; text-transform: uppercase; }
        .status-booked { background: #fff3cd; color: #856404; }
        .status-unlocked { background: #f8d7da; color: #721c24; }
        .status-completed { background: #d1ecf1; color: #0c5460; }
        .status-available { background: #e2e3e5; color: #383d41; }
        .refresh-info { text-align: center; margin-top: 20px; color: #6c757d; font-size: 0.9em; }
        .booking-id { font-weight: bold; color: #495057; }
        .booking-locker { font-weight: bold; color: #667eea; }
        .booking-contact { color: #28a745; }
        .booking-time { color: #6c757d; font-size: 0.9em; }
        .contact-details { line-height: 1.4; }
        .contact-details strong { margin-right: 5px; }
        
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .stats { grid-template-columns: 1fr; }
            .controls { flex-direction: column; }
            .search-box { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Locker System Database</h1>
            <p>Remote Database Access - Last Updated: <span id="lastUpdate">Loading...</span></p>
        </div>

        <div class="section">
            <h2>📊 System Overview</h2>
            <div class="stats" id="statsContainer">
                <div class="stat-box">
                    <h3>Total Bookings</h3>
                    <p id="totalBookings">-</p>
                </div>
                <div class="stat-box">
                    <h3>Active Bookings</h3>
                    <p id="activeBookings">-</p>
                </div>
                <div class="stat-box">
                    <h3>Completed Today</h3>
                    <p id="completedToday">-</p>
                </div>
                <div class="stat-box">
                    <h3>Most Used Locker</h3>
                    <p id="mostUsed">-</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🔍 Query Options</h2>
            <div class="controls">
                <button class="btn" onclick="loadAllBookings()">📋 All Bookings</button>
                <button class="btn secondary" onclick="loadActiveBookings()">🔴 Active Only</button>
                <button class="btn success" onclick="loadRecentBookings()">📅 Recent (7 days)</button>
                <button class="btn warning" onclick="loadStats()">📊 Detailed Stats</button>
                <input type="text" class="search-box" id="searchContact" placeholder="Search by name, email, phone..." onkeypress="handleSearchKeyPress(event)">
                <button class="btn" onclick="searchByContact()">🔍 Search</button>
                <button class="btn secondary" onclick="exportData()">📄 Export CSV</button>
            </div>
        </div>

        <div class="section">
            <h2 id="dataTitle">📋 Booking Data</h2>
            <div id="dataContainer">
                <div class="no-data">Click a button above to load data...</div>
            </div>
            <div class="refresh-info">
                <small>Data refreshes automatically every 30 seconds</small>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = window.location.origin;
        let currentEndpoint = null;
        let refreshInterval = null;
        
        function updateLastUpdate() {
            document.getElementById('lastUpdate').textContent = new Date().toLocaleString();
        }
        
        function handleSearchKeyPress(event) {
            if (event.key === 'Enter') {
                searchByContact();
            }
        }
        
        async function loadStats() {
            try {
                const response = await fetch(`${API_BASE}/api/stats`);
                const stats = await response.json();
                
                document.getElementById('totalBookings').textContent = stats.total_bookings || 0;
                
                // Calculate active bookings
                const activeCount = Object.entries(stats.status_counts || {})
                    .filter(([status]) => ['booked', 'unlocked'].includes(status))
                    .reduce((sum, [_, count]) => sum + count, 0);
                document.getElementById('activeBookings').textContent = activeCount;
                
                // Get today's completed (mock for now)
                document.getElementById('completedToday').textContent = stats.status_counts?.completed || 0;
                
                document.getElementById('mostUsed').textContent = 
                    stats.most_used_locker ? stats.most_used_locker.locker : 'N/A';
                
                document.getElementById('dataTitle').textContent = '📊 Detailed Statistics';
                document.getElementById('dataContainer').innerHTML = `
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                            <h3 style="margin-top: 0; color: #495057;">Status Distribution</h3>
                            <ul style="list-style: none; padding: 0;">
                                ${Object.entries(stats.status_counts || {}).map(([status, count]) => `
                                    <li style="margin: 10px 0; display: flex; justify-content: space-between;">
                                        <span class="status-badge status-${status}">${status}</span>
                                        <strong>${count}</strong>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                        
                        ${stats.most_used_locker ? `
                            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                                <h3 style="margin-top: 0; color: #495057;">Most Popular</h3>
                                <p style="font-size: 1.5em; margin: 10px 0;">
                                    <span class="booking-locker">Locker ${stats.most_used_locker.locker}</span>
                                </p>
                                <p style="color: #6c757d;">${stats.most_used_locker.count} total bookings</p>
                            </div>
                        ` : ''}
                        
                        ${stats.average_duration_hours > 0 ? `
                            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                                <h3 style="margin-top: 0; color: #495057;">Average Usage</h3>
                                <p style="font-size: 1.5em; margin: 10px 0; color: #28a745;">
                                    ${stats.average_duration_hours.toFixed(1)} hours
                                </p>
                                <p style="color: #6c757d;">Per completed booking</p>
                            </div>
                        ` : ''}
                    </div>
                `;
                updateLastUpdate();
            } catch (error) {
                console.error('Error loading stats:', error);
                document.getElementById('dataContainer').innerHTML = '<div class="error">❌ Error loading statistics</div>';
            }
        }
        
        async function loadAllBookings() {
            currentEndpoint = '/api/bookings?limit=50';
            await loadBookings(currentEndpoint, 'All Bookings (Last 50)');
        }
        
        async function loadActiveBookings() {
            currentEndpoint = '/api/bookings/active';
            await loadBookings(currentEndpoint, 'Active Bookings');
        }
        
        async function loadRecentBookings() {
            currentEndpoint = '/api/bookings/recent?days=7';
            await loadBookings(currentEndpoint, 'Recent Bookings (7 days)');
        }
        
        async function searchByContact() {
            const contact = document.getElementById('searchContact').value.trim();
            if (!contact) {
                alert('Please enter a name, email, or phone number to search for');
                return;
            }
            currentEndpoint = `/api/bookings/contact/${encodeURIComponent(contact)}`;
            await loadBookings(currentEndpoint, `Bookings for "${contact}"`);
        }
        
        async function loadBookings(endpoint, title) {
            try {
                document.getElementById('dataContainer').innerHTML = '<div class="loading">⏳ Loading data...</div>';
                const response = await fetch(`${API_BASE}${endpoint}`);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                
                const bookings = await response.json();
                
                document.getElementById('dataTitle').textContent = `📋 ${title} (${bookings.length})`;
                
                if (bookings.length === 0) {
                    document.getElementById('dataContainer').innerHTML = '<div class="no-data">📭 No bookings found.</div>';
                    return;
                }
                
                const bookingsHtml = bookings.map(booking => `
                    <div class="booking ${booking.status}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span class="booking-id">ID: ${booking.id}</span>
                            <span class="status-badge status-${booking.status}">${booking.status}</span>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
                            <div class="contact-details">
                                <strong>🔒 Locker:</strong> <span class="booking-locker">${booking.locker_number}</span><br>
                                ${booking.name ? `<strong>👤 Name:</strong> <span class="booking-contact">${booking.name}</span><br>` : ''}
                                ${booking.email ? `<strong>📧 Email:</strong> <span class="booking-contact">${booking.email}</span><br>` : ''}
                                ${booking.phone ? `<strong>📱 Phone:</strong> <span class="booking-contact">${booking.phone}</span><br>` : ''}
                                ${booking.birth_date ? `<strong>🎂 Birth Date:</strong> <span class="booking-contact">${booking.birth_date}</span><br>` : ''}
                                ${booking.contact && !booking.email ? `<strong>👤 Contact:</strong> <span class="booking-contact">${booking.contact}</span><br>` : ''}
                                <strong>🔑 PIN:</strong> <span style="color: #e74c3c; font-weight: bold;">${booking.pin || 'N/A'}</span>
                            </div>
                            <div>
                                <div class="booking-time"><strong>📅 Booked:</strong> ${formatDateTime(booking.booking_time)}</div>
                                ${booking.unlock_time ? `<div class="booking-time"><strong>🔓 Unlocked:</strong> ${formatDateTime(booking.unlock_time)}</div>` : ''}
                                ${booking.return_time ? `<div class="booking-time"><strong>🔄 Returned:</strong> ${formatDateTime(booking.return_time)}</div>` : ''}
                            </div>
                        </div>
                        ${booking.notes ? `<div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;"><strong>📝 Notes:</strong> ${booking.notes}</div>` : ''}
                    </div>
                `).join('');
                
                document.getElementById('dataContainer').innerHTML = bookingsHtml;
                updateLastUpdate();
            } catch (error) {
                console.error('Error loading bookings:', error);
                document.getElementById('dataContainer').innerHTML = '<div class="error">❌ Error loading data. Please check your connection.</div>';
            }
        }
        
        function formatDateTime(dateTimeString) {
            if (!dateTimeString) return 'N/A';
            try {
                const date = new Date(dateTimeString);
                return date.toLocaleString();
            } catch (e) {
                return dateTimeString;
            }
        }
        
        async function exportData() {
            try {
                const response = await fetch(`${API_BASE}/api/export`);
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `locker_bookings_${new Date().toISOString().split('T')[0]}.csv`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                alert('📄 Data exported successfully!');
            } catch (error) {
                console.error('Export error:', error);
                alert('❌ Export failed. Please try again.');
            }
        }
        
        // Auto-refresh current data
        function startAutoRefresh() {
            if (refreshInterval) clearInterval(refreshInterval);
            refreshInterval = setInterval(() => {
                if (currentEndpoint) {
                    const titleMatch = document.getElementById('dataTitle').textContent.match(/📋 (.+) \\(\\d+\\)/);
                    const title = titleMatch ? titleMatch[1] : 'Data';
                    loadBookings(currentEndpoint, title);
                }
                loadStats(); // Always refresh stats
            }, 30000); // 30 seconds
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadStats();
            startAutoRefresh();
            updateLastUpdate();
        });
        
        // Stop refresh when page is hidden
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                if (refreshInterval) clearInterval(refreshInterval);
            } else {
                startAutoRefresh();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Interface web principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/bookings')
def get_all_bookings():
    """API: Todas as reservas"""
    try:
        limit = request.args.get('limit', type=int)
        bookings = db.get_all_bookings(limit=limit)
        
        # Debug: imprimir primeira reserva
        if bookings:
            print(f"DEBUG: First booking keys: {list(bookings[0].keys())}")
            print(f"DEBUG: First booking PIN: {bookings[0].get('pin', 'NOT FOUND')}")
        
        return jsonify(bookings)
    except Exception as e:
        print(f"ERROR in get_all_bookings: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/active')
def get_active_bookings():
    """API: Reservas ativas"""
    try:
        all_bookings = db.get_all_bookings()
        active_bookings = [b for b in all_bookings if b['status'] in ['booked', 'unlocked']]
        return jsonify(active_bookings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/recent')
def get_recent_bookings():
    """API: Reservas recentes"""
    try:
        days = request.args.get('days', 7, type=int)
        bookings = db.get_recent_bookings(days=days)
        return jsonify(bookings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/contact/<contact>')
def get_bookings_by_contact(contact):
    """API: Reservas por contacto"""
    try:
        bookings = db.get_bookings_by_contact(contact)
        return jsonify(bookings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/locker/<locker_number>')
def get_bookings_by_locker(locker_number):
    """API: Reservas por locker"""
    try:
        bookings = db.get_bookings_by_locker(locker_number)
        return jsonify(bookings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_statistics():
    """API: Estatísticas"""
    try:
        stats = db.get_booking_statistics()
        # Add some additional stats
        all_bookings = db.get_all_bookings()
        active_count = len([b for b in all_bookings if b['status'] in ['booked', 'unlocked']])
        stats['active_bookings'] = active_count
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export')
def export_csv():
    """API: Exportar dados em CSV"""
    try:
        import csv
        from io import StringIO
        
        bookings = db.get_all_bookings()
        
        # Criar CSV em memória
        output = StringIO()
        fieldnames = ['id', 'locker_number', 'contact', 'pin', 'status', 
                     'booking_time', 'unlock_time', 'return_time', 'notes']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        for booking in bookings:
            writer.writerow(booking)
        
        # Preparar response
        csv_data = output.getvalue()
        output.close()
        
        response = app.response_class(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=locker_bookings_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
        )
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def get_system_status():
    """API: Status do sistema"""
    try:
        # Test database connection
        stats = db.get_booking_statistics()
        return jsonify({
            'status': 'online',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'total_bookings': stats.get('total_bookings', 0),
            'version': '1.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'database': 'disconnected',
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 LOCKER SYSTEM DATABASE API")
    print("="*60)
    print("📊 Starting Database API Server...")
    print("📱 Web Interface: http://localhost:5000")
    print("🌐 Network Access: http://YOUR_IP:5000")
    print()
    print("🔗 Available API Endpoints:")
    print("   • GET /api/bookings - All bookings")
    print("   • GET /api/bookings/active - Active bookings") 
    print("   • GET /api/bookings/recent - Recent bookings")
    print("   • GET /api/bookings/contact/<contact> - Search by name, email, or phone")
    print("   • GET /api/stats - System statistics")
    print("   • GET /api/export - Export CSV")
    print("   • GET /api/status - System status")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print("="*60)
    
    # Verificar se database existe
    if not os.path.exists('locker_system.db'):
        print("⚠️  WARNING: Database file 'locker_system.db' not found!")
        print("   The API will start but may not return data.")
        print()
    
    # Função para abrir navegador automaticamente
    def open_browser():
        """Abre o navegador após 2 segundos para dar tempo ao servidor iniciar"""
        time.sleep(2)  # Aguardar servidor iniciar
        try:
            print("🌐 Opening web browser automatically...")
            webbrowser.open('http://localhost:5000')
            print("✅ Browser opened! If it didn't open, go to: http://localhost:5000")
        except Exception as e:
            print(f"❌ Could not open browser automatically: {e}")
            print("🔗 Please open manually: http://localhost:5000")
    
    # Iniciar thread para abrir navegador
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Executar servidor (acessível de qualquer IP na rede)
    app.run(host='0.0.0.0', port=5000, debug=False)