from typing import Union
from .resource import ResourceModel

class MappingModel(ResourceModel):
    description: Union[str, None] = None # mapeamento da rfb
    file_path: str
