from typing import Union
from .resource import ResourceModel

class DataSourceModel(ResourceModel):
    description: Union[str, None] = None # para ler temperaturas dos ar-cond
    subject_datasource: Union[str, None] = None              # Temperatura
    type: str                            # csv, xml, tsv, BDR (select)
    connection_url: Union[str, None] = None # exemplo: jdbc:postgresql://ip:porta/nome_bd
    username: Union[str, None] = None
    password: Union[str, None] = None
    jdbc_driver: Union[str, None] = None # org.postgresql.Driver
    csv_file: Union[str, None] = None
    
# configuração de mapeamento    r2rml-f (https://github.com/chrdebru/r2rml-tutorial)
# CSVFiles = weatherstations.csv
# mappingFile = ./weather-mapping.ttl
# outputFile = ./weather-output.ttl
# format = TURTLE