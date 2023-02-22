from typing import Union, Sequence
from pydantic import BaseModel

class DataSource(BaseModel):
    identifier: Union[str, None] = None
    label: str
    description: Union[str, None] = None
    subject_datasource: str
    type: str #csv, xml, tsv, BDR
    url_or_path: Union[str, None] = None
    user: Union[str, None] = None
    password: Union[str, None] = None
    jdbc: Union[str, None] = None


# dic_property = json[
#     dict[str, str],
#     dict[str, Sequence[str]],
#     dict[str, str]
# ]

class DataProperty(BaseModel):
    nome: str
    propriedades: Sequence[str]
    tipo: str

class ObjectProperty(BaseModel):
    nome: str
    propriedades: Sequence[str]
    uri: str

class HighLevelMapping(BaseModel):
    table_or_file_name: str
    uri: str
    keys: Sequence[str]
    types: Sequence[str]
    data_properties: Sequence[DataProperty]
    object_properties: Sequence[ObjectProperty]