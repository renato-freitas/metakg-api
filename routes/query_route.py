from fastapi import APIRouter, Request
from model.global_model import ResoucesSameAsModel
from model.query_model import QueryModel
from controller import query_controller
router = APIRouter()

TAG = "Consultas Salvas" 

@router.post("/queries/", tags=[TAG])
async def create_queries(data: QueryModel, req:Request):
    try:
        repo = req.headers.get('repo')
        response = query_controller.create_queries(data, repo)
        return response
    except Exception as err:
        return err
    

@router.get("/queries/", tags=[TAG])
async def retrieve_queries(req:Request):
    try:
        repo = req.headers.get('repo')
        response = query_controller.retrieve_queries(repo)
        return response
    except Exception as err:
        return err
 

@router.put("/queries/", tags=[TAG])
async def update_saved_query(data: QueryModel, req:Request):
    try:
        repo = req.headers.get('repo')
        response = query_controller.update_saved_query(data, repo)
        return response
    except Exception as err:
        return err




@router.delete("/queries/", tags=[TAG])
async def delete_saved_query(name:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = query_controller.delete_saved_query(name, repo)
        return response
    except Exception as err:
        return err