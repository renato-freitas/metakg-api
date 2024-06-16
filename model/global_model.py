from typing import Union
from pydantic import BaseModel

class ResoucesSameAsModel(BaseModel):
  resources: Union[dict, None] = None 
    
  
class ResourcesSameAsModel(BaseModel):
  resources: Union[list, None] = None  


class CompetenceQuestionModel(BaseModel):
  identifier: Union[str, None] = None  
  name: str
  description: Union[str, None] = None   
  repository: str
  sparql: str 


class PropertyFunctionAssertionModel(BaseModel):
  identifier: Union[str, None] = None  
  name: str
  generalizationClass: str
  rdfProperty: str
  function: str 
  description: Union[str, None] = None   
  repository: str