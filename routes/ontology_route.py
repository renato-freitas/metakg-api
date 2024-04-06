from fastapi import APIRouter
from controller import ontology_controller
from commons import TEXTS
router = APIRouter()

TAG = "Classes" 

@router.get("/classes/", tags=[TAG])
async def retrieve_classes(type:str):
    """"""
    if(type == TEXTS.GENERALIZATION):
        result = ontology_controller.retrieve_generalization_classes()
    else: 
        result = ontology_controller.retrieve_semantic_view_exported_classes()
    return result


