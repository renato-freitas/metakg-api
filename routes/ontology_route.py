from fastapi import APIRouter
from controller import ontology_controller
router = APIRouter()

TAG = "Classes" 

@router.get("/classes/", tags=[TAG])
async def read_classes():
    response = ontology_controller.find_classes()
    return response


