import api
from commons import NameSpaces as ns
from uuid import uuid4

def create(data):
    uuid = uuid4()
    uri = f'{ns.VSKGR}DataSource/{uuid}'
    classe = 'drm:DataAsset'

    # Montar SPARQL
    print(data)
    sparql = f"""{uri} rdf:type {classe}; 
            rdfs:label "{data.label}" ; 
            dc:description "{data.description}"."""
    
    # Chamar a API
    response = api.create_resource(sparql)
    return response