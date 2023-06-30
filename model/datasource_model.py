from typing import Union
from .resource import ResourceModel

class DataSourceModel(ResourceModel):
    name: str                            # exemplo de nomes: Arduino_001
    description: Union[str, None] = None # para ler temperaturas dos ar-cond
    subject_datasource: str              # Temperatura
    type: str                            # csv, xml, tsv, BDR
    url_or_path: Union[str, None] = None
    user: Union[str, None] = None
    password: Union[str, None] = None
    jdbc: Union[str, None] = None