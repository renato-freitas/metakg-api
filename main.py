from fastapi import FastAPI
import requests
import platform
import os
from pydantic import BaseModel
from uuid import uuid4
import json
from commons import Endpoint, Prefixies, Functions, NameSpaces
from models import DataSource, HighLevelMapping, DataProperty

app = FastAPI()


@app.get("/")
def index():
  return "api ok"
  # q = Prefixies.ALL + """SELECT * WHERE { 
  #   { ?s a owl:Class . } UNION { ?s a rdfs:Class . } 
  # }"""
  # sparql = { 'query': q }
  # r = requests.get(Endpoint.TIMELINE_TBOX, params=sparql)
  # r = requests.get(Endpoint.TESTE, params=sparql)
  # if(r.status_code == 200):
    # return r.text
  # else:
    # return 404


@app.post("/datasources/record/")
def register_data_source(data: DataSource):
  """Por enquanto só relacional e csv"""

  file_name = f'datasources\\{data.label.lower().replace(" ", "_")}.txt'
  
  print(Functions.obtem_arquivos('datasources\\'))
  
  with open(file_name, 'w') as file:
    file.write(data.url_or_path)
  # fonte_dados = Functions.encontraUm(f'<{NameSpaces.SEFAZMA}{data.label}>')
  # uuid = uuid4()
  # q = Prefixies.ALL + f"""
  #   INSERT DATA {{
  #   vskg:{data.label} rdf:type drm:DataAsset, <{data.type}> ; 
  #     dc:identifier "{uuid}" ;
  #     rdfs:label "{data.label}" ;
  #     dc:description "{data.description}" .
  # }}"""
  
  # sparql = { 'query': q }
  # headers = {'Accept': 'application/x-turtle', "Content-type": "application/x-www-form-urlencoded"}

  # r = requests.post(Endpoint.TESTE, params=sparql, headers=headers)

  # print(r)
  # if(r.status_code == 200):
  #   return r.content
  # else:
  #   return r.content
  return data

@app.get("/datasources")
def get_data_sources():
  q = Prefixies.MOKG + "SELECT * WHERE { ?s a mokg:DataSource . } limit 10"
  sparql = { 'query': q }
  r = requests.get(Endpoint.TESTE, params=sparql)

  print(r)
  if(r.status_code == 200):
    return r.content
  else:
    return r.content



@app.post("/high-level-mappings")
def register_high_level_mapping(data: HighLevelMapping):
  """Regista Mapeamento de Alto Nível"""

  Functions.create_high_level_mapping(data)


  return data

# https://janakiev.com/blog/python-shell-commands/
@app.get("/triplify")
def run_triplification():
  operational_system = platform.system()
  if(operational_system == 'Windows'):
    # r = os.system(".\\d2rq-dev\\dump-rdf.bat -u ufc_sem -p ufcsemantic22_ -f N-TRIPLE -j jdbc:oracle:thin:@10.1.1.188:1521/bigsem.sefaz.ma.gov.br C:\\Users\\Adm\\ldif-0.5.2\\gcl\\mappings\\map-rfb-old-maranhao.ttl > C:\\Users\\Adm\\graphdb-import\\can-delete-this.nt")
    r = os.system("java -jar .\\tools\\rmlmapper-6.1.3-r367-all.jar -m .\\maps\\map-csv.ttl -o .\\aboxies\\teste-abox.ttl -s turtle")
    return r
  elif operational_system == 'Linux':
    r = os.system("ls -a")
    return r
