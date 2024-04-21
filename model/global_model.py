from typing import Union
from pydantic import BaseModel

class ResoucesSameAsModel(BaseModel):
  resources: Union[dict, None] = None 
    