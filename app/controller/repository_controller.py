import os, platform
from fastapi import FastAPI, HTTPException, status
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, RMLConstructs, OperationalSystem, VSKG, NamedGraph
import commons
from uuid import uuid4
# from model.datasource_model import DataSourceModel
# from model.meta_mashup_model import MetaMashupModel, AddExporteViewsModel, AddSparqlQueryParamsModel


def retrieve_repostories():
    result = api.Repository().retrieve_all()
    return result