from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from commons import NameSpaces as ns
from controller import datasource_controller, global_controller
router = APIRouter()

TAG = "Global" 

@router.get("/classes/{classRDF}/resources/{page}", tags=[TAG])
async def read_resources(classRDF:str, page:int):
    try:
        response = global_controller.find_resources(classRDF, page)
        return response
    except Exception as err:
        return err

@router.get("/properties/{uri}", tags=[TAG])
async def get_properties(uri:str):
    """
    Obtém as propriedades de um recurso.
    """
    try:
        response = global_controller.find_properties(uri)
        return response
    except Exception as err:
        return err
    


