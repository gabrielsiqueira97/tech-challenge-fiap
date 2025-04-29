from fastapi import APIRouter, Query, Depends, HTTPException, status
from app.services import consultar_producao_por_ano, consultar_processamento_uva,get_comercializacao, get_exportacao, get_importacao
from app.auth import gerar_hash_senha, obter_conexao_banco, criar_token_jwt, verificar_token_jwt
from app.models import Usuario, TokenJWT
 


router = APIRouter()
    
@router.post("/cadastro_usuario")
def cadastrar_usuario(usuario: Usuario):
    """Cadastra um novo usuário no banco"""
    conn = obter_conexao_banco()
    cursor = conn.cursor()

    # Verifica se o usuário já existe
    cursor.execute("SELECT id FROM usuarios WHERE nome_usuario = ?", (usuario.nome_usuario,))
    if cursor.fetchone():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário já existe!")

    # Insere o novo usuário com a senha hash
    cursor.execute("INSERT INTO usuarios (nome_usuario, senha_hash) VALUES (?, ?)",
                   (usuario.nome_usuario, gerar_hash_senha(usuario.senha_hash)))  # Ajustado para senha
    conn.commit()
    conn.close()

    return {"mensagem": f"Usuário '{usuario.nome_usuario}' cadastrado com sucesso!"}

@router.post("/login", response_model=TokenJWT)
def login(usuario: Usuario):
    """Autentica usuário e retorna um token JWT"""
    conn = obter_conexao_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE nome_usuario = ? AND senha_hash = ?", 
                   (usuario.nome_usuario, gerar_hash_senha(usuario.senha_hash)))

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos!")

    token = criar_token_jwt({"sub": usuario.nome_usuario})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/producao_uvas/{ano}")
def get_producao_por_ano(ano: int, usuario: str = Depends(verificar_token_jwt)):
    """Retorna a produção de um determinado ano (Apenas com autenticação JWT)"""
    produtos = consultar_producao_por_ano(ano)
    return {"usuario": usuario, "ano": ano, "produtos": produtos}

@router.get("/processamento_uvas")
def get_processamento_uvas(
    tipo_de_uva: str = Query(None, description="Tipo de uva (Viníferas, Americanas, etc.)"),
    grupo_de_uva: str = Query(None, description="Grupo de uva (TINTAS, BRANCAS...)"),
    nm_uva: str = Query(None, description="Nome da uva"),
    ano: int = Query(None, description="Ano de processamento"),
    usuario: str = Depends(verificar_token_jwt)  # Exige autenticação JWT
):
    """Retorna dados de processamento filtrados (Apenas com autenticação JWT)"""
    dados = consultar_processamento_uva(tipo_de_uva, grupo_de_uva, nm_uva, ano)
    return {"usuario": usuario, "total": len(dados), "dados": dados}

@router.get("/comercializacao/{ano}")
def get_comercializacao_por_ano(
    ano: int, 
    usuario: str = Depends(verificar_token_jwt),
    produto_principal: str = Query(None, description="Filtrar por produto principal"),
    subproduto: str = Query(None, description="Filtrar por subproduto")
):
    """Retorna dados de comercialização filtrados por ano, produto principal e subproduto (Apenas com autenticação JWT)"""
    produtos = get_comercializacao(produto_principal, subproduto, ano)
    return {"usuario": usuario, "ano": ano, "produto_principal": produto_principal, "subproduto": subproduto, "produtos": produtos}

@router.get("/exportacao/{ano}")
def get_exportacao_por_ano(
    ano: int, 
    usuario: str = Depends(verificar_token_jwt),
    pais: str = Query(None, description="Filtrar por país")
):
    """Retorna dados de exportação filtrados por ano e país (Apenas com autenticação JWT)"""
    produtos = get_exportacao(pais, ano)
    return {"usuario": usuario, "ano": ano, "pais": pais, "produtos": produtos}

@router.get("/importacao/{ano}")
def get_importacao_por_ano(
    ano: int, 
    usuario: str = Depends(verificar_token_jwt),
    pais: str = Query(None, description="Filtrar por país")
):
    """Retorna dados de importação filtrados por ano e país (Apenas com autenticação JWT)"""
    produtos = get_importacao(pais, ano)
    return {"usuario": usuario, "ano": ano, "pais": pais, "produtos": produtos}
