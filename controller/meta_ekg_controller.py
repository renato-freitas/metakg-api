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
               OPTIONAL {{ ?uri dc:description ?description. }}
        }}
        """
    query = {"query": sparql}
    print('{**}', query)
    response = api.execute_query_on_kg_metadata(query)
    return response


def suggested_exported_views(uri: str, fusionClass: str):
    uri_decoded = unquote_plus(uri)

	  # Primeiro, pegar o recurso que existe
    existe = api.check_resource_in_kg_metadata(uri_decoded)
    if(existe is None):
       return "not found"
    else:
        sparql = Prefixies.ALL + f""" select ?uri ?label where {{
			<{uri_decoded}> {VSKG.P_IS_A} <http://www.arida.ufc.br/VSKG#MetadataGraphEKG>;
        vskg:hasSemanticMetadata ?semanticMetadata.
    ?semanticMetadata vskg:hasSemanticView ?semanticView.
    ?semanticView vskg:hasLocalGraph ?exportedView.
    ?exportedView vskg:hasLocalOntology ?local_ontology;
                  rdfs:label ?label.
 	?local_ontology void:vocabulary ?vocabulary.
 	?vocabulary vskg:hasClasses ?classes .
    filter regex(str(?classes), "{fusionClass}", "i")
    
    ?semanticview vskg:hasLinksetView ?linksetview.
    ?linksetview vskg:hasLinkageRule ?linkagerule.
	?linkagerule vskg:hasMatchClass ?matchclass.
	filter regex(str(?matchclass), "{fusionClass}", "i")
    bind(?exportedView as ?uri)
        }}"""
        query = {"query": sparql}
        print('[3]', query)
        response = api.execute_query_on_kg_metadata(query)
        return response


