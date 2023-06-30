from typing import Union, Sequence
from pydantic import BaseModel

class ResourceModel(BaseModel):
  identifier: Union[str, None] = None
  label: str
