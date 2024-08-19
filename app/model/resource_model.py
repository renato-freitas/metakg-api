from typing import Union
# from pydantic import BaseModel
from pydantic import BaseModel


class ResourceModel(BaseModel):
  identifier: Union[str, None] = None
  uri: Union[str, None] = None
  label: str
  description: Union[str, None] = None
  comment: Union[str, None] = None
  creator: Union[str, None] = None # Algum agente criará um recurso
