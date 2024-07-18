from fastapi import APIRouter, Request
from model.global_model import ResoucesSameAsModel
from model.query_model import SavedQueryModel, SavedQueryModel
from controller import query_controller
router = APIRouter()

TAG = "Consultas Salvas" 

@router.post("/queries/", tags=[TAG])
async def create_saved_query(data:SavedQueryModel , req:Request):
    try:
        repo = req.headers.get('repo')
        response = query_controller.create_saved_query(data, repo)
        return response
    except Exception as err:
        return err


@router.get("/queries/", tags=[TAG])
async def retrieve_saved_queries(req:Request):
    try:
        repo = req.headers.get('repo')
        response = query_controller.retrieve_queries(repo)
        return response
    except Exception as err:
        return err
 

@router.get("/queries/execute", tags=[TAG])
async def execute_saved_queries(uri:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = query_controller.execute_saved_query(uri, repo)
        return response
    except Exception as err:
        return err

@router.put("/queries/", tags=[TAG])
async def update_one_saved_query(uri:str, data: SavedQueryModel, req:Request):
    """Atualiza um recurso do tipo sq:SavedQuery."""
    try:
        repo = req.headers.get('repo')
        response = query_controller.update(uri, data, repo)
        return response
    except Exception as err:
        return err


@router.delete("/queries/", tags=[TAG])
async def delete_one_saved_query(uri:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = query_controller.delete_one_saved_query(uri, repo)
        return response
    except Exception as err:
        return err
    



# =========================================================
# async def create_query(data: QueryModel, req:Request):
#     try:
#         repo = req.headers.get('repo')
#         response = query_controller.create_query(data, repo)
#         return response
#     except Exception as err:
#         return err
    


# @router.put("/queries/", tags=[TAG])
# async def update_saved_query(data: QueryModel, req:Request):
#     try:
#         repo = req.headers.get('repo')
#         response = query_controller.update_saved_query(data, repo)
#         return response
#     except Exception as err:
#         return err
