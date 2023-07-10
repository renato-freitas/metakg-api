from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from model.meta_mashup_model import MetaMashupModel
from commons import NameSpaces as ns
from controller import datasource_controller, meta_ekg_controller
router = APIRouter()

TAG = "Meta EKG" 
ROTA = "/meta-ekgs/"


@router.get(ROTA, tags=[TAG])
async def read_meta_ekgs():
    response = meta_ekg_controller.read_resources()
    print('{**}', response)
    return response


@router.get(ROTA + "{uri}/mashupClass/{mashupClass}", tags=[TAG])
async def sugest_exported_views(uri:str, mashupClass:str):
    print('[1]', uri)
    print('[2]', mashupClass)
    response = meta_ekg_controller.sugest_exported_views(uri, mashupClass)
    return response

# @router.post(ROTA, tags=[TAG])
# async def create_meta_mashup(data: MetaMashupModel):
#     try:
#         response = meta_mashup_controller.create(data)
#         return response
#     except Exception as err:
#         return err


# @router.get(ROTA + "exported-view/mat/" + "{uri}", tags=[TAG])
# async def read_meta_mashup(uri:str):
#     response = meta_mashup_controller.materialize_exported_view(uri)
#     return response




# @router.post(ROTA + "reuse-meta-ekg", tags=[TAG])
# async def associate_metaekg(data:MetaMashupModel):
#     try:
#         response = meta_mashup_controller.update(data)
#         return response
#     except Exception as err:
#         return err

# @router.put(ROTA + "{uri}", tags=[TAG])
# async def update_meta_mashup(uri:str, data: MetaMashupModel):
#     """
#     Atualiza um recurso vskg:MetadataGraphMashup.
#     A classe do mashup só pode ser alterada se não tiver visões exportadas selecionadas.
#     """
#     try:
#         response = meta_mashup_controller.update(uri, data)
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
