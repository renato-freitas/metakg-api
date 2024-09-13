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
from routes import global_routes, ontology_route, query_route, competence_question_route, pfassetion_route

app = FastAPI()
# app.include_router(user.router)
app.include_router(ontology_route.router)
# app.include_router(datasource_route.router)
# app.include_router(exported_view_route.router)
app.include_router(global_routes.router)
app.include_router(query_route.router)
app.include_router(competence_question_route.router)
app.include_router(pfassetion_route.router)

origins = [
    "http://localhost:3002",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:80",
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
  return { "status_code": status.HTTP_200_OK, "message": "ContextEKG_Explorer api is online." }