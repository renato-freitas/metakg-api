from typing import Union
from .resource_model import ResourceModel
# from .datasource_model import DataSourceModel

class ExportedViewModel(ResourceModel):
    description: Union[str, None] = None
    hasDataSource: str #uri
    hasMappings: str #uri
    hasLocalOntology: str #uri

