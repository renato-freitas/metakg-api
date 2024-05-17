from typing import Union
from pydantic import BaseModel

class QueryModel(BaseModel):
  name: str
  body: str 
  shared: bool  
  owner: Union[str, None] = None  
  repository: Union[str, None] = None  
  