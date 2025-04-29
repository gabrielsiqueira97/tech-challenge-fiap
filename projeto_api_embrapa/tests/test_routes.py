import pytest
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

# Variável global para armazenar o token JWT para os testes
TOKEN_JWT = None

def obter_e_validar_token():
    """Autentica o usuário 'Gabriel', salva o token JWT e valida se foi obtido corretamente."""
    global TOKEN_JWT
    response = client.post("/login", json={"nome_usuario": "Gabriel", "senha_hash": "123"})
    assert response.status_code == 200
    TOKEN_JWT = response.json()["access_token"]
    assert TOKEN_JWT is not None  # Garante que o token foi gerado corretamente

TOKEN_JWT_VAZIO = ""
@pytest.mark.parametrize("endpoint, params", [
    ("/producao_uvas/2023", {"ano": 2023, "token": TOKEN_JWT_VAZIO}),
    ("/processamento_uvas", {"tipo_de_uva": "Viníferas", "ano": 2023, "token": TOKEN_JWT_VAZIO}),
    ("/comercializacao/2023", {"produto_principal": "Vinho", "subproduto": "Tinto", "ano": 2023, "token": TOKEN_JWT_VAZIO}),
    ("/exportacao/2023", {"pais": "Argentina", "ano": 2023, "token": TOKEN_JWT_VAZIO}),
    ("/importacao/2023", {"pais": "Chile", "ano": 2023, "token": TOKEN_JWT_VAZIO})
])
def test_endpoints_sem_autenticacao(endpoint, params):
    """Testa múltiplos endpoints sem autenticação JWT e espera um erro 401"""
    response = client.get(endpoint, params=params)
    assert response.status_code == 401  # Se retornar 401, o teste passa


@pytest.mark.parametrize("endpoint, params", [
    ("/producao_uvas/2023", {}),
    ("/processamento_uvas", {"tipo_de_uva": "Viníferas", "ano": 2023}),
    ("/comercializacao/2023", {"produto_principal": "Vinho", "subproduto": "Tinto"}),
    ("/exportacao/2023", {"pais": "Argentina"}),
    ("/importacao/2023", {"pais": "Chile"})
])
def test_endpoints_com_autenticacao(endpoint, params):
    """Testa múltiplos endpoints com autenticação JWT via query parameter"""
    global TOKEN_JWT
    if TOKEN_JWT is None:
        obter_e_validar_token()

    params["token"] = TOKEN_JWT
    headers = {"Authorization": f"Bearer {TOKEN_JWT}"}
    response = client.get(endpoint, params=params, headers=headers)

    assert response.status_code == 200  
    assert "usuario" in response.json()  #Confirma que o usuário autenticado aparece na resposta