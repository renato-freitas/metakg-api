from typing import Union
from .resource_model import ResourceModel

class DataSourceModel(ResourceModel):
    label: str 
    description: Union[str, None] = None 
    subject_datasource: Union[str, None] = None  
    type: str  
    connection_url: Union[str, None] = None # exemplo: jdbc:postgresql://ip:porta/nome_bd
    username: Union[str, None] = None
    password: Union[str, None] = None
    jdbc_driver: Union[str, None] = None # org.postgresql.Driver
    csv_file: Union[str, None] = None