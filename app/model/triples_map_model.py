from typing import Union
from .resource_model import ResourceModel

class LogicalSourceModel(ResourceModel):
  sqlQuery: Union[str, None] = None 

class SubjectMapModel(ResourceModel):
  template: Union[str, None] = None
  classe: str

class PredicateObjectModel(ResourceModel):
  type: Union[str, None] = None
  predicate: str
  column: str

class TriplesMapModel(ResourceModel):
  logicalTable: LogicalSourceModel
  subject: SubjectMapModel
  predicateObjectMap: PredicateObjectModel = []
  sqlQuery: Union[str, None] = None 
  template: Union[str, None] = None  
  classe: str                           
  connection_url: Union[str, None] = None 
  username: Union[str, None] = None
  password: Union[str, None] = None
  jdbc_driver: Union[str, None] = None 
  csv_file: Union[str, None] = None
  

  