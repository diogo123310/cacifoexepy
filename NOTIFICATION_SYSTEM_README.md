# 📬 Sistema de Notificações por SMS e Email

## ✨ Funcionalidades Implementadas

O sistema de cacifos agora **envia automaticamente o PIN por SMS e/ou Email** quando um utilizador faz uma reserva!

### 🔄 Fluxo Automático
1. **Utilizador faz reserva** → Preenche dados (nome, email, telemóvel, data nascimento)
2. **Sistema gera PIN** → PIN único de 4 dígitos
3. **Cacifo abre fisicamente** → Pulso de 20ms enviado
4. **Notificações enviadas automaticamente**:
   - 📧 **Email detalhado** com instruções completas
   - 📱 **SMS rápido** com PIN e instruções básicas
5. **Popup de confirmação** → Mostra status das notificações (✅/❌)

---

## 📧 Email Template (7 idiomas)

```
🔐 PIN do Cacifo 001 - Sistema de Cacifos

Olá João Silva,

✅ A sua reserva foi confirmada com sucesso!

📋 DETALHES DA RESERVA:
• Cacifo: #001
• PIN de Acesso: 4582
• Data/Hora: 24/10/2025 às 21:30
• Nome: João Silva
• Email: joao.silva@example.com  
• Telemóvel: +351912345678

🔓 COMO USAR:
1. Para abrir o cacifo, dirija-se ao terminal
2. Selecione "Unlock Locker"
3. Introduza o seu contacto e o PIN: 4582
4. O cacifo será aberto automaticamente

⚠️ IMPORTANTE:
• Guarde este PIN em segurança
• Utilize apenas o contacto registado para acesso
• O cacifo fechará automaticamente após retirar os items

Obrigado por utilizar o nosso sistema!

---
Sistema de Cacifos Automático
Suporte: support@cacifo.com
```

---

## 📱 SMS Template

```
🔐 Cacifo #001 PIN: 4582. Use terminal 'Unlock Locker' com contacto+PIN. Guarde seguro!
```
*Optimizado para 1 SMS (< 160 caracteres)*

---

## ⚙️ Como Configurar

### 📧 1. Email (Gmail)

1. **Ative 2FA** na sua conta Google
2. **Gere Senha de App**:
   - Vá para https://myaccount.google.com/security
   - Procure "Passwords for apps" 
   - Gere senha para "Mail"
3. **Configure em `config_notifications.py`**:
   ```python
   # Descomentar e configurar:
   notification_service.configure_email(
       smtp_server='smtp.gmail.com',
       smtp_port=587,
       sender_email='seu_email@gmail.com',
       sender_password='sua_senha_de_app',  # NÃO a senha normal!
       sender_name='Sistema de Cacifos'
   )
   ```

### 📱 2. SMS Twilio (Pago - Recomendado)

1. **Crie conta** em https://www.twilio.com/
2. **Obtenha credenciais**:
   - Account SID
   - Auth Token  
   - Número de telefone Twilio
3. **Configure em `config_notifications.py`**:
   ```python
   # Descomentar e configurar:
   notification_service.configure_sms_twilio(
       account_sid='ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
       auth_token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
       from_number='+1234567890'
   )
   ```

### 📱 3. SMS TextBelt (Gratuito)

✅ **Já configurado!** 
- 1 SMS gratuito por dia
- Para mais SMS: https://textbelt.com/purchase

---

## 🧪 Como Testar

### Método 1: Usar o aplicativo
```bash
python main.py
```
1. Vá para "Find available lockers"
2. Selecione um cacifo
3. Preencha o formulário com **dados reais**
4. Veja as notificações sendo enviadas no log

### Método 2: Demonstração
```bash
python demo_notifications.py
```

### Método 3: Teste isolado
```bash
python config_notifications.py
```

---

## 📊 Status de Implementação

| Funcionalidade | Status | Detalhes |
|---|---|---|
| ✅ **Sistema base** | Implementado | Integração completa com booking |
| ✅ **Email multi-idioma** | Implementado | 7 idiomas: PT, EN, ES, FR, DE, IT, PL |
| ✅ **SMS otimizado** | Implementado | Mensagens < 160 caracteres |
| ✅ **Auto-detecção país** | Implementado | +351 para números portugueses |
| ✅ **Fallback SMS** | Implementado | TextBelt como backup |
| ✅ **Status no popup** | Implementado | ✅/❌ para email e SMS |
| ✅ **Logs detalhados** | Implementado | Debug completo no console |
| ⚙️ **Configuração** | Pendente | Requer credenciais Gmail/Twilio |

---

## 🔍 Debug e Logs

O sistema fornece logs detalhados:

```
📧📱 Enviando notificações para João Silva...
⚠️ Email não configurado - configurações necessárias
✅ SMS TextBelt configurado (1 SMS gratuito por dia)
📧 Email: ❌ Falhou (configuração necessária)
📱 SMS: ✅ Enviado com sucesso
```

---

## 🚀 Produção

### Configuração Recomendada
- **Email**: Gmail com senha de app
- **SMS Principal**: Twilio (confiável, pago)  
- **SMS Backup**: TextBelt (gratuito limitado)

### Custos
- **Email**: Gratuito (Gmail)
- **SMS Twilio**: ~€0,05 por SMS
- **SMS TextBelt**: 1 gratuito/dia, depois €0,10 por SMS

---

## 📱 Exemplos de Notificação por Idioma

### 🇵🇹 Português
```
Email: "🔐 PIN do Cacifo 001 - Sistema de Cacifos"
SMS: "🔐 Cacifo #001 PIN: 4582. Use terminal 'Unlock Locker' com contacto+PIN. Guarde seguro!"
```

### 🇬🇧 English  
```
Email: "🔐 Locker 001 PIN - Locker System"
SMS: "🔐 Locker #001 PIN: 4582. Use terminal 'Unlock Locker' with contact+PIN. Keep safe!"
```

### 🇪🇸 Español
```
Email: "🔐 PIN de Taquilla 001 - Sistema de Taquillas"  
SMS: "🔐 Taquilla #001 PIN: 4582. Use terminal 'Unlock Locker' con contacto+PIN. Mantener seguro!"
```

---

## 🎯 Resultado Final

✅ **Sistema 100% funcional** - Pronto para envio real de notificações
✅ **Integração transparente** - Funciona automaticamente no fluxo existente  
✅ **Multi-idioma completo** - Emails e SMS em 7 idiomas
✅ **Fallback robusto** - Múltiplas opções de SMS
✅ **Configuração flexível** - Email e/ou SMS conforme necessário
✅ **Status em tempo real** - Utilizador vê se notificações foram enviadas

**🔧 Para ativar: Configure credenciais em `config_notifications.py`**