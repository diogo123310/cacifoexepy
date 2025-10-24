# 🏪 Sistema de Cacifos Inteligente (CacifoExePy)

Sistema completo de gestão de cacifos com interface touchscreen, notificações automáticas e gestão web remota.

## 🚀 Funcionalidades Principais

### 📱 Interface Touchscreen
- **Interface Kivy** otimizada para dispositivos touchscreen
- **Navegação intuitiva** com ícones e instruções claras
- **Suporte multi-idioma** (7 idiomas: PT, EN, ES, FR, DE, IT, PL)
- **Design responsivo** adaptado para diferentes tamanhos de ecrã

### 👤 Sistema de Contactos Detalhados
- **Formulário completo** com nome, email, telefone e data de nascimento
- **Campos separados** na base de dados para melhor organização
- **Validação automática** de dados de entrada
- **Migração automática** de bases de dados existentes

### 🔍 Pesquisa Avançada
- **Pesquisa inteligente** por nome, email ou telefone
- **Resultados instantâneos** com todos os dados
- **Interface web moderna** para gestão remota
- **Filtros múltiplos** para encontrar reservas rapidamente

### 📧 Sistema de Notificações
- **Email automático** via Gmail SMTP
- **SMS** via Twilio ou TextBelt
- **Templates multi-idioma** para notificações
- **Modo demonstração** para testes
- **Fallback gracioso** quando serviços estão indisponíveis

### 🌐 Interface Web de Gestão
- **Dashboard completo** com estatísticas em tempo real
- **Visualização detalhada** de todas as reservas
- **Informações de contacto separadas** (nome, email, telefone)
- **Exportação de dados** em CSV
- **API REST** para integração externa

## 📋 Requisitos do Sistema

### Hardware
- **Raspberry Pi 4** (recomendado) ou computador com Linux/Windows
- **Ecrã touchscreen** (7" ou superior)
- **Módulos de controlo GPIO** para fechaduras eletrónicas
- **Conexão à Internet** para notificações

### Software
- **Python 3.8+**
- **Kivy** para interface touchscreen
- **Flask** para interface web
- **SQLite** para base de dados
- **GPIO** para controlo de hardware (Raspberry Pi)

## 🛠️ Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone https://github.com/diogo123310/cacifoexepy.git
cd cacifoexepy
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Notificações
```bash
python config_notifications.py
```
Siga as instruções para configurar:
- Gmail (email + app password)
- Twilio (SMS) - opcional

### 4. Executar Sistema Principal
```bash
python main.py
```

### 5. Executar Interface Web
```bash
python start_web.bat
# ou
python database_api.py
```
Acesse: `http://localhost:5000`

## 📊 Estrutura da Base de Dados

### Tabela `bookings`
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    locker_number TEXT NOT NULL,
    contact TEXT NOT NULL,           -- Campo legado (compatibilidade)
    name TEXT,                       -- Nome completo
    email TEXT,                      -- Email
    phone TEXT,                      -- Telefone com indicativo
    birth_date TEXT,                 -- Data de nascimento
    pin_hash TEXT NOT NULL,
    pin_salt TEXT NOT NULL,
    pin_display TEXT,                -- PIN visível (apenas para demo)
    status TEXT DEFAULT 'booked',
    booking_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    unlock_time DATETIME,
    return_time DATETIME,
    notes TEXT
);
```

## 🌐 API Endpoints

### Reservas
- `GET /api/bookings` - Todas as reservas
- `GET /api/bookings/active` - Reservas ativas
- `GET /api/bookings/recent` - Reservas recentes
- `GET /api/bookings/contact/<termo>` - Pesquisa por nome, email ou telefone

### Estatísticas
- `GET /api/stats` - Estatísticas do sistema
- `GET /api/status` - Status dos cacifos

### Dados
- `GET /api/export` - Exportar dados em CSV

## 🎯 Casos de Uso

### 👥 Para Utilizadores Finais
1. **Selecionar cacifo disponível** na interface touchscreen
2. **Preencher dados pessoais** (nome, email, telefone, data nascimento)
3. **Receber PIN** automaticamente gerado
4. **Receber notificação** por email/SMS com o PIN
5. **Usar PIN** para desbloquear o cacifo posteriormente

### 🔧 Para Administradores
1. **Aceder interface web** em `http://localhost:5000`
2. **Ver todas as reservas** com dados detalhados
3. **Pesquisar utilizadores** por qualquer campo
4. **Exportar dados** para análise
5. **Monitorizar estatísticas** em tempo real

## 📁 Estrutura de Ficheiros

```
cacifoexepy/
├── main.py                      # Aplicação principal Kivy
├── database.py                  # Gestão da base de dados SQLite
├── database_api.py              # Interface web Flask
├── contact_pin_screen.py        # Ecrã de formulário de contacto
├── notification_service.py     # Sistema de notificações
├── config_notifications.py     # Configuração de notificações
├── translations.py              # Sistema de traduções
├── pricing_screen.py            # Página de preços
├── how_it_works_screen.py       # Página explicativa
├── demo_mode.py                 # Modo demonstração
├── start_web.bat               # Script para iniciar interface web
├── requirements.txt            # Dependências Python
└── README.md                   # Esta documentação
```

## 🧪 Testes e Verificação

### Testar Funcionalidades de Contacto
```bash
python test_contact_features.py
```

### Verificar Dados na Base de Dados
```bash
python verify_contact_data.py
```

### Modo Demonstração (Notificações)
```bash
python demo_mode.py
```

## 🔧 Configuração Avançada

### Personalizar Idiomas
Edite `translations.py` para adicionar novos idiomas ou modificar traduções existentes.

### Configurar GPIO
Modifique as configurações de pinos GPIO em `main.py` conforme o seu hardware.

### Personalizar Templates de Email
Edite `notification_service.py` para personalizar templates de notificação.

## 📈 Melhorias Implementadas

### ✅ Base de Dados
- [x] Campos separados para dados de contacto
- [x] Migração automática de dados existentes
- [x] Compatibilidade com código anterior
- [x] Logs detalhados do sistema

### ✅ Interface
- [x] Formulário completo de dados pessoais
- [x] Interface web renovada e profissional
- [x] Pesquisa avançada multi-campo
- [x] Design responsivo

### ✅ Notificações
- [x] Sistema completo email + SMS
- [x] Templates multi-idioma
- [x] Modo demonstração para testes
- [x] Configuração simplificada

### ✅ Funcionalidades
- [x] Páginas de preços e instruções
- [x] Sistema de traduções completo
- [x] Scripts de teste e verificação
- [x] Documentação completa

## 🛟 Suporte e Contribuição

### Reportar Problemas
Crie uma issue no GitHub com:
- Descrição detalhada do problema
- Steps para reproduzir
- Logs relevantes
- Informações do sistema

### Contribuir
1. Fork do repositório
2. Criar branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das alterações (`git commit -m 'Adicionar nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Criar Pull Request

## 📄 Licença

Este projeto está sob licença [MIT](LICENSE).

## 👨‍💻 Autor

**Diogo** - [GitHub](https://github.com/diogo123310)

---

**🎉 Sistema completo e funcional para gestão profissional de cacifos com informações detalhadas de contacto!**