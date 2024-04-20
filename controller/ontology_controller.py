import os, platform
from fastapi import FastAPI, HTTPException, status
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, RMLConstructs, OperationalSystem, VSKG, NamedGraph
import commons
from uuid import uuid4
from model.datasource_model import DataSourceModel
from model.meta_mashup_model import MetaMashupModel, AddExporteViewsModel, AddSparqlQueryParamsModel


def retrieve_generalization_classes():
    sparql = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX sfz: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX : <http://www.sefaz.ma.gov.br/ontology/>
SELECT ?class ?label (MAX(?__comment) as ?comment) FROM <""" +NamedGraph.KG_TBOX_BIGDATAFORTALEZA+"""> { 
    {
        ?subclass rdfs:subClassOf ?class.
        ?class a owl:Class.
    } 
    UNION
    {
        ?subclass rdfs:subClassOf ?class.
        ?class a rdfs:Class.
    }
    OPTIONAL
    {
        ?class rdfs:label ?_label.
        FILTER(lang(?_label)="pt")    
    }
    OPTIONAL
    {
        ?class rdfs:comment ?_comment.
        FILTER(lang(?_comment)="pt")
    }
    OPTIONAL
    {
        ?class dcterms:description ?_description.
        FILTER(lang(?_description)="pt")
    }
    BIND(COALESCE(?_label,?class) AS ?label)
    BIND(COALESCE(?_comment,?_description) AS ?__comment)
    FILTER(!CONTAINS(STR(?class),"http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
    FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2000/01/rdf-schema#"))
    FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2001/XMLSchema#"))
    FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2002/07/owl#"))           
} GROUP BY ?class ?label
ORDER BY ?label"""
    result = api.Tbox().execute_query({"query": sparql})
    # print('***', result)
    return result



def retrieve_semantic_view_exported_classes():
    sparql = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT ?class ?label ?superclass (MAX(?__comment) as ?comment) FROM <""" +NamedGraph.KG_TBOX_BIGDATAFORTALEZA+"""> { 
    {
        ?class rdfs:subClassOf ?superclass.
    } 
    OPTIONAL
    {
        ?class rdfs:label ?_label.
        FILTER(lang(?_label)="pt")    
    }
    OPTIONAL
    {
        ?class rdfs:comment ?_comment.
        FILTER(lang(?_comment)="pt")
    }
    OPTIONAL
    {
        ?class dcterms:description ?_description.
        FILTER(lang(?_description)="pt")
    }
    BIND(COALESCE(?_label,?class) AS ?label)
    BIND(COALESCE(?_comment,?_description) AS ?__comment)
    FILTER(!CONTAINS(STR(?superclass),"_:node"))
    FILTER(!CONTAINS(STR(?class),"http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
    FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2000/01/rdf-schema#"))
    FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2001/XMLSchema#"))
    FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2002/07/owl#"))           
} GROUP BY ?class ?label ?superclass
ORDER BY ?label"""
    result = api.Tbox().execute_query({"query": sparql})
    # print('***', result)
    return result

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




# ====================
# OBTER AS CLASSES DE GENERALIZAÇÃO
# ===========
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX owl: <http://www.w3.org/2002/07/owl#>
# PREFIX sfz: <http://www.sefaz.ma.gov.br/ontology/>
# SELECT distinct ?o ?vo ?type_o  ?t  FROM <http://www.sefaz.ma.gov.br/named-graph/TBOX> { 
# 	?s rdfs:subClassOf ?o .
# 	?s a ?type_s.
#   	?o a owl:Class .
# 	?o a ?type_o.
# 	BIND( STR(?type_o) AS ?t)
# 	BIND( STR(?o) AS ?vo)
# 	FILTER ( (STR(?o) != "http://www.w3.org/2002/07/owl#Thing")  && STR(?vo) != "http://xmlns.com/foaf/0.1/Agent" &&
# STR(?vo) != "http://www.w3.org/2004/02/skos/core#Concept" && STR(?vo) != "http://purl.org/NET/c4dm/event.owl#Event" && STR(?type_o) != "http://www.w3.org/2002/07/owl#NamedIndividual")

# } order by ?o