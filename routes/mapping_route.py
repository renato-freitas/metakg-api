from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from model.mapping_model import MappingModel
from commons import NameSpaces as ns
from controller import mapping_controller

router = APIRouter()
TAG = "Mappings" 
ROTA = "/mappings"


@router.get(ROTA, tags=[TAG])
async def read_mappings():
    response = mapping_controller.read_resources()
    return response



@router.post(ROTA, tags=[TAG])
async def create_mapping(data: MappingModel):
    """
    Cria um recurso de mapeamento R2ML do tipo vskg:Mappings.
    """
    try:
        response = mapping_controller.create(data)
        return response
    except Exception as err:
        return err


# @router.put(ROTA + "{uri}", tags=[TAG])
# async def update_data_source(uri:str, data: DataSourceModel):
#     """
#     Atualiza um recurso fonte de dados do tipo drm:DataAsset.
#     """
#     try:
#         print('><-><', uri)
#         response = datasource_controller.update(uri, data)
#         return response
#     except Exception as err:
#         return err


