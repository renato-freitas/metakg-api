from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from commons import NameSpaces as ns
from controller import datasource_controller, meta_mashup_controller
router = APIRouter()

TAG = "Meta Mashup" 
ROTA = "/meta-mashups/"


@router.get(ROTA + "{uri}", tags=[TAG])
async def read_meta_mashups(uri:str):
    response = meta_mashup_controller.materialize_exported_view(uri)
    return response


# @router.post(ROTA, tags=[TAG])
# async def create_data_source(data: DataSourceModel):
#     """
#     Cria um recurso fonte de dados do tipo drm:DataAsset.

#     Propriedades da Fonte de dados:
#     nome, tipo de conexão (Mysql, Postgres,), nome_host, nome_banco_dados, num_porta, nome_usuario, senha
#     No Pentaho existem as Conexões que podem ser globais. 
#     No MetaEKG teremos as FD.
#     """
#     # chamar o controller
#     try:
#         response = datasource_controller.create(data)
#         return response
#     except Exception as err:
#         print('err',err)
#         return err


# @router.put(ROTA + "{uri}", tags=[TAG])
# async def update_data_source(uri:str, data: DataSourceModel):
#     """
#     Atualiza um recurso fonte de dados do tipo drm:DataAsset.
#     """
#     try:
#         response = datasource_controller.update(uri, data)
#         return response
#     except Exception as err:
#         return err

# @router.delete(ROTA + "{uri}", tags=[TAG])
# async def delete_data_source(uri:str):
#     """
#     Apaga um recurso fonte de dados do tipo drm:DataAsset.
#     """
#     try:
#         response = datasource_controller.delete(uri)
#         return response
#     except Exception as err:
#         return err
