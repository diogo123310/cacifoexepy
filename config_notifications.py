# config_notifications.py
# Configuração das credenciais para o sistema de notificações
# IMPORTANTE: Configure este arquivo com suas credenciais reais

from notification_service import notification_service

def setup_email_gmail():
    """
    Configurar Email via Gmail
    
    Para usar Gmail:
    1. Ative a autenticação de dois fatores na sua conta Google
    2. Gere uma "Senha de app" específica para esta aplicação:
       - Vá para https://myaccount.google.com/security
       - Selecione "Passwords for apps" 
       - Gere uma nova senha para "Mail"
       - Use essa senha aqui (não a sua senha normal do Gmail)
    """
    
    # CONFIGURE AQUI COM SUAS CREDENCIAIS REAIS:
    EMAIL_ADDRESS = "seu_email@gmail.com"  # Substitua pelo seu email
    EMAIL_PASSWORD = "sua_senha_de_app"    # Substitua pela senha de app do Gmail
    SENDER_NAME = "Sistema de Cacifos"
    
    # ⚠️ DESCOMENTAR ESTAS LINHAS APÓS CONFIGURAR:
    # notification_service.configure_email(
    #     smtp_server='smtp.gmail.com',
    #     smtp_port=587,
    #     sender_email=EMAIL_ADDRESS,
    #     sender_password=EMAIL_PASSWORD,
    #     sender_name=SENDER_NAME
    # )
    # print(f"✅ Email configurado: {EMAIL_ADDRESS}")
    
    print("⚠️ Email não configurado - edite config_notifications.py")

def setup_sms_twilio():
    """
    Configurar SMS via Twilio
    
    Para usar Twilio:
    1. Crie uma conta em https://www.twilio.com/
    2. Obtenha suas credenciais:
       - Account SID
       - Auth Token
       - Número de telefone Twilio
    3. Configure abaixo
    """
    
    # CONFIGURE AQUI COM SUAS CREDENCIAIS TWILIO:
    ACCOUNT_SID = "seu_account_sid"     # Ex: "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    AUTH_TOKEN = "seu_auth_token"       # Ex: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    FROM_NUMBER = "+1234567890"         # Seu número Twilio
    
    # ⚠️ DESCOMENTAR ESTAS LINHAS APÓS CONFIGURAR:
    # notification_service.configure_sms_twilio(
    #     account_sid=ACCOUNT_SID,
    #     auth_token=AUTH_TOKEN,
    #     from_number=FROM_NUMBER
    # )
    # print(f"✅ SMS Twilio configurado: {FROM_NUMBER}")
    
    print("⚠️ SMS Twilio não configurado - edite config_notifications.py")

def setup_sms_textbelt():
    """
    Configurar SMS via TextBelt (alternativa gratuita)
    
    TextBelt oferece:
    - 1 SMS gratuito por dia com API key "textbelt"
    - Mais SMS com créditos pagos
    
    Para comprar créditos: https://textbelt.com/
    """
    
    # Para teste gratuito (1 SMS por dia):
    notification_service.configure_sms_textbelt('textbelt')
    print("✅ SMS TextBelt configurado (1 SMS gratuito por dia)")
    
    # Para usar com créditos pagos, substitua "textbelt" pela sua API key:
    # API_KEY = "sua_api_key_textbelt"  # Substitua pela sua API key paga
    # notification_service.configure_sms_textbelt(API_KEY)
    # print(f"✅ SMS TextBelt configurado com API key: {API_KEY}")

def initialize_notifications():
    """Inicializar todas as configurações de notificação"""
    print("🔧 Configurando sistema de notificações...")
    
    # Configurar Email
    setup_email_gmail()
    
    # Configurar SMS Twilio
    setup_sms_twilio()
    
    # Configurar SMS TextBelt (fallback gratuito)
    setup_sms_textbelt()
    
    print("📬 Sistema de notificações inicializado!")
    return notification_service

def test_notifications():
    """Testar o sistema de notificações"""
    print("\n🧪 Testando sistema de notificações...")
    
    # Emails e números de teste (substitua pelos seus dados reais para teste)
    TEST_EMAIL = "seu_email_teste@gmail.com"  # Substitua pelo seu email para teste
    TEST_PHONE = "+351912345678"              # Substitua pelo seu número para teste
    
    # Executar teste
    results = notification_service.test_notifications(TEST_EMAIL, TEST_PHONE)
    
    print(f"\n📊 Resultados do teste:")
    print(f"📧 Email: {'✅ Sucesso' if results['email'] else '❌ Falhou'}")
    print(f"📱 SMS: {'✅ Sucesso' if results['sms'] else '❌ Falhou'}")
    
    return results

if __name__ == '__main__':
    # Inicializar configurações
    initialize_notifications()
    
    # Executar teste (opcional)
    # test_notifications()
    
    print("\n" + "="*50)
    print("📋 INSTRUÇÕES PARA CONFIGURAR:")
    print("="*50)
    print("1. 📧 GMAIL:")
    print("   - Ative autenticação 2FA na sua conta Google")
    print("   - Gere uma 'Senha de app' em https://myaccount.google.com/security")
    print("   - Edite setup_email_gmail() com suas credenciais")
    print()
    print("2. 📱 TWILIO SMS (pago mas confiável):")
    print("   - Crie conta em https://www.twilio.com/")
    print("   - Obtenha Account SID, Auth Token e número Twilio")
    print("   - Edite setup_sms_twilio() com suas credenciais")
    print()
    print("3. 📱 TEXTBELT SMS (1 gratuito/dia):")
    print("   - Já configurado! 1 SMS gratuito por dia")
    print("   - Para mais SMS: https://textbelt.com/")
    print()
    print("4. 🧪 TESTE:")
    print("   - Edite TEST_EMAIL e TEST_PHONE em test_notifications()")
    print("   - Execute: python config_notifications.py")
    print("="*50)