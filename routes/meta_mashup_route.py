from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from model.meta_mashup_model import MetaMashupModel, AddExporteViewsModel, AddSparqlQueryParamsModel
from commons import NameSpaces as ns
from controller import datasource_controller, meta_mashup_controller
router = APIRouter()

TAG = "Meta Mashup" 
# ROTA = "/meta-mashups/"

@router.post("/meta-mashups/", tags=[TAG])
async def create_meta_mashup(data: MetaMashupModel):
    """Instanciar o Grafo com os metadados do Mashup de Dados Especializado."""
    try:
        response = meta_mashup_controller.create(data)
        return response
    except Exception as err:
        return err


@router.get("/meta-mashups/", tags=[TAG])
async def read_meta_mashups():
    response = meta_mashup_controller.read_resources()
    return response


@router.get("/meta-mashups/exported-view/mat/{uri}", tags=[TAG])
async def read_meta_mashup(uri:str):
    response = meta_mashup_controller.materialize_exported_view(uri)
    return response


@router.put("/meta-mashups/{uri}", tags=[TAG])
async def update_meta_mashup(uri:str, data: MetaMashupModel):
    """
    Atualiza um recurso vskg:MetadataGraphMashup.
    A vskg:fusionClass só pode ser alterada se não tiver visões exportadas selecionadas. (ainda não foi implementado)
    """
    try:
        response = meta_mashup_controller.update(uri, data)
        return response
    except Exception as err:
        return err


# @router.post("/meta-mashups/reuse-meta-ekg", tags=[TAG])
# async def associate_metaekg(data:MetaMashupModel):
#     try:
#         response = meta_mashup_controller.update(data)
#         return response
#     except Exception as err:
#         return err



    

@router.delete("/meta-mashups/{uri}", tags=[TAG])
async def delete_meta_mashup(uri:str):
    """
    Apaga um recurso Meta-Mashup do tipo vskg:MetadataGraphMashup.
    """
    try:
        response = meta_mashup_controller.delete(uri)
        return response
    except Exception as err:
        return err
    
    
@router.put("/meta-mashups/{uri}/add-exported-views", tags=[TAG])
async def add_exported_views(uri:str, data: AddExporteViewsModel):
    """Adiciona as visões exportadas selecionadas do EKG para o MetaMashup."""
    try:
        print('ENTRADA:', data)
        response = meta_mashup_controller.add_exported_views(uri, data)
        return response
    except Exception as err:
        return err



    

@router.get("/meta-mashups/{uri}/sparql-query-params", tags=[TAG])
async def reade_sparql_params_to_reuse_mappings(uri:str):
    """
    uri: URI do MetaMashup
    """
    try:
        response = meta_mashup_controller.reade_sparql_params_to_reuse_mappings(uri)
        return response
    except Exception as err:
        return err


@router.put("/meta-mashups/{uri_meta_mashup}/sparql-query-params", tags=[TAG])
async def add_sparql_params_to_reuse_mappings(uri_meta_mashup:str, data: AddSparqlQueryParamsModel):
    """Adiciona os parametros a consulta SPARQL para reutilizar os metadados dos mapeamentos das
    visões exportadas.
    uri: URI do MetaMashup
    """
    try:
        print('ENTRADA:', data)
        response = meta_mashup_controller.add_sparql_params_to_reuse_mappings(uri_meta_mashup, data)
        return response
    except Exception as err:
        return err
# @router.delete(ROTA + "{uri}", tags=[TAG])
# async def delete_data_source(uri:str):
#     """
#     Apaga um recurso fonte de dados do tipo drm:DataAsset.
#     """
#     try:
#         response = datasource_controller.delete(uri)
#         return response
#     except Exception as err:
#         return err
