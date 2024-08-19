import os, platform
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, HTTPException, status
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, RMLConstructs, OperationalSystem, VSKG, NamedGraph
import commons
from uuid import uuid4
from model.datasource_model import DataSourceModel
from model.meta_mashup_model import MetaMashupModel, AddExporteViewsModel, AddSparqlQueryParamsModel

from langchain_community.graphs import OntotextGraphDBGraph
from langchain.chains import OntotextGraphDBQAChain
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
# from pydantic import BaseModel

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def make_question(repo:str, question:str):
    print('----------route:make_question----------')
    llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)
    graph = OntotextGraphDBGraph(
        query_endpoint="http://localhost:7200/repositories/EKG_MUSICA_BR",
        query_ontology="""
            CONSTRUCT {?s ?p ?o} 
            FROM <https://graphdb.arida.site/repositories/EKG_MUSICA_BR/rdf-graphs/TBOX> 
            WHERE {?s ?p ?o}
        """
    )
    chain = OntotextGraphDBQAChain.from_llm(
        llm,
        graph=graph,
        verbose=True,
    )
    re = chain.invoke({chain.input_key: question})[chain.output_key]   
    return re


