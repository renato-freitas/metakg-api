from typing import Union
from .resource_model import ResourceModel
from .exported_view_model import ExportedViewModel
from pydantic import BaseModel


class MetaMashupModel(ResourceModel):     
  hasExportedView: Union[str, None] = None  # devia ser uma lista de EV   
  fusionClass: Union[str, None] = None     
  propertyClass: Union[str, None] = None     
  

class AddExporteViewsModel(BaseModel):
  exportedViewCheckeds: list = []


class AddSparqlQueryParamsModel(ResourceModel):
  exportedViewURI: str
  localOntologyClass: str
  sqpCol: str
  

  