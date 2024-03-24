import os, platform
from fastapi import FastAPI, HTTPException, status
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, RMLConstructs, OperationalSystem, VSKG
from uuid import uuid4
from model.datasource_model import DataSourceModel
from model.meta_mashup_model import MetaMashupModel, AddExporteViewsModel, AddSparqlQueryParamsModel


def find_classes():
    sparql = """
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		    select ?class ?label (MAX(?c) as ?comment) ?subclass where { 
            {
                ?class a owl:Class.
            }
            UNION{
                ?class a rdfs:Class.
            }
            OPTIONAL{
              ?subclass rdfs:subClassOf ?class.
            }
            OPTIONAL{
                ?class rdfs:label ?l.
        		FILTER(lang(?l)="pt")
            
            }
    		    OPTIONAL{
                ?class rdfs:comment ?c1.
        		FILTER(lang(?c1)="pt")
            }
            BIND(COALESCE(?l,?class) AS ?label)
    		    BIND(COALESCE(?c1,"") AS ?c)
            FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2000/01/rdf-schema#"))
            FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2001/XMLSchema#"))
            FILTER(!CONTAINS(STR(?class),"http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
            FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2002/07/owl#"))
        }GROUP BY ?class ?label ?subclass
        ORDER BY ?label     
    """
    query = {"query": sparql}
    response = api.execute_query_on_kg_metadata(query, enviroment="DEV")
    return response



# def find_resources(classRDF, page):
#     offset = int(page) * 50
#     uri_decoded = unquote_plus(classRDF)

#     print('ops ops', page, classRDF)
#     if classRDF != None and classRDF != '':
#         sparql = f"""
#             prefix owl: <http://www.w3.org/2002/07/owl#>
#             prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#             select ?resource ?label where {{ 
#                 ?resource a <{uri_decoded}>.
#                 OPTIONAL{{
#                     ?resource rdfs:label ?l.
#                 }}
#                 BIND(COALESCE(?l,?resource) AS ?label)
#                 FILTER(!CONTAINS(STR(?resource),"http://www.sefaz.ma.gov.br/resource/AppEndereco/"))
#                 FILTER(!CONTAINS(STR(?resource),"http://www.sefaz.ma.gov.br/resource/AppRazaoSocial/"))
#                 FILTER(!CONTAINS(STR(?resource),"http://www.sefaz.ma.gov.br/resource/AppNomeFantasia/"))
#             }}
#             ORDER BY ?label
#             LIMIT 50
#             OFFSET {offset}
#         """
#     else:
#         sparql = f"""
#             prefix owl: <http://www.w3.org/2002/07/owl#>
#             prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#             select ?resource ?label where {{ 
#                 ?resource ?p _:x2.
#                 OPTIONAL{{
#                     ?resource rdfs:label ?l.
#                 }}
#                 BIND(COALESCE(?l,?resource) AS ?label)
#                 FILTER(!CONTAINS(STR(?resource),"http://www.sefaz.ma.gov.br/resource/AppEndereco/"))
#                 FILTER(!CONTAINS(STR(?resource),"http://www.sefaz.ma.gov.br/resource/AppRazaoSocial/"))
#                 FILTER(!CONTAINS(STR(?resource),"http://www.sefaz.ma.gov.br/resource/AppNomeFantasia/"))
#             }}
#             ORDER BY ?label
#             LIMIT 50
#             OFFSET {offset}
#         """
#     print(sparql)
#     query = {"query": sparql}
#     response = api.execute_query_resources(query, enviroment="DEV")
#     return response