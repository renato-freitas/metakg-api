import os
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies
from uuid import uuid4
from model.datasource_model import DataSourceModel
from model.mapping_model import MappingModel

CLASSE = "vskg:Mappings"

def create(data: MappingModel):
    uuid = uuid4()
    uri = f'{ns.META_EKG}Mapping/{uuid}'

    sparql = Prefixies.MAPPING + f"""INSERT DATA {{
        <{uri}> rdf:type {CLASSE}; 
            rdfs:label "{data.label}"; 
            dc:description "{data.description}".
        }}"""
    print('q:', sparql)
    query = {"update": sparql}

    response = api.create_resource_kg_metadata(query, CLASSE, data.label)
    return response

def read_resources():
    sparql = Prefixies.ALL + f""" select * where {{ 
            ?uri rdf:type {CLASSE};
                 rdfs:label ?label.
        }} 
        """
    query = {"query": sparql}
    response = api.read_resources_metakg(query)
    return response

def read_resource(uri_exported_view):
    uri_decoded = unquote_plus(uri_exported_view)
    sparql = Prefixies.ALL + f""" select * where {{ 
        <{uri_decoded}> vskg:hasMappings ?uri.
            ?uri rdf:type vskg:Mappings;
                 rdfs:label ?label.
        }} 
        """
    print('><><', sparql)
    query = {"query": sparql}
    response = api.read_resources_metakg(query)
    return response

def update(uri:str, data:DataSourceModel):
    uri_decoded = unquote_plus(uri)
    
    existe = check_resource(uri_decoded) # Primeiro, pegar o recurso que existe
    if(existe is None):
        return "not found"
    else:
        print('E', existe)
        query = Prefixies.DATASOURCE + f"""
            DELETE {{ 
                <{uri_decoded}> ?o ?p .
            }}
            INSERT {{
                <{uri_decoded}> rdf:type {CLASSE} ; 
                    rdfs:label "{data.label}"; 
                    dc:description "{data.description}";
                    vskg:type "{data.type}";
                    vskg:connection_url "{data.connection_url}";    
                    vskg:username "{data.username}";
                    vskg:password "{data.password}";
                    vskg:jdbc_driver "{data.jdbc_driver}".
            }}
            WHERE {{
                <{uri_decoded}> ?o ?p .
            }}
        """
        print('',query)
        sparql = {"update": query}

        # Chamar a API
        response = api.update_resource_kg_metadata(sparql)
        return response


def check_resource(uri:str):
    sparql = Prefixies.DATASOURCE + f""" select * where {{ 
            <{uri}> ?p ?o.
        }} limit 1
        """
    print('sparql, ', sparql)
    query = {"query": sparql}
    response = api.read_one_resource_metakg(query)
    return response

