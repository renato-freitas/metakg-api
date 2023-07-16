from typing import Union, Sequence
from pydantic import BaseModel

class ResourceModel(BaseModel):
  identifier: Union[str, None] = None
  uri: Union[str, None] = None
  label: str
  description: Union[str, None] = None
  creator: Union[str, None] = None # Algum agente criará um recurso
