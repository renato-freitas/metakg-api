from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
import requests
import platform
import os
from pydantic import BaseModel
from uuid import uuid4
import json
from urllib.parse import quote_plus, quote
from commons import Endpoint, Prefixies, Functions, NameSpaces, RoutesPath, VSKG as o
from models import DataSource, MetaMashupModel, HighLevelMapping, DataProperty, AddGCLMashupModel, AssociaMetaEKGAoMetaMashupModel
from api import MetaEKG, MetaMashup
# from routes import datasource
from routes import datasource_route, user, exported_view_route, mapping_route, global_routes, meta_mashup_route, meta_ekg_route

app = FastAPI()
# app.include_router(user.router)
app.include_router(datasource_route.router)
app.include_router(exported_view_route.router)
app.include_router(mapping_route.router)
app.include_router(global_routes.router)
app.include_router(meta_mashup_route.router)
app.include_router(meta_ekg_route.router)

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
  return { "status_code": status.HTTP_200_OK, "message": "meta-ekg-api is online." }


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


# O que é esse associa
@app.post(f'{RoutesPath.META_MASHUP}/associa-meta-ekg')
def associa_meta_ekg(obj: AssociaMetaEKGAoMetaMashupModel):
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
  return m.lista_recursos_meta_ekg()  


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
