import os, platform
from fastapi import FastAPI, HTTPException, status
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, RMLConstructs, OperationalSystem, VSKG
from uuid import uuid4
from model.datasource_model import DataSourceModel
from model.meta_mashup_model import MetaMashupModel

def read_resources():
    sparql = Prefixies.ALL + f""" select * where {{ 
            ?uri rdf:type <http://www.arida.ufc.br/VSKG#MetadataGraphEKG>;
               rdfs:label ?label.
              #  OPTIONAL {{ ?uri dc:description ?description. }}
        }}
        """
    query = {"query": sparql}
    print('{**}', query)
    response = api.execute_query(query)
    return response


def suggested_exported_views(uri: str, mashupClass: str):
    uri_decoded = unquote_plus(uri)

	  # Primeiro, pegar o recurso que existe
    existe = api.check_resource(uri_decoded)
    if(existe is None):
       return "not found"
    else:
        sparql = Prefixies.ALL + f""" select ?uri ?label where {{
			<{uri_decoded}> {VSKG.P_TYPE} <http://www.arida.ufc.br/VSKG#MetadataGraphEKG>;
        vskg:hasSemanticMetadata ?sm.
    ?sm vskg:hasSemanticView ?sv.
    ?sv vskg:hasLocalGraph ?ev.
    ?ev vskg:hasMappings ?m;
    	rdfs:label ?label.
    ?m vskg:hasTriplesMap ?tm.
    ?tm rr:subject ?sub.
    ?sub rr:class ?classes.
    filter(regex(str(?classes),"{mashupClass}","i"))
    bind(?ev as ?uri)
        }}"""
        query = {"query": sparql}
        print('{**}', query)
        response = api.execute_query(query)
        return response


