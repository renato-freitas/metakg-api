from typing import Union
from .resource_model import ResourceModel
from .exported_view_model import ExportedViewModel
from pydantic import BaseModel


class MetaMashupModel(ResourceModel):
  hasMashupView: Union[str, None] = None     
  hasExportedView: Union[str, None] = None  # devia ser uma lista de EV   
  hasFusionKG: Union[str, None] = None     
  

class AddExporteViewsModel(BaseModel):
  exportedViewCheckeds: list = []


class AddSparqlQueryParamsModel(ResourceModel):
  exportedViewURI: str
  localOntologyClass: str
  sqpCol: str
  

  