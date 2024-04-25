from urllib.parse import quote_plus, unquote_plus
from typing import Union
import api
from commons import NameSpaces as ns, Functions, Prefixies
from uuid import uuid4
from model.datasource_model import DataSourceModel
from model.global_model import ResoucesSameAsModel

def check_resource(uri:str):
    """Verifica se um recurso existe no repositório"""
    sparql = f"""SELECT * WHERE {{ 
            <{uri}> ?p ?o.
        }} LIMIT 1"""
    # print('***\n',sparql)
    result = api.Global().execute_sparql_query({"query": sparql})
    return result



def retrieve_resources(classRDF:str, page:int, rowPerPage:int, label:str):
    """Recupera recursos do repositório usando paginação. [falta testar paginação]"""
    print(f'*** RECUPERANDO RECURSOS DA CLASSE >>> {classRDF}')
    offset = page * rowPerPage
    uri_decoded = unquote_plus(classRDF)

    sparql = f"""
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        select ?uri ?label where {{ 
            ?uri a <{uri_decoded}>; 
                 dc:identifier ?id.
            OPTIONAL{{
                ?uri rdfs:label ?l.
            }}
            FILTER(CONTAINS(LCASE(?l), "{label.lower()}"))
            BIND(COALESCE(?l,?uri) AS ?label)
            # FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppEndereco/"))
            # FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppRazaoSocial/"))
            # FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppNomeFantasia/"))
        }}
        ORDER BY ?id
        LIMIT {rowPerPage}
        OFFSET {offset}
    """
    print(f'sparql: {sparql}')
    result = api.Global().execute_sparql_query({"query": sparql})
    return result



def retrieve_one_resource(uri):
    """Recupera todos os dados de um recurso"""
    print(f'PROCURANDO R DA CLASSE {uri}')
    uri_decoded = unquote_plus(uri)
    sparql = f"""SELECT * WHERE {{
        <{uri_decoded}> ?p ?o. 
    }}"""
    print(f'sparql: {sparql}')
    result = api.Global().execute_sparql_query({"query": sparql})
    return result


def retrieve_properties_from_exported_view(uri:str):
    """Recupera propriedades do repositório"""
    uri_decoded = unquote_plus(uri)
    existe = check_resource(uri_decoded) 
    if(existe is None):
        return "not found"
    else:
        result = api.Global().get_properties(uri_decoded)
        return result


def retrieve_sameAs_resources(uri:str):
    """Recupera os recurso que tem link com a {uri}"""
    print('*** RECUPERANDO OS LINKS SAMEAS DO RECURSO')
    uri_decoded = unquote_plus(uri)
    existe = check_resource(uri_decoded) 
    if(existe is None):
        return "not found"
    else:
        sparql = f"""PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?origin ?target  where {{
    BIND(<{uri_decoded}> AS ?origin)
    {{
		<{uri_decoded}> owl:sameAs ?same_r .
#        FILTER(!CONTAINS(STR(?same_r),"/resource/App")).
        BIND(?same_r AS ?target)
        
    }}
    UNION 
    {{
        ?same_l owl:sameAs <{uri_decoded}> .
        BIND(?same_l as ?target)
    }}
}}"""
        res = api.Global().execute_sparql_query({'query': sparql})
        print('*** RESULTADO DA CONSULTA SPARQL >>>', res)
        result = api.Global().agroup_resources(res)
        print('*** SAMEAS AGRUPADO >>> ', result)
        return result
    




def get_quantity_of_all_resources(classRDF:str, label:str):
    # FILTER(lang(?_label)="") :: falta definir esse filtro. os dados estão sem @pt ou @en
    uri_decoded = unquote_plus(classRDF)
    filter = f"""FILTER(CONTAINS(LCASE(STR(?label)),"{label.lower()}"))""" if label is not None else ""  
    sparql = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    SELECT (COUNT(?r) AS ?total) WHERE {{
    ?r a <{uri_decoded}> .
    OPTIONAL {{ ?r rdfs:label ?_label.  }}
    BIND(COALESCE(?_label,?r) AS ?label)
    {filter}
}} """
    print(f'sparql: {sparql}')
    result = api.Global().execute_sparql_query({"query": sparql})
    return int(result[0]['total']['value'])







def retrieve_properties_from_unification_view(data:ResoucesSameAsModel):
    if(data.resources is None):
        return "not found"
    else:
        sparql = "PREFIX owl: <http://www.w3.org/2002/07/owl#>"
        for key in data.resources:
            sparql += f"""SELECT ?s ?p ?o WHERE {{ 
        {{ 
            <{key}> ?p ?o. 
            BIND(STRAFTER("{key}", "resource/") AS ?_s)
            BIND(STRBEFORE(STR(?_s), "/") AS ?s)
        }}
        """
            for value in data.resources[key]:
                sparql += f""" UNION
        {{ 
            <{value}> ?p ?o. 
            BIND(STRAFTER("{value}", "resource/") AS ?_s)
            BIND(STRBEFORE(STR(?_s), "/") AS ?s)
        }}
        FILTER(!CONTAINS(STR(?o),"_:node") && !(?p = owl:topDataProperty) && !(?p = owl:sameAs))
    }}"""
        # print('*** sparql uv', sparql)
        result = api.Global().get_properties_from_sameAs_resources(sparql)
    return result





# def retrieve_properties(uri:str):
#     uri_decoded = unquote_plus(uri)
#     existe = api.check_resource_in_kg_metadata(uri_decoded) 
#     if(existe is None):
#         return "not found"
#     else:
#         response = api.get_properties_kg_metadata(uri_decoded)
#         return response





# def find_properties(uri:str, expand_sameas:bool):
#     expandSameAs = bool(expand_sameas)
#     uri_decoded = unquote_plus(uri)
#     existe = check_resource(uri_decoded) 
#     if(existe is None):
#         return "not found"
#     else:
#         response = api.get_properties_kg_metadata(uri_decoded, expandSameAs)
#         return response


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



# def retrieve_resources(classRDF, page):
#     print(f'PROCURANDO R DA CLASSE {classRDF}')
#     offset = int(page) * 20
#     # search = request.args.get('search',default="")
#     uri_decoded = unquote_plus(classRDF)

#     # filterSearch = ""
#     # if search != None and search != '':
#     #     filterSearch = f"""FILTER(REGEX(STR(?resource),"{search}","i") || REGEX(STR(?label),"{search}","i"))"""
#     if classRDF != None and classRDF != '':
#         sparql = f"""
#             prefix owl: <http://www.w3.org/2002/07/owl#>
#             prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#             select ?uri ?label where {{ 
#                 ?uri a <{uri_decoded}>.
#                 OPTIONAL{{
#                     ?uri rdfs:label ?l.
#                 }}
#                 BIND(COALESCE(?l,?uri) AS ?label)
#                 FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppEndereco/"))
#                 FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppRazaoSocial/"))
#                 FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppNomeFantasia/"))
#             }}
#             ORDER BY ?label
#             LIMIT 20
#             OFFSET {offset}
#         """
#     else:
#         sparql = f"""
#             prefix owl: <http://www.w3.org/2002/07/owl#>
#             prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#             select ?uri ?label where {{ 
#                 ?uri ?p _:x2.
#                 OPTIONAL{{
#                     ?uri rdfs:label ?l.
#                 }}
#                 BIND(COALESCE(?l,?uri) AS ?label)
#                 FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppEndereco/"))
#                 FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppRazaoSocial/"))
#                 FILTER(!CONTAINS(STR(?uri),"http://www.sefaz.ma.gov.br/resource/AppNomeFantasia/"))
#             }}
#             ORDER BY ?label
#             LIMIT 50
#             OFFSET {offset}
#         """
#     print(f'sparql: {sparql}')
#     query = {"query": sparql}
#     response = api.execute_query_resources(query)
#     return response
    

    # GLOBAL - OBTER PROPRIEDADES
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX owl: <http://www.w3.org/2002/07/owl#>
# PREFIX dcterms: <http://purl.org/dc/terms/>
# SELECT * WHERE {
#     <http://www.sefaz.ma.gov.br/resource/Cadastro_SEFAZ-MA/Empresa/17636236> ?p ?o. 
#     MINUS { <http://www.sefaz.ma.gov.br/resource/Cadastro_SEFAZ-MA/Empresa/17636236> owl:topDataProperty ?o.}
#     FILTER(!CONTAINS(STR(?o),"_:node"))
# }