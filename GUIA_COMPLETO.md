# 📦 ESTOQUE QUALIFICA — GUIA COMPLETO
## Do zero ao deploy, passo a passo para iniciantes

---

## ✅ O QUE VOCÊ VAI PRECISAR ANTES DE COMEÇAR

- Python 3.10 ou superior instalado
- Git instalado
- Conta no GitHub (gratuita): https://github.com
- Conta no PythonAnywhere (gratuita): https://www.pythonanywhere.com
- (Opcional) Chave da API OpenAI: https://platform.openai.com

---

## 🖥️ PARTE 1 — RODANDO NO SEU COMPUTADOR (LOCAL)

### PASSO 1 — Criar a pasta e entrar nela

Abra o terminal (Prompt de Comando no Windows, Terminal no Mac/Linux):

```bash
# Windows (use o Prompt de Comando ou PowerShell)
cd C:\Users\SEU_NOME
mkdir projetos
cd projetos

# Mac / Linux
cd ~
mkdir projetos
cd projetos
```

---

### PASSO 2 — Copiar o projeto para a pasta

Se você baixou como ZIP:
1. Extraia o ZIP
2. Mova a pasta `estoque_qualifica` para dentro da pasta `projetos`
3. No terminal: `cd estoque_qualifica`

Se você vai clonar do GitHub (depois que subir):
```bash
git clone https://github.com/SEU_USUARIO/estoque_qualifica.git
cd estoque_qualifica
```

---

### PASSO 3 — Criar o Ambiente Virtual

O ambiente virtual isola as bibliotecas do projeto para não misturar com outros projetos:

```bash
# Cria o ambiente virtual (só faz isso uma vez)
python -m venv venv

# Ativa o ambiente virtual
# Windows:
venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```

> ✅ Você saberá que funcionou quando ver `(venv)` no início da linha do terminal.
> ⚠️  Toda vez que abrir um novo terminal, você precisa ativar o venv novamente!

---

### PASSO 4 — Instalar as dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

Aguarde instalar tudo. Pode levar alguns minutos na primeira vez.

---

### PASSO 5 — Criar o arquivo .env com as configurações

```bash
# Copia o arquivo de exemplo
# Windows:
copy .env.example .env

# Mac / Linux:
cp .env.example .env
```

Agora abra o arquivo `.env` com qualquer editor de texto (Bloco de Notas, VS Code, etc) e edite:

```
SECRET_KEY=coloque-qualquer-texto-longo-aqui-123456789
DEBUG=True
OPENAI_API_KEY=sk-sua-chave-aqui  ← opcional, pode deixar em branco
```

> 💡 Se não tiver a chave OpenAI, deixe `OPENAI_API_KEY=` em branco.
> O sistema vai funcionar normalmente — só a análise de IA vai usar modo offline.

---

### PASSO 6 — Criar o banco de dados

Estes comandos criam as tabelas no banco de dados SQLite:

```bash
# Cria os arquivos de migração (mapeamento do banco)
python manage.py makemigrations accounts
python manage.py makemigrations fornecedores
python manage.py makemigrations produtos
python manage.py makemigrations movimentacoes
python manage.py makemigrations

# Aplica as migrações (cria as tabelas no banco)
python manage.py migrate
```

---

### PASSO 7 — Popular o banco com dados de exemplo

Este comando cria usuários, produtos, fornecedores e movimentações de exemplo:

```bash
python manage.py seed_dados
```

Você verá uma mensagem assim:
```
✅ SEED CONCLUÍDO COM SUCESSO!
  👤 Usuários: 2
  🏷️  Categorias: 8
  🏢 Fornecedores: 5
  📦 Produtos: 15
  📊 Movimentações: 8
  🔑 Login de ADMIN: admin / admin123
  🔑 Login de Funcionário: funcionario / func123
```

---

### PASSO 8 — Coletar os arquivos estáticos

```bash
python manage.py collectstatic --noinput
```

---

### PASSO 9 — Iniciar o servidor

```bash
python manage.py runserver
```

Você verá:
```
Starting development server at http://127.0.0.1:8000/
```

Abra o navegador em: **http://127.0.0.1:8000**

🎉 **Pronto! O sistema está rodando!**

Login com: `admin` / `admin123`

---

## 🌐 PARTE 2 — SUBINDO NO GITHUB

### PASSO 1 — Criar repositório no GitHub

1. Acesse https://github.com e entre na sua conta
2. Clique no botão **"New"** (verde, canto superior esquerdo)
3. Nome do repositório: `estoque_qualifica`
4. Deixe como **Public** (público) ou **Private** (privado)
5. **NÃO** marque "Add a README file"
6. Clique em **"Create repository"**

---

### PASSO 2 — Configurar o Git na pasta do projeto

No terminal, dentro da pasta `estoque_qualifica`:

```bash
# Inicia o git na pasta (só faz isso uma vez)
git init

# Configura seu nome e email (só faz isso uma vez no computador)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Adiciona todos os arquivos
git add .

# Cria o primeiro commit (salva o estado atual)
git commit -m "Primeiro commit - Sistema Estoque Qualifica"

# Conecta com o repositório do GitHub
# Substitua SEU_USUARIO pelo seu username do GitHub
git remote add origin https://github.com/SEU_USUARIO/estoque_qualifica.git

# Envia para o GitHub
git push -u origin main
```

> 💡 O Git vai pedir seu usuário e senha do GitHub.
> Hoje o GitHub pede um "token" no lugar da senha.
> Crie em: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

---

## 🚀 PARTE 3 — DEPLOY NO PYTHONANYWHERE

### PASSO 1 — Criar conta no PythonAnywhere

1. Acesse https://www.pythonanywhere.com
2. Clique em **"Start running Python online in less than a minute!"**
3. Escolha **"Create a Beginner account"** (gratuito)
4. Preencha: username, email, senha
5. Confirme o email

> ⚠️ O username vira parte da URL do sistema: `seuusername.pythonanywhere.com`

---

### PASSO 2 — Abrir o Console do PythonAnywhere

1. No painel do PythonAnywhere, clique em **"Consoles"**
2. Clique em **"Bash"** para abrir o terminal

---

### PASSO 3 — Clonar o projeto do GitHub

No console do PythonAnywhere:

```bash
# Entra na pasta home
cd ~

# Clona o projeto do GitHub
git clone https://github.com/SEU_USUARIO/estoque_qualifica.git

# Entra na pasta
cd estoque_qualifica
```

---

### PASSO 4 — Criar ambiente virtual no PythonAnywhere

```bash
# Cria o ambiente virtual com Python 3.10
mkvirtualenv estoque_qualifica --python=python3.10

# O ambiente já ativa automaticamente. Se precisar ativar depois:
workon estoque_qualifica
```

---

### PASSO 5 — Instalar as dependências

```bash
pip install -r requirements.txt
```

---

### PASSO 6 — Criar o arquivo .env no PythonAnywhere

```bash
# Cria o arquivo .env
nano .env
```

Cole o conteúdo abaixo (edite os valores):
```
SECRET_KEY=uma-chave-super-secreta-e-longa-para-producao-12345
DEBUG=False
OPENAI_API_KEY=sk-sua-chave-aqui
```

Salve: **Ctrl+X**, depois **Y**, depois **Enter**

---

### PASSO 7 — Configurar o banco de dados

```bash
python manage.py makemigrations accounts
python manage.py makemigrations fornecedores
python manage.py makemigrations produtos
python manage.py makemigrations movimentacoes
python manage.py makemigrations
python manage.py migrate
python manage.py seed_dados
python manage.py collectstatic --noinput
```

---

### PASSO 8 — Configurar o Web App no PythonAnywhere

1. No painel do PythonAnywhere, clique em **"Web"**
2. Clique em **"Add a new web app"**
3. Clique em **"Next"**
4. Escolha **"Manual configuration"** (NÃO escolha Django)
5. Escolha **"Python 3.10"**
6. Clique em **"Next"**

---

### PASSO 9 — Configurar o arquivo WSGI

1. Na página do Web App, procure **"WSGI configuration file"**
2. Clique no link (algo como `/var/www/SEU_USUARIO_pythonanywhere_com_wsgi.py`)
3. **Delete TODO o conteúdo** do arquivo
4. Cole o conteúdo abaixo, substituindo `SEU_USUARIO` pelo seu username:

```python
import sys
import os

# Caminho do projeto
PASTA_PROJETO = '/home/SEU_USUARIO/estoque_qualifica'
if PASTA_PROJETO not in sys.path:
    sys.path.insert(0, PASTA_PROJETO)

# Ambiente virtual
VIRTUALENV = '/home/SEU_USUARIO/.virtualenvs/estoque_qualifica/lib/python3.10/site-packages'
if VIRTUALENV not in sys.path:
    sys.path.insert(0, VIRTUALENV)

# Variáveis de ambiente
os.environ['DJANGO_SETTINGS_MODULE'] = 'estoque_qualifica.settings'
os.environ['SECRET_KEY'] = 'sua-chave-secreta-aqui'
os.environ['DEBUG'] = 'False'
os.environ['OPENAI_API_KEY'] = 'sk-sua-chave-aqui'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. Clique em **"Save"**

---

### PASSO 10 — Configurar arquivos estáticos

Na página do Web App, procure **"Static files"** e adicione:

| URL         | Directory                                      |
|-------------|------------------------------------------------|
| `/static/`  | `/home/SEU_USUARIO/estoque_qualifica/staticfiles` |
| `/media/`   | `/home/SEU_USUARIO/estoque_qualifica/media`    |

---

### PASSO 11 — Reiniciar o app

1. Na página do Web App, clique no botão verde **"Reload SEU_USUARIO.pythonanywhere.com"**
2. Aguarde alguns segundos
3. Acesse: `https://SEU_USUARIO.pythonanywhere.com`

🎉 **Seu sistema está no ar!**

---

## 🔄 PARTE 4 — ATUALIZANDO O SISTEMA DEPOIS

Sempre que fizer mudanças no código e quiser atualizar no PythonAnywhere:

**No seu computador:**
```bash
git add .
git commit -m "Descreva o que mudou"
git push
```

**No console do PythonAnywhere:**
```bash
cd ~/estoque_qualifica
git pull
python manage.py migrate
python manage.py collectstatic --noinput
```

Depois clique em **"Reload"** na página Web do PythonAnywhere.

---

## ❓ PROBLEMAS COMUNS E SOLUÇÕES

### "ModuleNotFoundError: No module named 'django'"
→ O ambiente virtual não está ativado. Rode: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)

### "django.db.utils.OperationalError: no such table"
→ Esqueceu de rodar as migrações. Rode: `python manage.py migrate`

### "PermissionError" ao fazer upload de imagem
→ Crie a pasta media: `mkdir media`

### "500 Internal Server Error" no PythonAnywhere
→ Veja os logs em: Web → Log files → Error log

### A IA não funciona
→ Verifique se a `OPENAI_API_KEY` está correta no arquivo `.env`
→ O sistema funciona sem a API da OpenAI usando análise local automática

---

## 📂 ESTRUTURA DO PROJETO (para entender o código)

```
estoque_qualifica/
├── manage.py               ← Ferramenta de linha de comando do Django
├── requirements.txt        ← Lista de bibliotecas necessárias
├── .env.example            ← Modelo do arquivo de configuração
├── .gitignore              ← Arquivos que o Git ignora
│
├── estoque_qualifica/      ← Configurações do projeto
│   ├── settings.py         ← Configurações principais
│   └── urls.py             ← Rotas principais
│
├── accounts/               ← App de usuários e autenticação
│   ├── models.py           ← Modelo de usuário
│   ├── views.py            ← Lógica de login/cadastro
│   ├── forms.py            ← Formulários
│   └── urls.py             ← Rotas de usuário
│
├── fornecedores/           ← App de fornecedores (CRUD completo)
├── produtos/               ← App de produtos (CRUD completo)
├── movimentacoes/          ← App de entradas e saídas
├── relatorios/             ← App de relatórios e gráficos
├── core/                   ← App principal: dashboard + IA
│   └── management/
│       └── commands/
│           └── seed_dados.py  ← Comando para popular o banco
│
├── templates/              ← Todos os arquivos HTML
│   ├── base.html           ← Template base (sidebar, header)
│   ├── registration/       ← Tela de login
│   ├── core/               ← Dashboard
│   ├── accounts/           ← Telas de usuário
│   ├── fornecedores/       ← Telas de fornecedor
│   ├── produtos/           ← Telas de produto
│   ├── movimentacoes/      ← Telas de movimentação
│   └── relatorios/         ← Telas de relatório
│
└── static/                 ← Arquivos estáticos
    ├── manifest.json       ← Configuração do PWA
    ├── sw.js               ← Service Worker (offline)
    └── icons/              ← Ícones do sistema
```

---

## 🔑 CREDENCIAIS PADRÃO APÓS O SEED

| Perfil      | Usuário      | Senha    | Permissões                        |
|-------------|--------------|----------|-----------------------------------|
| Admin       | `admin`      | `admin123` | Acesso total ao sistema          |
| Funcionário | `funcionario`| `func123`  | Pode ver e registrar movimentações|

> ⚠️ Troque as senhas antes de usar em produção!
> Admin Panel: `http://seusite/admin/`

---

Dúvidas? O código tem comentários em português em todas as funções.
Boa sorte com o Estoque Qualifica! 🚀
