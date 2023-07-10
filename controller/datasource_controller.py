from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies
from uuid import uuid4
from model.datasource_model import DataSourceModel

CLASSE = 'drm:DataAsset'

def create(data: DataSourceModel):
    uuid = uuid4()
    uri = f'{ns.META_EKG}DataSource/{uuid}'

    query = Prefixies.DATASOURCE + f"""INSERT DATA {{
        <{uri}> rdf:type {CLASSE}; 
            rdfs:label "{data.label}"; 
            dc:description "{data.description}";
            vskg:type "{data.type}";
            vskg:connection_url "{data.connection_url}";    
            vskg:username "{data.username}";
            vskg:password "{data.password}";
            vskg:jdbc_driver "{data.jdbc_driver}".
        }}"""
    sparql = {"update": query}

    response = api.create_resource(sparql, CLASSE, data.label)
    return response

def read_resources():
    sparql = Prefixies.DATASOURCE + f""" select * where {{ 
            ?uri rdf:type {CLASSE};
               rdfs:label ?label;
               dc:description ?description.
        }}
        """
    query = {"query": sparql}

    response = api.execute_query(query)
    return response

def update(uri:str, data:DataSourceModel):
    uri_decoded = unquote_plus(uri)
    print('como tá chegando', uri_decoded)
    existe = api.check_resource(uri_decoded) # Primeiro, pegar o recurso que existe
    if(existe is None):
        return "not found$$$"
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
        response = api.update_resource(sparql)
        return response


def delete(uri:str):
    uri_decoded = unquote_plus(uri)
    
    existe = api.check_resource(uri_decoded) # Primeiro, pegar o recurso que existe
    if(existe is None):
        return "not found"
    else:
        print('E', existe)
        query = Prefixies.DATASOURCE + f"""
            DELETE WHERE {{ 
                <{uri_decoded}> ?o ?p .
            }}
        """
        print('',query)
        sparql = {"update": query}

        response = api.update_resource(sparql)
        return response


# def check_resource(uri:str):
#     sparql = Prefixies.DATASOURCE + f""" select * where {{ 
#             <{uri}> ?p ?o.
#         }} limit 1
#         """
#     print('sparql, ', sparql)
#     query = {"query": sparql}
#     response = api.read_resource(query)
#     return response

# $ java -jar r2rml.jar --connectionURL jdbc:mysql://localhost/r2rml \
#   --user foo --password bar \
#   --mappingFile mapping.ttl \
#   --outputFile output.ttl \
#   --format TURTLE