from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies
from uuid import uuid4
from model.datasource_model import DataSourceModel

CLASSE = 'drm:DataAsset'

def get_properties(uri:str):
    uri_decoded = unquote_plus(uri)
    existe = check_resource(uri_decoded) 
    if(existe is None):
        return "not found"
    else:
        response = api.get_properties(uri_decoded)
        return response





def check_resource(uri:str):
    sparql = Prefixies.DATASOURCE + f""" select * where {{ 
            <{uri}> ?p ?o.
        }} limit 1
        """
    query = {"query": sparql}
    response = api.read_resource(query)
    return response


# update

# <http://www.sefaz.ma.gov.br/RFB/ontology/> <http://www.arida.ufc.br/VSKG/hasClasses> ?o
# <http://www.sefaz.ma.gov.br/RFB/ontology/> <http://www.arida.ufc.br/VSKG/hasProperties> ?o.

# DELETE { 
#     <http://www.sefaz.ma.gov.br/RFB/ontology/> <http://www.arida.ufc.br/VSKG/hasProperties> ?o 
# }
# INSERT { 
#     <http://www.sefaz.ma.gov.br/RFB/ontology/> <http://www.arida.ufc.br/VSKG#hasProperties> ?o
# }
# WHERE { 
#     <http://www.sefaz.ma.gov.br/RFB/ontology/> <http://www.arida.ufc.br/VSKG/hasProperties> ?o
# }