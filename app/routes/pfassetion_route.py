from fastapi import APIRouter, Request
from model.global_model import ResoucesSameAsModel, CompetenceQuestionModel, PropertyFunctionAssertionModel
from model.query_model import SavedQueryModel, SavedQueryModel
from controller import pfassertion_controller
router = APIRouter()

TAG = "Questão de Competência" 
BASE = "/property-funsion-assertion/"

@router.post(BASE, tags=[TAG])
async def create_pfa(data:PropertyFunctionAssertionModel , req:Request):
    try:
        repo = req.headers.get('repo')
        response = pfassertion_controller.create_pfa(data, repo)
        return response
    except Exception as err:
        return err


@router.get(BASE, tags=[TAG])
async def retrieve_saved_queries(classGen:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = pfassertion_controller.retrieve_pfa_by_class(classGen, repo)
        print(response)
        functions = ""
        for item in response:
            if "def" not in item["function"]["value"]: pass
            else: functions += item["function"]["value"] + "\n"
        print("------functions----\n", functions)
        # with open(f'pfa/temp.py', 'w', encoding="utf-8") as file:
        #     file.write(functions)
        return response
    except Exception as err:
        return err
 

@router.get("/competence-questions/execute", tags=[TAG])
async def execute_competence_question(uri:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = pfassertion_controller.execute_competence_question(uri, repo)
        return response
    except Exception as err:
        return err
