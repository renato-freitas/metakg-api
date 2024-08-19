from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
# import requests
# import platform
# import os
# from pydantic import BaseModel
# from uuid import uuid4
# import json
# from urllib.parse import quote_plus, quote
# from commons import VSKG as o
# from models import DataSource, MetaMashupModel, HighLevelMapping, DataProperty, AddGCLMashupModel, AssociaMetaEKGAoMetaMashupModel
# from api import MetaEKG, MetaMashup
# from routes import datasource
from routes import datasource_route, exported_view_route, mapping_route, global_routes, meta_mashup_route, meta_ekg_route
from routes import ontology_route, repository_route, query_route, competence_question_route, pfassetion_route
from routes import llm_route

app = FastAPI()
# app.include_router(user.router)
app.include_router(ontology_route.router)
app.include_router(datasource_route.router)
app.include_router(exported_view_route.router)
app.include_router(mapping_route.router)
app.include_router(global_routes.router)
app.include_router(meta_mashup_route.router)
app.include_router(meta_ekg_route.router)
app.include_router(repository_route.router)
app.include_router(query_route.router)
app.include_router(competence_question_route.router)
app.include_router(pfassetion_route.router)
app.include_router(llm_route.router)

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
  return { "status_code": status.HTTP_200_OK, "message": "meta-ekg api is online." }



# https://janakiev.com/blog/python-shell-commands/
# @app.get("/triplify")
# def run_triplification():
#   operational_system = platform.system()
#   if(operational_system == 'Windows'):
#     # r = os.system(".\\d2rq-dev\\dump-rdf.bat -u ufc_sem -p ufcsemantic22_ -f N-TRIPLE -j jdbc:oracle:thin:@10.1.1.188:1521/bigsem.sefaz.ma.gov.br C:\\Users\\Adm\\ldif-0.5.2\\gcl\\mappings\\map-rfb-old-maranhao.ttl > C:\\Users\\Adm\\graphdb-import\\can-delete-this.nt")
#     r = os.system("java -jar .\\tools\\rmlmapper-6.1.3-r367-all.jar -m .\\maps\\map-csv.ttl -o .\\aboxies\\teste-abox.ttl -s turtle")
#     return r
#   elif operational_system == 'Linux':
#     r = os.system("ls -a")
#     return r
