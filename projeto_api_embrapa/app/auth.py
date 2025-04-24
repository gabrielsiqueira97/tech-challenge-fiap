from fastapi import HTTPException, status
import jwt
import datetime
import sqlite3
import hashlib

# Configuração JWT
JWT_SECRET_KEY = "xyz123"  # Sua chave secreta
JWT_ALGORITHM = "HS256"

# Função para gerar hash da senha
def gerar_hash_senha(senha: str) -> str:
    """Gera um hash SHA256 para armazenar a senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para conectar ao banco SQLite
def obter_conexao_banco():
    """Conectar ao banco SQLite"""
    conn = sqlite3.connect("data/database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar token JWT
def criar_token_jwt(dados: dict):
    """Gera um token JWT válido por 1 hora"""
    expiracao = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    dados.update({"exp": expiracao})
    return jwt.encode(dados, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# Função para verificar token JWT
def verificar_token_jwt(token: str):
    """Valida token JWT e retorna o nome de usuário"""
    try:
        dados = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return dados.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado!")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido!")