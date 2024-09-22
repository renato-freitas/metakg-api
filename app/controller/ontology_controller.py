import os, platform
from fastapi import FastAPI, HTTPException, status
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, RMLConstructs, OperationalSystem, VSKG, NamedGraph
import commons
from uuid import uuid4


def retrieve_generalization_classes(repo:str, language:str):
    print('\n---controller: retrieve_generalization_classes---')
    # _lang = f"@{language}" if language != "" else "" 
    sparql = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX schema: <http://schema.org/>
PREFIX sfz: <http://www.sefaz.ma.gov.br/ontology/>
PREFIX : <http://www.sefaz.ma.gov.br/ontology/>
SELECT ?classURI ?label (MAX(?__comment) as ?comment) ?image 
FROM <""" +NamedGraph(repo).TBOX+"""> { 
    {
        ?subclass rdfs:subClassOf ?classURI.
        ?classURI a owl:Class.
    } 
    UNION
    {
        ?subclass rdfs:subClassOf ?classURI.
        ?classURI a rdfs:Class.
    }
    OPTIONAL
    {
        ?classURI rdfs:label ?_label.
        FILTER(LANG(?_label)='"""+language+"""' || !LANGMATCHES(LANG(?_label), "*"))  
    }
    OPTIONAL
    {
        ?classURI rdfs:comment ?_comment.
        FILTER(LANG(?_comment)='"""+language+"""' || !LANGMATCHES(LANG(?_label), "*"))
    }
    OPTIONAL
    {
        ?classURI dcterms:description ?_description.
        FILTER(lang(?_description)='"""+language+"""' || !LANGMATCHES(LANG(?_label), "*"))
    }
    OPTIONAL
    {
        ?subclass rdfs:subClassOf ?classURI.
        ?classURI foaf:img ?image.
    }
    OPTIONAL
    {
        ?subclass rdfs:subClassOf ?classURI.
        ?classURI schema:thumbnail ?image.
    }
    BIND(COALESCE(?_label,?classURI) AS ?label)
    BIND(COALESCE(?_comment,?_description) AS ?__comment)
    FILTER(!CONTAINS(STR(?classURI),"http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
    FILTER(!CONTAINS(STR(?classURI),"http://www.w3.org/2000/01/rdf-schema#"))
    FILTER(!CONTAINS(STR(?classURI),"http://www.w3.org/2001/XMLSchema#"))
    FILTER(!CONTAINS(STR(?classURI),"http://www.w3.org/2002/07/owl#"))           
} GROUP BY ?classURI ?label ?image
ORDER BY ?label"""
    print('+ sparql:\n', sparql)
    result = api.Tbox(repo).execute_query({"query": sparql})
    return result



def retrieve_exported_semantic_view_datasources(repo:str):
    print('\n---controller..retrieve_exported_semantic_view_datasources---')
#     sparql = """PREFIX foaf: <http://xmlns.com/foaf/0.1/>
# PREFIX owl: <http://www.w3.org/2002/07/owl#>
# PREFIX dc: <http://purl.org/dc/elements/1.1/>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX : <http://www.arida.ufc.br/ontologies/music.owl#>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# SELECT DISTINCT ?datasource from <""" +NamedGraph(repo).TBOX+"""> { 
# #    PEGAR TODAS AS SUBCLASSES
#     {
#     	?classURI rdf:type owl:Class.    
#     }
#     union
#     {
#         ?classURI rdf:type rdfs:Class.  
#     }
#     MINUS { ?sub rdfs:subClassOf ?classURI. }
#     BIND(STRAFTER(STR(?classURI), "_") AS ?datasource)
# } ORDER BY ?datasource"""
    sparql = f"""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX vskg: <http://www.arida.ufc.br/VSKG/>
    SELECT DISTINCT ?datasource 
    FROM <""" +NamedGraph(repo).TBOX+"""> {{
        {{ ?classURI a owl:Class. }}
        union
        {{ ?classURI a rdfs:Class. }}
        ?classURI vskg:belongsToESV ?datasource .
    }} ORDER BY ?datasource"""
    print('+ sparql:', sparql)
    result = api.Tbox(repo).execute_query({"query": sparql})
    return result

# def retrieve_semantic_view_exported_datasources(repo:str):
#     sparql = """PREFIX foaf: <http://xmlns.com/foaf/0.1/>
# PREFIX owl: <http://www.w3.org/2002/07/owl#>
# PREFIX dc: <http://purl.org/dc/elements/1.1/>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX : <http://www.arida.ufc.br/ontologies/music.owl#>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# SELECT DISTINCT ?datasource where {
# #    PEGAR TODAS AS SUBCLASSES
#     ?classURI rdf:type owl:Class.
#     MINUS { ?sub rdfs:subClassOf ?classURI. }
#     ?i a ?classURI.
# #    GARANTIR QUE SÓ TENHA URI QUE É UM RECURSO
#     FILTER(!CONTAINS(STR(?i),"/resource/App")).
#     FILTER(!CONTAINS(LCASE(STR(?i)),"/resource/canonical")).
#     FILTER(!CONTAINS(LCASE(STR(?i)),"/resource/unification")).
# #    RECORTAR A URI PARA OBTER A FONTE DE DADOS DISTINTAS
#     BIND(STRAFTER(STR(?i), "resource/") AS ?_s)
#     BIND(STRBEFORE(STR(?_s), "/") AS ?datasource)
# } ORDER BY ?datasource"""
#     print('-------SPARQL GET EXPORTED VIEW---------\n', sparql)
#     result = api.Tbox(repo).execute_query({"query": sparql})
#     return result


def retrieve_exported_semantic_view_classes(repo:str, exported_view:str, language:str):
    print('\n---controller:_retrieve_exported_semantic_view_classes---')
    _lang = f"@{language}" if language != "" else "" 
    _exp_view = f"'{exported_view}'" + _lang
    sparql = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX schema: <http://schema.org/>
PREFIX svm: <http://www.arida.ufc.br/ontologies/music#>
PREFIX vskg: <http://www.arida.ufc.br/VSKG/>
SELECT ?classURI ?label ?superclass ?comment ?image FROM <""" +NamedGraph(repo).TBOX+"""> { 
    ?classURI vskg:belongsToESV '"""+exported_view+"""'.
    OPTIONAL { 
        ?classURI rdfs:label ?_label. 
        FILTER(lang(?_label)='"""+language+"""' || !LANGMATCHES(LANG(?_label), "*"))   
    }
    OPTIONAL { 
        ?classURI rdfs:comment ?_comment. 
        FILTER(lang(?_comment)='"""+language+"""' || !LANGMATCHES(LANG(?_comment), "*")) 
    }
    OPTIONAL
    {
        ?classURI dcterms:description ?_description.
        FILTER(lang(?_description)='"""+language+"""' || !LANGMATCHES(LANG(?_description), "*")) 
    }
    OPTIONAL
    {
        ?classURI foaf:img ?foaf_image.
    }
    OPTIONAL
    {
        ?classURI schema:thumbnail ?thumb_image.
    }
    BIND(COALESCE(?_label,?classURI) AS ?label)
    BIND(COALESCE(?_comment,?_description) AS ?comment)
    BIND(COALESCE(?foaf_image,?thumb_image) AS ?image)
    FILTER(!CONTAINS(STR(?classURI),"_:node"))
}""" 
# GROUP BY ?classURI ?label ?superclass ?sub ?image
# ORDER BY ?label"""
    print('+ sparql:', sparql)
    result = api.Tbox(repo).execute_query({"query": sparql})
    return result


def retrieve_metadata_classes(repo:str):
    sparql = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX schema: <http://schema.org/>
SELECT ?classURI ?label ?superclass (MAX(?__comment) as ?comment) FROM <""" +NamedGraph(repo).TBOX_METADATA+"""> { 
    ?classURI rdf:type owl:Class.
    MINUS { ?sub rdfs:subClassOf ?classURI. }
    OPTIONAL { 
        ?classURI rdfs:label ?_label. 
        FILTER(lang(?_label)="pt")
    }
    OPTIONAL { 
        ?classURI rdfs:comment ?_comment. 
        FILTER(lang(?_comment)="pt")
    }
    OPTIONAL
    {
        ?classURI dcterms:description ?_description.
        FILTER(lang(?_description)="pt")
    }
    BIND(COALESCE(?_label,?classURI) AS ?label)
    BIND(COALESCE(?_comment,?_description) AS ?__comment)
    FILTER(!CONTAINS(STR(?classURI),"_:node"))
} 
GROUP BY ?classURI ?label ?superclass ?sub
ORDER BY ?label"""
    return api.Tbox(repo).execute_query({"query": sparql})

# VERSÃO ANTIGA
# def retrieve_semantic_view_exported_classes():
#     sparql = """
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX owl: <http://www.w3.org/2002/07/owl#>
# PREFIX dcterms: <http://purl.org/dc/terms/>
# SELECT ?class ?label ?superclass (MAX(?__comment) as ?comment) FROM <""" +NamedGraph.KG_TBOX_BIGDATAFORTALEZA+"""> { 
#     {
#         ?class rdfs:subClassOf ?superclass.
#     } 
#     OPTIONAL
#     {
#         ?class rdfs:label ?_label.
#         FILTER(lang(?_label)="pt")    
#     }
#     OPTIONAL
#     {
#         ?class rdfs:comment ?_comment.
#         FILTER(lang(?_comment)="pt")
#     }
#     OPTIONAL
#     {
#         ?class dcterms:description ?_description.
#         FILTER(lang(?_description)="pt")
#     }
#     BIND(COALESCE(?_label,?class) AS ?label)
#     BIND(COALESCE(?_comment,?_description) AS ?__comment)
#     FILTER(!CONTAINS(STR(?superclass),"_:node"))
#     FILTER(!CONTAINS(STR(?class),"http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
#     FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2000/01/rdf-schema#"))
#     FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2001/XMLSchema#"))
#     FILTER(!CONTAINS(STR(?class),"http://www.w3.org/2002/07/owl#"))           
# } GROUP BY ?class ?label ?superclass
# ORDER BY ?label"""
#     result = api.Tbox().execute_query({"query": sparql})
#     # print('***', result)
#     return result

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