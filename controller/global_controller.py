from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies
from uuid import uuid4
from model.datasource_model import DataSourceModel

CLASSE = 'drm:DataAsset'


def find_resources(classRDF, page):
    offset = int(page) * 50
    # search = request.args.get('search',default="")
    uri_decoded = unquote_plus(classRDF)

    # filterSearch = ""
    # if search != None and search != '':
    #     filterSearch = f"""FILTER(REGEX(STR(?resource),"{search}","i") || REGEX(STR(?label),"{search}","i"))"""
    if classRDF != None and classRDF != '':
        sparql = f"""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            select ?uri ?label where {{ 
                ?uri a <{uri_decoded}>.
                OPTIONAL{{
                    ?uri rdfs:label ?l.
                }}
                BIND(COALESCE(?l,?uri) AS ?label)
                FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppEndereco/"))
                FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppRazaoSocial/"))
                FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppNomeFantasia/"))
            }}
            ORDER BY ?label
            LIMIT 50
            OFFSET {offset}
        """
    else:
        sparql = f"""
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            select ?uri ?label where {{ 
                ?uri ?p _:x2.
                OPTIONAL{{
                    ?uri rdfs:label ?l.
                }}
                BIND(COALESCE(?l,?uri) AS ?label)
                FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppEndereco/"))
                FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppRazaoSocial/"))
                FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppNomeFantasia/"))
            }}
            ORDER BY ?label
            LIMIT 50
            OFFSET {offset}
        """
    query = {"query": sparql}
    response = api.execute_query_resources(query, enviroment="DEV")
    return response




def find_properties(uri:str, expand_sameas:bool):
    expandSameAs = bool(expand_sameas)
    uri_decoded = unquote_plus(uri)
    existe = check_resource(uri_decoded) 
    if(existe is None):
        return "not found"
    else:
        response = api.get_properties(uri_decoded, expandSameAs)
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