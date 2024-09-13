from fastapi import APIRouter, Request
from model.global_model import ResoucesSameAsModel, CompetenceQuestionModel
from model.query_model import SavedQueryModel, SavedQueryModel
from controller import competence_question_controller

router = APIRouter()
TAG = "Questão de Competência" 

@router.post("/competence-questions/", tags=[TAG])
async def create_competence_question(data:CompetenceQuestionModel , req:Request):
    try:
        repo = req.headers.get('repo')
        response = competence_question_controller.create_pfa(data, repo)
        return response
    except Exception as err:
        return err


@router.get("/competence-questions/", tags=[TAG])
async def retrieve_saved_queries(language:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = competence_question_controller.retrieve_competence_questions(language, repo)
        return response
    except Exception as err:
        return err
 

@router.get("/competence-questions/execute", tags=[TAG])
async def execute_competence_question(uri:str, language:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = competence_question_controller.execute_competence_question(uri, language, repo)
        return response
    except Exception as err:
        return err