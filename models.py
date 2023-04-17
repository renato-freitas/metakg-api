from typing import Union, Sequence
from pydantic import BaseModel


class DataSource(BaseModel):
    identifier: Union[str, None] = None
    label: str
    description: Union[str, None] = None
    subject_datasource: str
    type: str  # csv, xml, tsv, BDR
    url_or_path: Union[str, None] = None
    user: Union[str, None] = None
    password: Union[str, None] = None
    jdbc: Union[str, None] = None


class MetaMashupModel(BaseModel):
    """<App> tem_KG <Meta-Mashup> Metadados das Aplicações (KG especializados = Data Mashup) """
    # uri_camada_app: Union[str, None] = None
    # app_name: Union[str, None] = None
    # app_description: Union[str, None] = None
    # prefix: Union[str, None] = None # é pra vir do meta-ekg
    # namespace_base: Union[str, None] = None # é pra vir do meta-ekg
    label: str
    identifier: Union[str, None] = None

class AssociaMetaMashupMOdel(BaseModel):
    """Diz qual KG de metadado é usado pelo Meta Masup"""
    uri_meta_mashup: str
    uri_meta_ekg: str

class AddGCLMashupModel(BaseModel):
    uri_visao_semantica_mashup: str
    uri_gcl: str
    label_gcl: str

# dic_property = json[
#     dict[str, str],
#     dict[str, Sequence[str]],
#     dict[str, str]
# ]

# META-EKG hasApplicationsMetadata

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
