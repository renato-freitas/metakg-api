from fastapi import APIRouter, Request
from model.global_model import ResoucesSameAsModel
from controller import global_controller
router = APIRouter()

TAG = "Global" 

@router.get("/resources/", tags=[TAG])
async def retrieve_resources(classRDF:str, page:int, rowPerPage:int, label:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = global_controller.retrieve_resources(classRDF, page, rowPerPage, label, repo)
        return response
    except Exception as err:
        return err
    

@router.get("/resources/count/", tags=[TAG])
async def retrieve_quantity_resources(classURI:str, label:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = global_controller.get_quantity_of_all_resources(classURI, label, repo)
        return response
    except Exception as err:
        return err



@router.get("/resources/{uri}", tags=[TAG])
async def retrieve_one_resource(uri:str, req:Request):
    """Usado quando clica em um owl:ObjectProperty que é só uma URI com o objetivo de retornar o recurso."""
    try:
        print('***')
        repo = req.headers.get('repo')
        response = global_controller.retrieve_one_resource(uri, repo)
        return response
    except Exception as err:
        return err
    

@router.get("/links/", tags=[TAG])
async def retrieve_sameas_resources(sameas:str, req:Request):
    """Recuperas apenas recursos que tem ligação com o recurso de origem"""
    try:
        repo = req.headers.get('repo')
        response = global_controller.retrieve_sameAs_resources(sameas, repo)
        return response
    except Exception as err:
        return err
    



@router.get("/properties/", tags=[TAG])
async def retrieve_properties_of_one_resource(resourceURI:str, req:Request):
    """Obtém as propriedades de um recurso."""
    try:
        repo = req.headers.get('repo')
        response = global_controller.retrieve_properties_from_exported_view(resourceURI, repo)
        return response
    except Exception as err:
        return err



@router.post("/properties/unification/", tags=[TAG])
async def retrieve_properties_from_unification_of_resource(data: ResoucesSameAsModel, req:Request):
    """Obtém as propriedades unificadas dos recursos da lista."""
    try:
        repo = req.headers.get('repo')
        response = global_controller.retrieve_properties_from_unification_view(data, repo)
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
    


