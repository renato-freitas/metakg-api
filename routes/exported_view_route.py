import platform
import os
from fastapi import APIRouter, Request
from model.datasource_model import DataSourceModel
from model.exported_view_model import ExportedViewModel
from commons import NameSpaces as ns, Ontology as o
from controller import exported_view_controller
router = APIRouter()

TAG = "Exported View" 
ROTA = "/exportedviews"


@router.get(ROTA, tags=[TAG])
async def read_exported_views():
    """Lista todas as Visões Exportadas do tipo vskg:LocalGraph."""
    response = exported_view_controller.read_resources()
    return response


@router.post(ROTA, tags=[TAG])
async def create_exported_view(data: ExportedViewModel):
    """
    Cria um recurso visão exportada do tipo vskg:LocalGraph.
    """
    try:
        response = exported_view_controller.create(data)
        return response
    except Exception as err:
        return err


@router.put(ROTA + "{uri}", tags=[TAG])
async def update_exported_view(uri:str, data: ExportedViewModel):
    """
    Cria um recurso visão exportada do tipo vskg:LocalGraph.
    """
    try:
        response = exported_view_controller.update(uri, data)
        return response
    except Exception as err:
        return err


# https://janakiev.com/blog/python-shell-commands/
@router.get(ROTA + "triplify/" + "{uri}", tags=[TAG])
async def run_triplification(uri):
    """Materializa uma fonte de dados de acordo com as regras de mapeamentos."""
    try:
        exported_view_controller.materialize(uri)
    except Exception as err:
        return err
