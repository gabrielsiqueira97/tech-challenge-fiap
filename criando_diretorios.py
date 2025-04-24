import os

# Defina a raiz do projeto
base_path = r"C:\Users\Gabriel\Desktop\FIAP\Tech Challeng FIAP\projeto_api_embrapa"

# Lista de diretórios
folders = [
    "app",
    "config",
    "docs",
    "tests",
    "data",
    "scripts"
]

# Lista de arquivos
files = [
    "app/__init__.py",
    "app/routes.py",
    "app/models.py",
    "app/services.py",
    "config/settings.py",
    "docs/README.md",
    "docs/api_documentation.md",
    "tests/test_routes.py",
    "scripts/data_extraction.py",
    "requirements.txt",
    ".env",
    "main.py"
]

# Criar diretórios
for folder in folders:
    os.makedirs(os.path.join(base_path, folder), exist_ok=True)

# Criar arquivos vazios
for file in files:
    open(os.path.join(base_path, file), 'a').close()

print("Estrutura de diretórios e arquivos criada com sucesso em:", base_path)