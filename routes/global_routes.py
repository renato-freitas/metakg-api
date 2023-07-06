from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from commons import NameSpaces as ns
from controller import datasource_controller, global_controller
router = APIRouter()

TAG = "Global" 
ROTA = "/properties/"

@router.get(ROTA + "{uri}", tags=[TAG])
async def get_properties(uri:str):
    """
    Obtém as propriedades de um recurso.
    """
    try:
        response = global_controller.get_properties(uri)
        return response
    except Exception as err:
        return err