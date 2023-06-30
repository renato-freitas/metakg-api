from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from commons import NameSpaces as ns
from controller import datasource_controller

router = APIRouter()
TAG = "datasources" 
ROTA = f'/{TAG}/'
PADRAO_URI = f'{ns.VSKGR}DataSource'

# Para cria qualquer recurso deve ter uma única função que recebe a URI do recurso com os dados e a classe.
# :fd_001, drm:DataAsset

@router.get(ROTA, tags=[TAG])
async def read_data_sources():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get(ROTA+"me", tags=[TAG])
async def read_data_source():
    return {"username": "fakecurrentuser"}


@router.get(ROTA+"{username}", tags=[TAG])
async def read_user(username: str):
    return {"username": username}


@router.post(ROTA, tags=[TAG])
async def create_data_source(data: DataSourceModel):
    """Propriedade da Fonte de dados:
    nome, tipo de conexão (Mysql, Postgres,), nome_host, nome_banco_dados, num_porta, nome_usuario, senha
    No Pentaho existem as Conexões que podem ser globais. 
    No MetaEKG teremos as FD.
    """
    # chamar o controller
    response = datasource_controller.create(data)
    return response
