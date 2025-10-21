# 🌐 API de Acesso Remoto ao Sistema de Cacifos

## 📖 Guia Completo de Instalação e Uso

### 🎯 **O que foi implementado?**

Implementamos uma solução completa para acessar a base de dados SQLite do sistema de cacifos **remotamente** através da rede. Agora você pode consultar reservas, ver estatísticas e exportar dados de qualquer computador!

---

## 🏗️ **Arquitetura da Solução**

```
┌─────────────────────┐    HTTP/API    ┌─────────────────────┐
│   Seu Computador    │ ◄──────────► │   Raspberry Pi      │
│                     │               │                     │
│ • remote_client.py  │               │ • database_api.py   │
│ • Browser Web       │               │ • locker_system.db  │
│ • Interface Gráfica │               │ • Sistema Principal │
└─────────────────────┘               └─────────────────────┘
```

---

## 📂 **Arquivos Criados**

### 1. **`database_api.py`** - Servidor Flask
- 🔥 **API REST completa** com endpoints para todas as consultas
- 🎨 **Interface web bonita** acessível via navegador
- 📊 **Dashboard em tempo real** com estatísticas
- 📱 **Responsivo** - funciona no telemóvel também
- 🔄 **Auto-refresh** a cada 30 segundos

### 2. **`remote_client.py`** - Cliente de Acesso Remoto
- 🖥️ **Menu interativo** no terminal
- 🔍 **Todas as funcionalidades de consulta**
- 🌐 **Abre interface web automaticamente**
- 📄 **Exportação de dados** para CSV
- ⚡ **Testes de conectividade**

---

## 🚀 **Como Usar - Passo a Passo**

### **PASSO 1: No Raspberry Pi (Servidor)**

```bash
# 1. Ir para a pasta do projeto
cd /home/pi/cacifoexepy

# 2. Instalar dependências (se necessário)
pip install flask flask-cors

# 3. Iniciar o servidor API
python database_api.py
```

**✅ Resultado esperado:**
```
🚀 LOCKER SYSTEM DATABASE API
📊 Starting Database API Server...
📱 Web Interface: http://localhost:5000
🌐 Network Access: http://YOUR_IP:5000
* Running on http://127.0.0.1:5000
* Running on http://192.168.1.100:5000  ← Este é o IP importante!
```

### **PASSO 2: No Seu Computador (Cliente)**

#### **Opção A: Interface Web (Recomendado)**
1. **Abrir navegador**
2. **Ir para:** `http://IP_DO_RASPBERRY:5000`
3. **Usar a interface gráfica** - tudo funciona via cliques!

#### **Opção B: Cliente Terminal**
```bash
# 1. Editar o IP no remote_client.py
# Alterar: RASPBERRY_PI_IP = "192.168.1.100"  # IP do seu Raspberry Pi

# 2. Executar o cliente
python remote_client.py

# 3. Usar o menu interativo
# Escolher opções 1-9 para diferentes consultas
```

---

## 🔧 **Configuração de Rede**

### **Como descobrir o IP do Raspberry Pi?**

**No Raspberry Pi, executar:**
```bash
hostname -I
```
ou
```bash
ifconfig | grep "inet "
```

### **IP típicos por rede:**
- **WiFi doméstico:** `192.168.1.X` ou `192.168.0.X`
- **Hotspot móvel:** `192.168.43.X`
- **Rede corporativa:** Varia (perguntar ao admin de rede)

---

## 🌟 **Funcionalidades Disponíveis**

### **📊 Interface Web (`http://IP:5000`)**
- ✅ **Dashboard em tempo real** com estatísticas
- ✅ **Consulta todas as reservas** (paginadas)
- ✅ **Filtro por reservas ativas**
- ✅ **Pesquisa por contacto**
- ✅ **Reservas recentes** (últimos 7 dias)
- ✅ **Estatísticas detalhadas** (locker mais usado, etc.)
- ✅ **Exportação CSV** via download
- ✅ **Auto-refresh** automático
- ✅ **Design responsivo** (funciona no telemóvel)

### **🖥️ Cliente Terminal (`remote_client.py`)**
- ✅ **Menu interativo** fácil de usar
- ✅ **Todas as consultas** da interface web
- ✅ **Teste de conectividade**
- ✅ **Abre interface web** automaticamente
- ✅ **Exportação CSV** local

### **🔗 API REST (`/api/*`)**
- ✅ **GET /api/bookings** - Todas as reservas
- ✅ **GET /api/bookings/active** - Reservas ativas
- ✅ **GET /api/bookings/recent** - Reservas recentes
- ✅ **GET /api/bookings/contact/<nome>** - Pesquisa por contacto
- ✅ **GET /api/bookings/locker/<numero>** - Histórico do locker
- ✅ **GET /api/stats** - Estatísticas completas
- ✅ **GET /api/export** - Exportar CSV
- ✅ **GET /api/status** - Status do sistema

---

## 🛠️ **Resolução de Problemas**

### **❌ "Erro de conexão"**
**Verificar:**
1. ✅ Servidor API está rodando no Raspberry Pi?
2. ✅ IP está correto no cliente?
3. ✅ Firewall não está bloqueando a porta 5000?
4. ✅ Computadores estão na mesma rede WiFi?

### **❌ "Database not found"**
**Verificar:**
1. ✅ Arquivo `locker_system.db` existe?
2. ✅ Executando API na pasta correta?
3. ✅ Permissões de leitura do arquivo?

### **❌ Interface web não carrega**
**Tentar:**
1. ✅ `http://localhost:5000` (no próprio Raspberry Pi)
2. ✅ `http://127.0.0.1:5000` (alternativo local)
3. ✅ Verificar se porta 5000 não está ocupada

---

## 🔐 **Considerações de Segurança**

### **⚠️ Rede Local Apenas**
- A API atual funciona **apenas na rede local** (WiFi doméstico)
- **Não está acessível pela internet** (mais seguro)
- Para acesso via internet, seria necessário configuração adicional

### **🔒 Dados Apenas de Leitura**
- A API atual permite **apenas consulta** de dados
- **Não é possível criar/editar/apagar** reservas remotamente
- O sistema principal continua sendo a interface física

---

## 📱 **Casos de Uso Práticos**

### **👨‍💼 Administrador**
```
📊 Dashboard web sempre aberto para monitorizar sistema
📈 Consultar estatísticas diárias
📋 Verificar reservas ativas em tempo real
📄 Exportar relatórios semanais
```

### **👩‍🔧 Técnico de Manutenção**  
```
🔍 Pesquisar histórico de problemas por locker
📞 Consultar contactos de utilizadores
🔄 Verificar padrões de utilização
📊 Identificar lockers com mais avarias
```

### **📈 Análise de Dados**
```
📄 Exportar dados para Excel/análise
📊 Criar gráficos de utilização
🏆 Identificar períodos de pico
📍 Otimizar localização dos cacifos
```

---

## 🎯 **Próximos Passos**

### **Para Desenvolvimento Futuro:**
1. **🔐 Sistema de autenticação** (login/password)
2. **📧 Notificações por email** de reservas
3. **📱 App móvel nativo** (Android/iOS)
4. **🌐 Acesso via internet** (com VPN/tunneling)
5. **📊 Relatórios automáticos** (PDF)
6. **🔔 Alertas em tempo real** (WebSocket)

### **Para Produção:**
1. **🔒 HTTPS** em vez de HTTP
2. **🗃️ Servidor web robusto** (nginx + gunicorn)
3. **📊 Logging completo** de acessos
4. **⚡ Cache** para melhor performance
5. **🔄 Backup automático** da base de dados

---

## 📞 **Suporte**

Se tiver problemas:

1. **🔍 Verificar logs** no terminal onde roda `database_api.py`
2. **🌐 Testar API diretamente:** `http://IP:5000/api/status`
3. **🔄 Reiniciar servidor API** se necessário
4. **📋 Verificar dependências:** `flask`, `flask-cors` instaladas

---

## 🎉 **Resumo do que consegue fazer agora:**

✅ **Consultar reservas de qualquer computador na rede**  
✅ **Interface web moderna e intuitiva**  
✅ **Estatísticas em tempo real**  
✅ **Exportação de dados para análise**  
✅ **Pesquisa avançada por múltiplos critérios**  
✅ **Monitorização remota do sistema**  

**🚀 O seu sistema de cacifos agora é verdadeiramente moderno e acessível remotamente!**