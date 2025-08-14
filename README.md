# Wine IA - Configuração do Ambiente de Desenvolvimento

Este guia explica como configurar o ambiente de desenvolvimento para o projeto Wine IA, incluindo criação de ambiente virtual Python e controle de versão com Git.

## 📋 Pré-requisitos

- Python 3.8+ instalado
- Git instalado
- VS Code (opcional, mas recomendado)

## 🐍 Ambiente Virtual Python

### Criando o Ambiente Virtual

```cmd
# Navegar para o diretório do projeto
cd c:\Projetos\wine_ia

# Criar ambiente virtual
python -m venv .venv
```

### Ativando o Ambiente Virtual

**Windows (Command Prompt):**
```cmd
.\.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Verificar se está ativo:**
```cmd
# O prompt deve mostrar (.venv) no início
# Verificar localização do Python
where python
```

### Desativando o Ambiente

```cmd
deactivate
```

### Instalando Dependências

```cmd
# Com ambiente ativo, instalar pacotes
pip install pandas numpy matplotlib scikit-learn jupyter

# Ou instalar de requirements.txt
pip install -r requirements.txt

# Gerar arquivo requirements.txt
pip freeze > requirements.txt
```

## 🔧 VS Code - Configuração Automática

### Configurações Recomendadas

Adicione ao arquivo `.vscode/settings.json`:

```json
{
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true,
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe"
}
```

### Comandos VS Code

- `Ctrl+Shift+P` → `Python: Select Interpreter` → Escolher `./.venv/Scripts/python.exe`
- `Ctrl+Shift+P` → `Python: Create Terminal` → Terminal com ambiente ativo

## 📦 Git - Controle de Versão

### Inicializando Repositório

```cmd
# Inicializar repositório Git
git init

# Configurar usuário (primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### Criando .gitignore

Crie o arquivo `.gitignore` na raiz do projeto:

```gitignore
# Ambiente Virtual
.venv/
env/
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Jupyter Notebook
.ipynb_checkpoints

# VS Code
.vscode/
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json

# Sistema
.DS_Store
Thumbs.db

# Dados sensíveis
*.csv
*.xlsx
data/
models/
```

### Comandos Git Básicos

```cmd
# Adicionar arquivos
git add .

# Fazer commit
git commit -m "Initial commit: projeto wine IA"

# Conectar com repositório remoto
git remote add origin https://github.com/usuario/wine_ia.git

# Enviar para repositório remoto
git push -u origin main

# Verificar status
git status

# Ver histórico
git log --oneline
```

### Workflow Recomendado

```cmd
# Verificar branch atual
git branch

# Criar nova branch para feature
git checkout -b feature/nova-funcionalidade

# Trabalhar no código...
# Adicionar e comitar mudanças
git add .
git commit -m "Adiciona nova funcionalidade"

# Voltar para main e fazer merge
git checkout main
git merge feature/nova-funcionalidade

# Enviar mudanças
git push origin main
```

## 🚀 Setup Completo - Passo a Passo

```cmd
# 1. Clonar ou criar diretório
cd c:\Projetos
mkdir wine_ia
cd wine_ia

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar ambiente
.\.venv\Scripts\activate.bat

# 4. Instalar dependências básicas
pip install pandas numpy matplotlib scikit-learn jupyter

# 5. Gerar requirements.txt
pip freeze > requirements.txt

# 6. Inicializar Git
git init

# 7. Criar .gitignore (ver conteúdo acima)

# 8. Primeiro commit
git add .
git commit -m "Initial setup: ambiente virtual e dependências"

# 9. Conectar com repositório remoto (opcional)
git remote add origin https://github.com/usuario/wine_ia.git
git push -u origin main
```

## 📁 Estrutura de Projeto Recomendada

```
wine_ia/
├── .venv/                   # Ambiente virtual (não versionado)
├── data/                   # Datasets (não versionado)
├── notebooks/              # Jupyter notebooks
├── src/                    # Código fonte
│   ├── __init__.py
│   ├── data_processing.py
│   ├── models.py
│   └── utils.py
├── tests/                  # Testes unitários
├── requirements.txt        # Dependências
├── .gitignore             # Arquivos ignorados pelo Git
├── README.md              # Este arquivo
└── main.py                # Script principal
```

## 🔄 Comandos Úteis do Dia a Dia

```cmd
# Ativar ambiente e abrir VS Code
.\.venv\Scripts\activate.bat && code .

# Verificar status do Git e ambiente
git status
python --version

# Instalar nova dependência e atualizar requirements
pip install nova-biblioteca
pip freeze > requirements.txt

# Commit rápido
git add . && git commit -m "Mensagem do commit"
```

## ❓ Troubleshooting

### Problema: PowerShell não executa scripts
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema: Git não reconhece mudanças
```cmd
git config --global core.autocrlf true
```

### Problema: VS Code não encontra o interpretador
1. `Ctrl+Shift+P`
2. `Python: Select Interpreter`
3. Selecionar `./.venv/Scripts/python.exe`

---

**Desenvolvido para o projeto Wine IA** 🍷🤖
