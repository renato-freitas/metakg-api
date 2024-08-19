from fastapi import APIRouter, Request
from controller import ontology_controller
from commons import TEXTS
router = APIRouter()

TAG = "Classes" 

# ESSA FERRAMENTA SEMPRE ESPERA UM LABEL COM IDIOMA @en ou @pt PARA OS TERMOS DA ONTOLOGIA.
# CASO NÃO TENHA RDFS:LABEL É EXIBIDO A URI DO TERMO

@router.get("/classes/", tags=[TAG])
async def retrieve_classes(view:str, exported_view:str, language:str, req: Request):
    """"""
    print('\n---routes:_retrieve_classes---')
    repo = req.headers.get('repo')
    print(f'+ repositório: {repo}')
    print(f'+ tipo de visão de contexto: {view}')

    if (view in [TEXTS.CODE_OF_UNIFICATION_VIEW, TEXTS.CODE_OF_FUSION_VIEW]):
        result = ontology_controller.retrieve_generalization_classes(repo, language)
    elif (view == TEXTS.CODE_OF_EXPORTED_VIEW): 
        result = ontology_controller.retrieve_exported_semantic_view_classes(repo, exported_view, language)
    return result

# ESSA FERRAMENTA ESPER

@router.get("/classes/exported-views", tags=[TAG])
async def retrieve_exported_views(req: Request):
    """Rota utilizada para recuperar as visões semânticas exportadas"""
    print('\n---routes:_retrieve_exported_views---')
    repo = req.headers.get('repo')
    print('+ repo:', repo)
    result = ontology_controller.retrieve_semantic_view_exported_datasources(repo)
    return result

