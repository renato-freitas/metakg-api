from fastapi import APIRouter
from controller import ontology_controller
from commons import TEXTS
router = APIRouter()

TAG = "Classes" 

@router.get("/classes/", tags=[TAG])
async def retrieve_classes(type:str, repo:str):
    """"""
    print('*** CLASSES/REPO:', repo)
    if(type == TEXTS.GENERALIZATION):
        result = ontology_controller.retrieve_generalization_classes(repo)
    elif (type == TEXTS.EXPORTED): 
        result = ontology_controller.retrieve_semantic_view_exported_classes(repo)
    else:
        result = ontology_controller.retrieve_metadata_classes(repo)
    return result


