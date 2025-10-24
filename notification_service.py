# notification_service.py
# Sistema de notificações por SMS e Email para envio de PINs

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from datetime import datetime
from translations import translator

class NotificationService:
    """Serviço para envio de notificações por SMS e Email"""
    
    def __init__(self):
        # Configurações de Email (Gmail como exemplo)
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': '',  # Configurar com email real
            'sender_password': '',  # Configurar com senha de app Gmail
            'sender_name': 'Cacifo System'
        }
        
        # Configurações SMS (Twilio como exemplo)
        self.sms_config = {
            'account_sid': '',  # Configurar com Account SID do Twilio
            'auth_token': '',   # Configurar com Auth Token do Twilio
            'from_number': '',  # Número Twilio (ex: +1234567890)
            'api_url': 'https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json'
        }
        
        # Configurações alternativas SMS (TextBelt - gratuito para teste)
        self.textbelt_config = {
            'api_url': 'https://textbelt.com/text',
            'api_key': 'textbelt'  # 'textbelt' para 1 SMS gratuito por dia, ou comprar créditos
        }
    
    def configure_email(self, smtp_server, smtp_port, sender_email, sender_password, sender_name="Cacifo System"):
        """Configurar credenciais de email"""
        self.email_config.update({
            'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'sender_email': sender_email,
            'sender_password': sender_password,
            'sender_name': sender_name
        })
        print(f"Email configurado: {sender_email}")
    
    def configure_sms_twilio(self, account_sid, auth_token, from_number):
        """Configurar credenciais do Twilio para SMS"""
        self.sms_config.update({
            'account_sid': account_sid,
            'auth_token': auth_token,
            'from_number': from_number,
            'api_url': f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'
        })
        print("SMS Twilio configurado")
    
    def configure_sms_textbelt(self, api_key):
        """Configurar TextBelt para SMS (alternativa gratuita)"""
        self.textbelt_config['api_key'] = api_key
        print("SMS TextBelt configurado")
    
    def send_email(self, recipient_email, subject, message_body):
        """Enviar email"""
        try:
            # Verificar se email está configurado
            if not self.email_config['sender_email'] or not self.email_config['sender_password']:
                print("⚠️ Email não configurado - configurações necessárias em notification_service.py")
                return False
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = f"{self.email_config['sender_name']} <{self.email_config['sender_email']}>"
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Adicionar corpo da mensagem
            msg.attach(MIMEText(message_body, 'plain', 'utf-8'))
            
            # Conectar ao servidor SMTP
            context = ssl.create_default_context()
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls(context=context)
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                
                # Enviar email
                text = msg.as_string()
                server.sendmail(self.email_config['sender_email'], recipient_email, text)
            
            print(f"✅ Email enviado com sucesso para {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
            return False
    
    def send_sms_twilio(self, recipient_phone, message_body):
        """Enviar SMS via Twilio"""
        try:
            # Verificar se Twilio está configurado
            if not self.sms_config['account_sid'] or not self.sms_config['auth_token']:
                print("⚠️ Twilio não configurado - configurações necessárias em notification_service.py")
                return False
            
            import base64
            
            # Preparar autenticação
            auth_string = f"{self.sms_config['account_sid']}:{self.sms_config['auth_token']}"
            auth_bytes = auth_string.encode('ascii')
            auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
            
            # Preparar dados
            data = {
                'From': self.sms_config['from_number'],
                'To': recipient_phone,
                'Body': message_body
            }
            
            # Headers
            headers = {
                'Authorization': f'Basic {auth_base64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Enviar SMS
            response = requests.post(
                self.sms_config['api_url'],
                data=data,
                headers=headers
            )
            
            if response.status_code == 201:
                print(f"✅ SMS enviado com sucesso para {recipient_phone}")
                return True
            else:
                print(f"❌ Erro ao enviar SMS: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar SMS via Twilio: {e}")
            return False
    
    def send_sms_textbelt(self, recipient_phone, message_body):
        """Enviar SMS via TextBelt (alternativa gratuita)"""
        try:
            data = {
                'phone': recipient_phone,
                'message': message_body,
                'key': self.textbelt_config['api_key']
            }
            
            response = requests.post(self.textbelt_config['api_url'], data=data)
            result = response.json()
            
            if result.get('success'):
                print(f"✅ SMS enviado com sucesso para {recipient_phone} via TextBelt")
                return True
            else:
                error_msg = result.get('error', 'Erro desconhecido')
                print(f"❌ Erro ao enviar SMS via TextBelt: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar SMS via TextBelt: {e}")
            return False
    
    def send_pin_notification(self, user_data, locker_number, pin, notification_methods=['email', 'sms']):
        """
        Enviar notificação com PIN para o utilizador
        
        Args:
            user_data (dict): Dados do utilizador {'name', 'email', 'phone', 'birth_date'}
            locker_number (str): Número do cacifo (ex: '001')
            pin (str): PIN gerado (ex: '1234')
            notification_methods (list): ['email', 'sms'] ou ['email'] ou ['sms']
        
        Returns:
            dict: Resultado do envio {'email': bool, 'sms': bool}
        """
        results = {'email': False, 'sms': False}
        
        # Obter textos traduzidos
        current_lang = translator.get_current_language()
        
        # Preparar dados da mensagem
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M")
        
        # Criar mensagens personalizadas para cada idioma
        if current_lang == 'pt':
            email_subject = f"🔐 PIN do Cacifo {locker_number} - Sistema de Cacifos"
            email_body = f"""Olá {user_data.get('name', 'Cliente')},

✅ A sua reserva foi confirmada com sucesso!

📋 DETALHES DA RESERVA:
• Cacifo: #{locker_number}
• PIN de Acesso: {pin}
• Data/Hora: {timestamp}
• Nome: {user_data.get('name', 'N/A')}
• Email: {user_data.get('email', 'N/A')}
• Telemóvel: {user_data.get('phone', 'N/A')}

🔓 COMO USAR:
1. Para abrir o cacifo, dirija-se ao terminal
2. Selecione "Unlock Locker"
3. Introduza o seu contacto e o PIN: {pin}
4. O cacifo será aberto automaticamente

⚠️ IMPORTANTE:
• Guarde este PIN em segurança
• Utilize apenas o contacto registado para acesso
• O cacifo fechará automaticamente após retirar os items

Obrigado por utilizar o nosso sistema!

---
Sistema de Cacifos Automático
Suporte: support@cacifo.com"""
            
            sms_body = f"Cacifo {locker_number} PIN: {pin}. Terminal > Unlock Locker"
        
        elif current_lang == 'en':
            email_subject = f"🔐 Locker {locker_number} PIN - Locker System"
            email_body = f"""Hello {user_data.get('name', 'Customer')},

✅ Your booking has been confirmed successfully!

📋 BOOKING DETAILS:
• Locker: #{locker_number}
• Access PIN: {pin}
• Date/Time: {timestamp}
• Name: {user_data.get('name', 'N/A')}
• Email: {user_data.get('email', 'N/A')}
• Phone: {user_data.get('phone', 'N/A')}

🔓 HOW TO USE:
1. Go to the terminal to open your locker
2. Select "Unlock Locker"
3. Enter your contact and PIN: {pin}
4. The locker will open automatically

⚠️ IMPORTANT:
• Keep this PIN secure
• Use only the registered contact for access
• The locker will close automatically after removing items

Thank you for using our system!

---
Automatic Locker System
Support: support@cacifo.com"""
            
            sms_body = f"Locker {locker_number} PIN: {pin}. Terminal > Unlock Locker"
        
        elif current_lang == 'es':
            email_subject = f"🔐 PIN de Taquilla {locker_number} - Sistema de Taquillas"
            email_body = f"""Hola {user_data.get('name', 'Cliente')},

✅ ¡Su reserva ha sido confirmada con éxito!

📋 DETALLES DE RESERVA:
• Taquilla: #{locker_number}
• PIN de Acceso: {pin}
• Fecha/Hora: {timestamp}
• Nombre: {user_data.get('name', 'N/A')}
• Email: {user_data.get('email', 'N/A')}
• Teléfono: {user_data.get('phone', 'N/A')}

🔓 CÓMO USAR:
1. Vaya al terminal para abrir su taquilla
2. Seleccione "Unlock Locker"
3. Introduzca su contacto y PIN: {pin}
4. La taquilla se abrirá automáticamente

⚠️ IMPORTANTE:
• Mantenga este PIN seguro
• Use solo el contacto registrado para acceso
• La taquilla se cerrará automáticamente después de retirar los artículos

¡Gracias por usar nuestro sistema!

---
Sistema de Taquillas Automático
Soporte: support@cacifo.com"""
            
            sms_body = f"Taquilla {locker_number} PIN: {pin}. Terminal > Unlock Locker"
        
        else:  # Default to English for other languages
            email_subject = f"🔐 Locker {locker_number} PIN - Locker System"
            email_body = f"""Hello {user_data.get('name', 'Customer')},

✅ Your booking has been confirmed successfully!

📋 BOOKING DETAILS:
• Locker: #{locker_number}
• Access PIN: {pin}
• Date/Time: {timestamp}

🔓 HOW TO USE:
1. Go to the terminal to open your locker
2. Select "Unlock Locker"  
3. Enter your contact and PIN: {pin}
4. The locker will open automatically

Thank you for using our system!

---
Automatic Locker System"""
            
            sms_body = f"Locker {locker_number} PIN: {pin}. Terminal > Unlock Locker"
        
        # Enviar Email
        if 'email' in notification_methods and user_data.get('email'):
            results['email'] = self.send_email(
                user_data['email'],
                email_subject,
                email_body
            )
        
        # Enviar SMS
        if 'sms' in notification_methods and user_data.get('phone'):
            # Tentar primeiro Twilio, depois TextBelt como fallback
            phone = user_data['phone']
            
            # Formato do número: garantir que tem código do país
            if not phone.startswith('+'):
                if phone.startswith('9'):  # Número português
                    phone = '+351' + phone
                else:
                    phone = '+351' + phone
            
            # Tentar Twilio primeiro
            sms_sent = self.send_sms_twilio(phone, sms_body)
            
            # Se Twilio falhar, tentar TextBelt
            if not sms_sent:
                sms_sent = self.send_sms_textbelt(phone, sms_body)
            
            results['sms'] = sms_sent
        
        return results
    
    def test_notifications(self, test_email="test@example.com", test_phone="+351912345678"):
        """Testar configurações de notificação"""
        print("🧪 Testando sistema de notificações...")
        
        test_user_data = {
            'name': 'Utilizador Teste',
            'email': test_email,
            'phone': test_phone,
            'birth_date': '01/01/1990'
        }
        
        test_pin = "1234"
        test_locker = "001"
        
        results = self.send_pin_notification(
            test_user_data,
            test_locker,
            test_pin,
            ['email', 'sms']
        )
        
        print(f"📧 Email: {'✅ Sucesso' if results['email'] else '❌ Falhou'}")
        print(f"📱 SMS: {'✅ Sucesso' if results['sms'] else '❌ Falhou'}")
        
        return results

# Instância global do serviço de notificações
notification_service = NotificationService()

# Exemplo de configuração (descomente e configure com suas credenciais reais)
# 
# Para Gmail:
# notification_service.configure_email(
#     smtp_server='smtp.gmail.com',
#     smtp_port=587,
#     sender_email='seu_email@gmail.com',
#     sender_password='sua_senha_de_app',  # Senha de app do Gmail, não a senha normal
#     sender_name='Sistema de Cacifos'
# )
#
# Para Twilio SMS:
# notification_service.configure_sms_twilio(
#     account_sid='seu_account_sid',
#     auth_token='seu_auth_token',
#     from_number='+1234567890'  # Seu número Twilio
# )
#
# Para TextBelt SMS (alternativa gratuita):
# notification_service.configure_sms_textbelt('textbelt')  # ou sua API key

if __name__ == '__main__':
    # Teste do sistema (apenas para desenvolvimento)
    print("Sistema de Notificações - Cacifo System")
    print("Configure as credenciais em notification_service.py para ativar")
    
    # Teste sem credenciais (apenas mostra como funcionaria)
    notification_service.test_notifications()