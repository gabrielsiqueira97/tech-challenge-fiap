from pydantic import BaseModel

class ProducaoUva(BaseModel):
    produto_principal: str
    subproduto: str
    quantidade: int | None
    ano: int

from pydantic import BaseModel

class ProcessamentoUva(BaseModel):
    tipo_de_uva: str
    grupo_de_uva: str
    nm_uva: str
    ano: int
    quantidade_kg: int 

class Usuario(BaseModel):
    nome_usuario: str
    senha_hash: str

class TokenJWT(BaseModel):
    access_token: str
    token_type: str = "bearer"
