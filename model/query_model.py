from typing import Union
from pydantic import BaseModel

# class SavedQueryModel(BaseModel):
#   name: str
#   descritpion: Union[str, None] = None   
#   repository: str
#   sparql: str 
  

class SavedQueryModel(BaseModel):
  identifier: Union[str, None] = None  
  name: str
  description: Union[str, None] = None   
  repository: str
  generalizationClass: Union[str, None] = None  
  sparql: str 