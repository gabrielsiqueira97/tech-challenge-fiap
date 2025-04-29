from pydantic import BaseModel

class ProducaoUva(BaseModel):
    produto_principal: str
    subproduto: str
    quantidade: int | None
    ano: int

class ProcessamentoUva(BaseModel):
    tipo_de_uva: str
    grupo_de_uva: str
    nm_uva: str
    ano: int
    quantidade_kg: int 

class ComercializacaoProduto(BaseModel):
    produto_principal: str
    subproduto: str
    quantidade: int
    ano: int

class ExportacaoProduto(BaseModel):
    pais: str
    quantidade_kg: int
    valor_usd: float
    ano: int

class ImportacaoProduto(BaseModel):
    pais: str
    quantidade_kg: int
    valor_usd: float
    ano: int

class Usuario(BaseModel):
    nome_usuario: str
    senha_hash: str

class TokenJWT(BaseModel):
    access_token: str
    token_type: str = "bearer"
