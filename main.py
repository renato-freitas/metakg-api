from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import platform
import os
from pydantic import BaseModel
from uuid import uuid4
import json
from urllib.parse import quote_plus, quote
from commons import Endpoint, Prefixies, Functions, NameSpaces, RoutesPath, Ontology as o
from models import DataSource, MetaMashupModel, HighLevelMapping, DataProperty, AddGCLMashupModel, AssociaMetaMashupMOdel
from api import MetaEKG, MetaMashup

app = FastAPI()

origins = [
    "http://localhost:3002",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uvicorn main:app --reload
@app.get("/")
async def index():
  return { "status_code": 200, "message": "metakg-api is online." }


# ROTAS DO META-MASHUP

@app.post(RoutesPath.META_MASHUP)
async def instancia_meta_mashup(obj: MetaMashupModel):
  """Rota para instanciar um Grafo de Metadados Mashup (Meta-Mashup). Verificar se pode ter ponto no nome"""
  print('instancia_meta_mashup')
  print(f'obj: {obj}')
  m = MetaMashup()
  return m.cria_um_recurso_meta_mashup(obj) 


@app.get(f'{RoutesPath.META_MASHUP}/{{uri}}')
def obtem_meta_mashup(uri:str):
  """Rota para obter um Grafo de Metadados Mashup (Meta-Mashup)"""
  m = MetaMashup()
  return m.obtem_um_recurso_meta_mashup(uri) 


@app.get(RoutesPath.META_MASHUP)
def obtem_meta_mashups():
  """Rota para obter um Grafo de Metadados Mashup"""
  m = MetaMashup()
  return m.lista_recursos_meta_mashup()  


@app.get("/propriedades/mashup/")
def obtem_propriedades(uri):
  """Rota para listar as propriedades de um recurso"""
  print("obtem_propriedades do meta-mashup")
  m = MetaMashup()
  return m.encontra_propriedades(uri)  


@app.post(f'{RoutesPath.META_MASHUP}/associa/')
def associa(obj: AssociaMetaMashupMOdel):
  print("associa")
  m = MetaMashup()
  return m.associa_metaEKG(obj) 


# @app.post("/meta-mashup/gcl/")
@app.post(f'{RoutesPath.META_MASHUP}/{{gcl}}/')
def add_gcl(data: AddGCLMashupModel):
  """Rota para copiar um GCL do EKG para a Especificação da Visão Mashup"""
  print(f'dados: {data}')
  m = MetaMashup()
  return m.add_gcl_visao_semantica_mashup(data) 

@app.get(f'{RoutesPath.META_MASHUP}/{{gcl}}/')
def obtem_gcl():
  """Rota para obter um Grafo de Conhecimento Local"""
  m = MetaMashup()
  return m.obtem_gcl()  


@app.get("/meta-mashup/gcl/{uri}")
async def obtem_gcl(uri: str):
  """Rota para obter um Grafo de Conhecimento Local"""
  m = MetaMashup()
  return m.obtem_gcl_by_uri(uri)  






# ROTAS DO EKG
@app.get("/meta-ekg/")
def obtem_instancias_meta_ekg():
  """Rota para instâncias de Grafo de Metadadso EKG"""
  print("obtem_instancias_meta_ekg")
  m = MetaEKG()
  return m.encontra_recursos()  


@app.get("/propriedades/")
def obtem_propriedades(uri):
  """Rota para listar as propriedades de um recurso"""
  print("obtem_propriedades")
  m = MetaEKG()
  return m.encontra_propriedades(uri)  




@app.get("/meta-ekg/gcl/")
def obtem_gcl_ekg(uri: str):
  """Rota para obter todos os Grafo de Conhecimento Local da Visão Semântica do EKG"""
  print(f'obtem gcl ekg')
  m = MetaEKG()
  return m.lista_gcl_do_meta_ekg(uri) 





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
  r = requests.get(Endpoint.METAKG, params=sparql)

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
