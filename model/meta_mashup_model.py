from typing import Union
from .resource_model import ResourceModel
from .exported_view_model import ExportedViewModel
from pydantic import BaseModel


class MetaMashupModel(ResourceModel):
  mashupClass: str                          # Deveria ser uma classe da ontologia
  hasMashupView: Union[str, None] = None  
  reuse_metaekg: Union[str, None] = None    # range: vskg:MetadataGraphEKG     
  hasExportedView: Union[str, None] = None  # devia ser uma lista de EV   
  
class AddExporteViewsModel(BaseModel):
  exportedViewCheckeds: list = []
  

  