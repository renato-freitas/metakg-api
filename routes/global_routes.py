from fastapi import APIRouter
from typing import Union
from model.datasource_model import DataSourceModel
from commons import NameSpaces as ns
from controller import datasource_controller, global_controller
router = APIRouter()

TAG = "Global" 

@router.get("/resources/", tags=[TAG])
async def retrieve_resources(classURI:str, page:int, rowPerPage:int, label:str):
    try:
        response = global_controller.retrieve_resources(classURI, page, rowPerPage, label)
        return response
    except Exception as err:
        return err
    

@router.get("/resources/count/", tags=[TAG])
async def retrieve_resources(classURI:str):
    try:
        response = global_controller.get_quantity_of_all_resources(classURI)
        return response
    except Exception as err:
        return err



@router.get("/resources/{uri}", tags=[TAG])
async def retrieve_one_resource(uri:str):
    """Usado quando clica em um owl:ObjectProperty que é só uma URI com o objetivo de retornar o recurso."""
    try:
        print('***')
        response = global_controller.retrieve_one_resource(uri)
        return response
    except Exception as err:
        return err
    

@router.get("/links/", tags=[TAG])
async def retrieve_sameas(sameas:str):
    """"""
    try:
        response = global_controller.retrieve_sameAs(sameas)
        return response
    except Exception as err:
        return err
    



@router.get("/properties/", tags=[TAG])
async def retrieve_properties(resourceURI:str):
    """Obtém as propriedades de um recurso."""
    try:
        response = global_controller.retrieve_properties_from_exported_view(resourceURI)
        return response
    except Exception as err:
        return err



# @router.get("/properties/{uri}/{expand_sameas}", tags=[TAG])
# async def get_properties(uri:str, expand_sameas:bool):
#     """
#     Obtém as propriedades de um recurso.
#     """
#     try:
#         print('OBTEM PROPRIEDADES DE UM RECURSO SELECIONADO', expand_sameas, type(expand_sameas))
#         response = global_controller.find_properties(uri, expand_sameas)
#         return response
#     except Exception as err:
#         print(err)
#         return err
    


