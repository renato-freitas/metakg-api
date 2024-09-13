from fastapi import APIRouter, Request
from model.global_model import ResoucesSameAsModel, ResourcesSameAsModel, ListResourcesSameAsModel
from controller import global_controller
router = APIRouter()

TAG = "Global" 

@router.get("/resources/", tags=[TAG])
async def retrieve_resources(classRDF:str, page:int, rowPerPage:int, label:str, language:str, req:Request):
    try:
        print('\n---routes: retriever_resources---')
        repo = req.headers.get('repo')
        response = global_controller.retrieve_resources(classRDF, page, rowPerPage, label, language, repo)
        return response
    except Exception as err:
        return err


@router.get("/resources/exported-view", tags=[TAG])
async def retrieve_resources(classRDF:str, page:int, rowPerPage:int, label:str, language:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = global_controller.retrieve_resources(classRDF, page, rowPerPage, label, language, repo)
        return response
    except Exception as err:
        return err  


@router.get("/resources/generalization", tags=[TAG])
async def retrieve_resources(classRDF:str, page:int, rowPerPage:int, label:str, language:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = global_controller.retrieve_unification_resources(classRDF, page, rowPerPage, label, language, repo)
        return response
    except Exception as err:
        return err



@router.get("/resources/count/", tags=[TAG])
async def retrieve_quantity_resources(classURI:str, label:str, sameas: bool, language:str, req:Request):
    try:
        repo = req.headers.get('repo')
        response = global_controller.get_quantity_of_all_resources(classURI, label, sameas, language, repo)
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
    

@router.get("/sameas/", tags=[TAG])
async def retrieve_sameas_resources(resourceURI:str, req:Request):
    """Recuperas apenas recursos que tem ligação com o recurso de origem"""
    try:
        repo = req.headers.get('repo')
        response = global_controller.retrieve_sameAs_resources(resourceURI, repo)
        return response
    except Exception as err:
        return err
    



@router.get("/properties/", tags=[TAG])
async def retrieve_properties_of_one_resource(resourceURI:str, typeOfView:str, language:str, req:Request):
    """Obtém as propriedades de um recurso nos três contextos de visão"""
    eh_visao_unification = typeOfView == 0 or typeOfView == "0"
    eh_visao_exportada = typeOfView == 1 or typeOfView == "1"
    eh_visao_fusao = typeOfView == 2 or typeOfView == "2"
    try:
        print('\n--------route:retrieve_properties_of_one_resource------')
        repo = req.headers.get('repo')
        print('?tipo de visão:', typeOfView)
        if (eh_visao_unification):
            response = global_controller.retrieve_properties_at_unification_view(resourceURI, language, repo)
        elif (eh_visao_exportada):
            response = global_controller.retrieve_properties_at_exported_view(resourceURI, language, repo)
        else:
            response = global_controller.retrieve_properties_at_fusion_view(resourceURI, language, repo)
        return response
    except Exception as err:
        return err



@router.post("/properties/unification", tags=[TAG])
async def retrieve_properties_from_unification_of_resource(language:str, data: ListResourcesSameAsModel, req:Request):
    """Obtém as propriedades unificadas dos recursos da lista."""
    try:
        print('\n-routes: retrieve_properties_from_unification_of_resource-\n')
        print('+ resources:', data.resources)
        repo = req.headers.get('repo')
        response = global_controller.retrieve_properties_from_list_of_resources_to_unification_view(data, language, repo)
        return response
    except Exception as err:
        return err




@router.post("/properties/fusion/", tags=[TAG])
# async def retrieve_properties_from_unification_of_resource(data: ResoucesSameAsModel, req:Request):
async def retrieve_properties_from_fusion_of_resource(language:str, data: ListResourcesSameAsModel, req:Request):
    """Obtém a fusão das propriedades dos recursos."""
    try:
        print('\n---ROUTES: retrieve_properties_from_fusion_of_resource( )---\n')
        print('+ data:',data)
        repo = req.headers.get('repo')
        response = global_controller.retrieve_properties_from_list_of_resources_to_fusion_view(data, language, repo)
        return response
    except Exception as err:
        return err
    


@router.get("/timeline/", tags=[TAG])
async def retrieve_timeline_of_one_resource(resourceURI:str, owlProperty:str, req:Request):
    """Obtém a linha do tempo de um recurso."""
    try:
        repo = req.headers.get('repo')
        response = global_controller.retrieve_timeline_of_one_resource(resourceURI, owlProperty, repo)
        return response
    except Exception as err:
        return err
    


@router.post("/timeline/unification/", tags=[TAG])
async def retrieve_timeline_of_unification_resources(data: ListResourcesSameAsModel, owlProperty:str, req:Request):
    """Obtém a linha do tempo de um recurso."""
    try:
        repo = req.headers.get('repo')
        response = global_controller.retrieve_timeline_of_unification_resources(data, owlProperty, repo)
        return response
    except Exception as err:
        return err

