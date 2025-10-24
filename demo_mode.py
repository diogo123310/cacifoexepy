# demo_mode.py
# Modo demonstração com notificações simuladas

from notification_service import notification_service

def enable_demo_mode():
    """Ativar modo demonstração com notificações simuladas"""
    
    # Sobrescrever métodos de envio para sempre retornarem True
    def mock_send_email(self, recipient_email, subject, message_body):
        print(f"📧 DEMO: Email simulado para {recipient_email}")
        print(f"📧 Assunto: {subject}")
        print(f"📧 Conteúdo: {len(message_body)} caracteres")
        return True
    
    def mock_send_sms_textbelt(self, recipient_phone, message_body):
        print(f"📱 DEMO: SMS simulado para {recipient_phone}")
        print(f"📱 Mensagem: {message_body}")
        return True
    
    def mock_send_sms_twilio(self, recipient_phone, message_body):
        print(f"📱 DEMO: SMS Twilio simulado para {recipient_phone}")
        print(f"📱 Mensagem: {message_body}")
        return True
    
    # Substituir métodos
    notification_service.__class__.send_email = mock_send_email
    notification_service.__class__.send_sms_textbelt = mock_send_sms_textbelt
    notification_service.__class__.send_sms_twilio = mock_send_sms_twilio
    
    print("🎭 MODO DEMONSTRAÇÃO ATIVADO")
    print("✅ Todas as notificações serão simuladas como enviadas com sucesso")

def disable_demo_mode():
    """Desativar modo demonstração"""
    # Recarregar o módulo para restaurar métodos originais
    import importlib
    import notification_service as ns_module
    importlib.reload(ns_module)
    
    print("🔧 MODO DEMONSTRAÇÃO DESATIVADO")
    print("⚙️ Métodos originais restaurados")

if __name__ == '__main__':
    # Teste do modo demonstração
    from translations import translator
    
    print("🧪 TESTE DO MODO DEMONSTRAÇÃO")
    print("=" * 40)
    
    # Ativar modo demo
    enable_demo_mode()
    
    # Configurar idioma
    translator.set_language('pt')
    
    # Dados de teste
    user_data = {
        'name': 'João Demo',
        'email': 'demo@example.com',
        'phone': '+351912345678',
        'birth_date': '01/01/1990'
    }
    
    # Testar notificações
    print("\n📧📱 Testando notificações no modo demo...")
    results = notification_service.send_pin_notification(
        user_data=user_data,
        locker_number='001',
        pin='1234',
        notification_methods=['email', 'sms']
    )
    
    print(f"\n📊 RESULTADOS:")
    print(f"📧 Email: {'✅ Sucesso' if results['email'] else '❌ Falhou'}")
    print(f"📱 SMS: {'✅ Sucesso' if results['sms'] else '❌ Falhou'}")
    
    print("\n💡 Para usar no aplicativo principal:")
    print("1. Importe: from demo_mode import enable_demo_mode")
    print("2. Execute: enable_demo_mode()")
    print("3. Execute o aplicativo normalmente")
    print("4. As notificações aparecerão como ✅ Sent")