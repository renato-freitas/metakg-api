from fastapi import APIRouter, Request
from controller import llm_controller
from commons import TEXTS
router = APIRouter()

TAG = "LLM" 

# https://www.youtube.com/watch?v=6ExFTPcJJFs
# https://www.youtube.com/watch?v=Arf7UwWjGyc
# pip install pydantic==1.10.17

@router.get("/llm/", tags=[TAG])
async def make_question(question:str, req: Request):
    """"""
    repo = req.headers.get('repo')
    result = llm_controller.make_question(repo, question)
    return result




