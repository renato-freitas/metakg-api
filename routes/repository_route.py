from fastapi import APIRouter
from controller import repository_controller
from commons import TEXTS
router = APIRouter()

TAG = "Repositórios" 

@router.get("/repositories/", tags=[TAG])
async def retrieve_repositories():
    """"""
    print('/reposito')
    result = repository_controller.retrieve_repostories()
    return result


