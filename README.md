# ComunicaSaaS

Plataforma SaaS para automação de comunicação empresarial e gestão de agendamentos.

## Visão Geral

O ComunicaSaaS é uma plataforma web que centraliza a comunicação entre empresas e seus clientes, automatizando tarefas como:

- Gerenciamento de clientes e leads
- Agendamento de compromissos com lembretes automáticos
- Integração com WhatsApp e Instagram
- Envio automático de e-mails
- Respostas automáticas com inteligência artificial
- Painel administrativo com logs de auditoria

## Tecnologias

- **Backend:** Python / Django
- **Frontend:** Django Templates + Bootstrap 5
- **Banco de Dados:** SQLite (dev) / PostgreSQL (produção)
- **Fila de Tarefas:** Celery + Redis
- **Autenticação:** django-allauth (Google, Apple)

## Requisitos

- Python 3.10+
- Redis (para Celery)
- Pip

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/YOUR_USER/comunicacao-saas.git
cd comunicacao-saas
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Executar migrações

```bash
python manage.py migrate
```

### 6. Criar superusuário

```bash
python manage.py createsuperuser
```

### 7. Iniciar o servidor

```bash
python manage.py runserver
```

Acesse: http://localhost:8000

### 8. Iniciar o Celery (para lembretes automáticos)

```bash
celery -A config worker -l info
celery -A config beat -l info
```

## Estrutura do Projeto

```
comunicacao-saas/
├── accounts/          # Autenticação e gestão de usuários
├── appointments/      # Agendamentos e lembretes
├── auditlog/          # Logs de auditoria
├── clients/           # Gestão de clientes e leads
├── communications/    # Integrações (WhatsApp, Instagram, Email, IA)
├── config/            # Configurações Django
├── dashboard/         # Painel administrativo
├── static/            # Arquivos estáticos (CSS, JS)
├── templates/         # Templates HTML
├── manage.py
└── requirements.txt
```

## Funcionalidades

### Autenticação (RF-01, RF-02)
- Cadastro e login de usuários
- Login social (Google, Apple)
- Controle de acesso por perfil (Admin, Gerente, Funcionário)

### Gestão de Clientes (RF-03, RF-04)
- CRUD completo de clientes
- Gestão de leads com conversão para clientes
- Busca e filtros por status

### Agendamentos (RF-05, RF-06)
- Criação e gestão de compromissos
- Visualização em calendário (FullCalendar)
- Lembretes automáticos via Celery

### Comunicação (RF-07, RF-08, RF-09)
- Integração com WhatsApp (stub)
- Integração com Instagram (stub)
- Envio de e-mails automáticos
- Histórico de interações por cliente

### Painel Administrativo (RF-10)
- Dashboard com estatísticas
- Visão geral de clientes, leads e agendamentos

### Inteligência Artificial (RF-11)
- Geração de respostas automáticas (stub para API OpenAI)

### Auditoria (RF-12)
- Registro de todas as ações dos usuários
- Filtros por ação e usuário

## Modelo SaaS

O sistema utiliza o modelo multi-tenant com a entidade `Company`:
- Cada empresa possui seus próprios dados isolados
- Usuários são associados a uma empresa
- Todos os dados são filtrados pela empresa do usuário logado

## LGPD

O sistema implementa princípios da LGPD:
- Dados pessoais armazenados de forma segura
- Logs de auditoria para rastreabilidade
- Possibilidade de exclusão de dados de clientes

## Licença

Este projeto é de uso acadêmico.
