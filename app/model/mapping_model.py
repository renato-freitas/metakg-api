from typing import Union
from .resource_model import ResourceModel

class MappingModel(ResourceModel):
    description: Union[str, None] = None # mapeamento da rfb
    prefixies: str
    # file_path: str
    # o nome do arquivo rml é o label da visão exportada, por ser única ao usar o prefixo "ev (exported view)"
