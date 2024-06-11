from typing import Union
from pydantic import BaseModel

class SavedQueryModel(BaseModel):
  name: str
  descritpion: Union[str, None] = None   
  repository: str
  sparql: str 
  

class SavedQueryFusionModel(BaseModel):
  identifier: str
  name: str
  description: Union[str, None] = None   
  repository: str
  generalizationClass: str
  sparql: str 