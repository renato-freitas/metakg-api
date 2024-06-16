from urllib.parse import unquote_plus
import api
from model.global_model import ResoucesSameAsModel
from commons import NameSpaces as ns, Prefixies, VSKG, TBOX_SAVED_QUERY, NamedGraph

def check_resource(uri:str, repo:str):
    """Verifica se um recurso existe no repositório"""
    sparql = f"""SELECT * WHERE {{ 
            <{uri}> ?p ?o.
        }} LIMIT 1"""
    result = api.Global(repo).execute_sparql_query({"query": sparql})
    return result



def retrieve_unification_resources(classRDF:str, page:int, rowPerPage:int, label:str, language:str, repo:str):
    print('-----retrieve_unification_resources-----\n')
    _filter_language = f'FILTER(LANG(?l)="{language}")' if language != "" else "" 
    uri_decoded = unquote_plus(classRDF)
    offset = page * rowPerPage
    sparql = f"""PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?uri ?label where {{
    ?uri owl:sameAs ?o.
    ?uri a <{uri_decoded}>.
    OPTIONAL{{
            ?uri rdfs:label ?l.
            {_filter_language}
        }}
     OPTIONAL {{
            ?uri rdfs:label ?l.
        }}
    FILTER(CONTAINS(LCASE(?l), "{label.lower()}"))
    FILTER(!CONTAINS(LCASE(STR(?uri)), "resource/canonical"))
    FILTER(!CONTAINS(LCASE(STR(?uri)), "resource/unification"))
    BIND(COALESCE(?l,?uri) AS ?label)
}}LIMIT {rowPerPage}
    OFFSET {offset}
    """
    print('-----------SPARQL--------\n', sparql)
    result = api.Global(repo).execute_sparql_query({"query": sparql})
    print('-----------', result)
    return result



def retrieve_resources(classRDF:str, page:int, rowPerPage:int, label:str, language:str, repo:str):
    """Recupera recursos do repositório usando paginação. [falta testar paginação]"""
    # print(f'*** RECUPERANDO RECURSOS DA CLASSE >>> {classRDF}')
    _filter_language = f'FILTER(LANG(?l)="{language.lower()}")' if language != "" else "" 
    _filter_search = f'FILTER(CONTAINS(LCASE(?l), "{label.lower()}"))' if label != "" else "" 
    offset = page * rowPerPage
    uri_decoded = unquote_plus(classRDF)

    sparql = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        SELECT distinct ?uri ?label WHERE {{ 
            ?uri a <{uri_decoded}>; 
                 dc:identifier ?id.
            OPTIONAL{{
                ?uri rdfs:label ?l.
                {_filter_language}
            }}
            OPTIONAL{{
                ?uri rdfs:label ?l.
            }}
            {_filter_search}
            BIND(COALESCE(?l,?uri) AS ?label)
            FILTER(!CONTAINS(LCASE(STR(?uri)),"resource/App"))
            FILTER(!CONTAINS(LCASE(STR(?uri)),"resource/unification"))
            FILTER(!CONTAINS(LCASE(STR(?uri)),"resource/canonical"))
        }}
        ORDER BY ?l
        LIMIT {rowPerPage}
        OFFSET {offset}
    """
    print(f'===sparql: retrieve_resources===\n', sparql)
    result = api.Global(repo).execute_sparql_query({"query": sparql})
    return result



def retrieve_one_resource(uri, repo:str):
    """Recupera todos os dados de um recurso"""
    print(f'PROCURANDO R DA CLASSE {uri}')
    uri_decoded = unquote_plus(uri)
    sparql = f"""SELECT * WHERE {{
        <{uri_decoded}> ?p ?o. 
    }}"""
    print(f'sparql: {sparql}')
    result = api.Global(repo).execute_sparql_query({"query": sparql})
    return result




def retrieve_properties_at_exported_view(uri:str, language:str, repo:str):
    """Recupera propriedades do repositório"""
    print('----------retrieve_properties_from_exported_view---------------\n')
    _filter_language = f'FILTER(LANG(?l)="{language}")' if language != "" else "" 
    uri_decoded = unquote_plus(uri)
    existe = check_resource(uri_decoded, repo) 
    if(existe is None):
        return "not found"
    else:
        sparql = f"""PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?origin ?target ?label ?p ?o ?prov where {{
    BIND(<{uri_decoded}> AS ?origin)
    {{      
     <{uri_decoded}> ?p ?o.
     BIND(STRAFTER(STR("{uri}"), "resource/") AS ?_s)
     BIND(STRBEFORE(STR(?_s), "/") AS ?prov)
     OPTIONAL {{
        ?p rdfs:label ?label. 
        {_filter_language}
     }}
    FILTER(!CONTAINS(LCASE(STR(?o)),"_:node") && !(?p = owl:topDataProperty) && !(?p = owl:sameAs))
}}
	UNION
    {{ 
                <{uri_decoded}> owl:sameAs+ ?same_r .
                bind(?same_r as ?target)
    }}
    UNION 
    {{
        ?same_l owl:sameAs+ <{uri_decoded}> .
                BIND(?same_l AS ?target)
    }}
        UNION 
    {{
        ?same_l2 owl:sameAs+ <{uri_decoded}> .
		?same_l2 owl:sameAs+ ?same_r2.	                        
        FILTER(?same_r2 != <{uri_decoded}>).
        BIND(?same_r2 AS ?target)
    }}
#    FILTER(!CONTAINS(LCASE(STR(?target)),"/resource/unification")).
# FILTER(!CONTAINS(LCASE(STR(?o)),"_:node") && !(?p = owl:topDataProperty))
}}"""
        result = api.Global(repo).get_properties_of_resource_in_exported_view(sparql)
        return result





def retrieve_sameAs_resources(uri:str, repo:str):
    """Recupera os recurso que tem link com a {uri}"""
    print('----RECUPERANDO OS LINKS SAMEAS DO RECURSO----\n')
    uri_decoded = unquote_plus(uri)
    existe = check_resource(uri_decoded, repo) 
    if(existe is None):
        return "not found"
    else:
        sparql = f"""PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?origin ?target  where {{
    BIND(<{uri_decoded}> AS ?origin)
    {{
		<{uri_decoded}> owl:sameAs+ ?same_r .
#        FILTER(!CONTAINS(STR(?same_r),"/resource/App")).
        BIND(?same_r AS ?target)
        
    }}
    UNION 
    {{
        ?same_l owl:sameAs+ <{uri_decoded}> .
        BIND(?same_l as ?target)
    }}
    FILTER(!CONTAINS(LCASE(STR(?target)),"/resource/App")).
    # FILTER(!CONTAINS(LCASE(STR(?target)),"/resource/canonical")).
    FILTER(!CONTAINS(LCASE(STR(?target)),"/resource/unification")).
}}"""
        print('===SPARQL: retrieve_sameAs_resources===\n', sparql)
        res = api.Global(repo).execute_sparql_query({'query': sparql})
        result = api.Global(repo).agroup_resources(res)
        print('*** SAMEAS AGRUPADO >>> ', result)
        return result
    




def get_quantity_of_all_resources(classRDF:str, label:str, sameas:str, repo:str):
    # FILTER(lang(?_label)="") :: falta definir esse filtro. os dados estão sem @pt ou @en
    if_sameas = "?r owl:sameAs ?r2." if sameas == True else ""
    uri_decoded = unquote_plus(classRDF)
    filter = f"""FILTER(CONTAINS(LCASE(STR(?label)),"{label.lower()}"))""" if label is not None else ""  
    sparql = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    SELECT (COUNT(?r) AS ?total) WHERE {{
    ?r a <{uri_decoded}> .
    {if_sameas}
    OPTIONAL {{ ?r rdfs:label ?_label.  }}
    BIND(COALESCE(?_label,?r) AS ?label)
    {filter}
}} """
    print(f'sparql: {sparql}')
    result = api.Global(repo).execute_sparql_query({"query": sparql})
    return int(result[0]['total']['value'])


# new
def retrieve_properties_at_unification_view(uri:str, repo:str):
    print('\n-------controller:retrieve_properties_from_unification_view--------\n')
    if(uri is None):
        return "not found"
    else:
        sparql = f"""PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX jsfn:<http://www.ontotext.com/js#>
SELECT ?origin ?target ?label ?p ?o ?prov where {{
    BIND(<{uri}> AS ?origin)
    {{      
     <{uri}> ?p ?o.
     BIND(jsfn:getContext("{uri}") AS ?prov)
     OPTIONAL {{ ?p rdfs:label ?label. FILTER(lang(?label)="pt") }}
    #  FILTER(!CONTAINS(LCASE(STR(?o)),"_:node") && !(?p = owl:topDataProperty) && !(?p = owl:sameAs))
    FILTER(!CONTAINS(LCASE(STR(?o)),"_:node") && !(?p = owl:topDataProperty))
    }}
	UNION
    {{ 
        <{uri}> owl:sameAs+ ?same_r .
        ?same_r ?p ?o.
        BIND(jsfn:getContext(STR(?same_r)) AS ?prov)
        OPTIONAL {{ ?p rdfs:label ?label. FILTER(lang(?label)="pt") }}
        bind(?same_r as ?target)
    }}
    UNION 
    {{
        ?same_l owl:sameAs+ <{uri}> .
        ?same_l ?p ?o.
        BIND(jsfn:getContext(STR(?same_l)) AS ?prov)
        OPTIONAL {{ ?p rdfs:label ?label. FILTER(lang(?label)="pt") }}
        BIND(?same_l AS ?target)
    }}
    UNION 
    {{
        ?same_l2 owl:sameAs+ <{uri}> .
		?same_l2 owl:sameAs+ ?same_r2.	                        
        ?same_r2 ?p ?o.
        BIND(jsfn:getContext(STR(?same_r2)) AS ?prov)
        OPTIONAL {{ ?p rdfs:label ?label. FILTER(lang(?label)="pt") }}
        FILTER(?same_r2 != <{uri}>).
        BIND(?same_r2 AS ?target)
    }}
#    FILTER(!CONTAINS(LCASE(STR(?target)),"/resource/unification")).
     FILTER(!CONTAINS(LCASE(STR(?o)),"_:node") && !(?p = owl:topDataProperty))
}}"""
        print('*** SPARQL VISAO UNIFICAÇÃO\n', sparql)
        result = api.Global(repo).get_properties_from_resources_in_unification_view(sparql)
    return result

# OPTIONAL { ?r rdfs:label ?_label.  }

# old
#  BIND(STRAFTER(STR("{uri}"), "resource/") AS ?_s)
#  BIND(STRBEFORE(STR(?_s), "/") AS ?prov)
def retrieve_properties_from_unification_view(data:ResoucesSameAsModel, repo:str):
    print('\n----------retrieve_properties_from_unification_view--------\n')
    if(data.resources is None):
        return "not found"
    else:
        sparql = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?prov ?p ?o ?label WHERE {"""
        for key in data.resources:
            sparql += f"""
            {{ 
                <{key}> ?p ?o. 
                BIND(STRAFTER("{key}", "resource/") AS ?_s)
                BIND(STRBEFORE(STR(?_s), "/") AS ?prov)
                OPTIONAL {{
                    ?p rdfs:label ?label. 
                    FILTER(lang(?label)="pt") 
                }}
                # BIND(COALESCE(?_label,?p) AS ?label)
            }}"""
        for value in data.resources[key]:
            sparql += f"""
            UNION
                {{ 
                    <{value}> ?p ?o. 
                    BIND(STRAFTER("{value}", "resource/") AS ?_s)
                    BIND(STRBEFORE(STR(?_s), "/") AS ?prov)
                    OPTIONAL {{
                        ?p rdfs:label ?label. 
                        FILTER(lang(?label)="pt") 
                    }}
                    # BIND(COALESCE(?_label,?p) AS ?label)
                }}"""
        sparql += """\nFILTER(!CONTAINS(STR(?o),"_:node") && !(?p = owl:topDataProperty) && !(?p = owl:sameAs) && !CONTAINS(STR(LCASE(?prov)), "canonical") && !CONTAINS(STR(LCASE(?prov)), "fusion"))\n}"""
        print('*** SPARQL VISAO UNIFICAÇÃO\n', sparql)
        result = api.Global(repo).get_properties_from_sameAs_resources(sparql)
    return result




# new
def retrieve_properties_at_fusion_view(uri:str, language:str, repo:str):
    print('\n-------controller:retrieve_properties_at_fusion_view--------\n')
    if(uri is None):
        return "not found"
    else:
        sparql = f"""PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX jsfn:<http://www.ontotext.com/js#>
SELECT ?can ?origin ?target ?p ?label ?o ?prov ?name where {{
    BIND(<{uri}> AS ?origin)
    {{
     <{uri}> ?p ?o.
     OPTIONAL {{ ?p rdfs:label ?label. FILTER(lang(?label)="pt") }}
     BIND(jsfn:getContext("{uri}") AS ?prov)
     BIND(URI(jsfn:canonicalUri("{uri}")) as ?can)
     FILTER(!CONTAINS(LCASE(STR(?o)),"_:node") && !(?p = owl:topDataProperty) && !(?p = owl:sameAs))
	}}
        UNION
    {{
        <{uri}> owl:sameAs+ ?same_r .
        ?same_r ?p ?o.
        BIND(jsfn:getContext(STR(?same_r)) AS ?prov)
        BIND(URI(jsfn:canonicalUri(STR(?same_r))) as ?can)
        OPTIONAL {{ ?p rdfs:label ?label. FILTER(lang(?label)="pt") }}
        bind(?same_r as ?target)
    }}
    	UNION
    {{
        ?same_l owl:sameAs+ <{uri}> .
        ?same_l ?p ?o.
        BIND(jsfn:getContext(STR(?same_l)) AS ?prov)
        BIND(URI(jsfn:canonicalUri(STR(?same_l))) as ?can)
        OPTIONAL {{ ?p rdfs:label ?label. FILTER(lang(?label)="pt") }}
		BIND(?same_l AS ?target)
    }}
        UNION
    {{
        ?same_l2 owl:sameAs+ <{uri}> .
        ?same_l2 owl:sameAs+ ?same_r2.
        ?same_r2 ?p ?o.
        BIND(jsfn:getContext(STR(?same_r2)) AS ?prov)
        BIND(URI(jsfn:canonicalUri(STR(?same_r2))) as ?can)
		OPTIONAL {{ ?p rdfs:label ?label. FILTER(lang(?label)="pt") }}
        FILTER(?same_r2 != <{uri}>).
        BIND(?same_r2 AS ?target)
    }}
    FILTER(!CONTAINS(LCASE(STR(?o)),"_:node") && !(?p = owl:topDataProperty))
    #    FUSÃO DA PROPRIEDADE FOAF:NAME
    BIND(jsfn:fusionOfName(?prov, STR(?p), ?o) as ?name)
}}"""
        print('--------sparql visão de fusão--------\n', sparql)
        result = api.Global(repo).get_properties_from_resources_in_fusion_view(sparql)
    return result



# {{
#     <{uri}> foaf:name ?name1.
#     <{uri}> owl:sameAs+ ?same_r .
#     ?same_r foaf:name ?name2.
#     OPTIONAL {{
#         ?same_l owl:sameAs <{uri}> .
#         ?same_l foaf:name ?name3. }}
#     OPTIONAL {{
#         ?same_l2 owl:sameAs+ <{uri}> .
#         ?same_l2 owl:sameAs+ ?same_r2.
#         ?same_r2 foaf:name ?name4.
#     }}
#     BIND(IF(BOUND(?name2), STR(?name2),"") as ?n2)
#     BIND(IF(BOUND(?name3), STR(?name3),"") as ?n3)
#     BIND(IF(BOUND(?name4), STR(?name4),"") as ?n4)
#     BIND(CONCAT(STR(?name1), STR(?n2), STR(?n3), STR(?n4)) as ?nome)
#     BIND(jsfn:fusionOfName(?name1, ?n2, ?n3, ?n4) as ?name)
# }}




def retrieve_timeline_of_one_resource(resourceURI, repo):
    uri_decoded = unquote_plus(resourceURI)
    existe = check_resource(uri_decoded, repo) 
    if(existe is None):
        return "not found"
    else:
        sparql = f"""PREFIX tl: <http://purl.org/NET/c4dm/timeline.owl#>
PREFIX tlo: <http://www.arida.ufc.br/ontologies/timeline#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?tl ?label ?inst ?update ?date ?property ?va ?vn WHERE {{        
    <{uri_decoded}> tlo:has_timeline ?tl.
    OPTIONAL {{ <{uri_decoded}> rdfs:label ?_label_pt. FILTER(lang(?_label_pt)="pt") }}
    OPTIONAL {{ <{uri_decoded}> rdfs:label ?_label. }}
    BIND(COALESCE(?_label_pt,?_label) AS ?__label)
    BIND(COALESCE(?__label,<{uri_decoded}>) AS ?label)
    ?inst tl:timeLine ?tl;
        tlo:has_update ?update;
        tl:atDate ?date.      
    ?update a tlo:Update;
        tlo:property ?property;
        tlo:old_value ?va;
        tlo:new_value ?vn.
}}ORDER BY ?date"""
        print('sparql',sparql)
        res = api.Global(repo).execute_sparql_query({'query': sparql})
        print('*** TIMELINE >>>', res)
        result = api.Global(repo).agroup_instants_in_timeline(res)
        print('*** SAMEAS AGRUPADO >>> ', result)
        return result



def retrieve_timeline_of_unification_resources(data: ResoucesSameAsModel, repo):
    print('***** TIMELINE UNIFICATION CONTROLLER ***\n', data.resources)
    if(data.resources is None):
        return "not found"
    else:
        cont = 1
        sparql = f"""PREFIX tl: <http://purl.org/NET/c4dm/timeline.owl#>
PREFIX tlo: <http://www.arida.ufc.br/ontologies/timeline#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?tl ?label ?inst ?update ?date ?property ?va ?vn WHERE {{"""   
    for key in data.resources:
        sparql += f"""
        {{
            <{key}> tlo:has_timeline ?tl.
            OPTIONAL {{
                <{key}> rdfs:label ?_label_pt. 
                FILTER(lang(?_label_pt)="pt") 
            }}
            OPTIONAL {{
                <{key}> rdfs:label ?_label. 
            }}
            BIND(COALESCE(?_label_pt,?_label) AS ?__label)
            BIND(COALESCE(?__label,<{key}>) AS ?label)
            ?inst tl:timeLine ?tl;
                tlo:has_update ?update;
                tl:atDate ?date.      
            ?update a tlo:Update;
                tlo:property ?property;
                tlo:old_value ?va;
                tlo:new_value ?vn.
        }}
        {"UNION" if cont < len(data.resources) else ""}
        """
        cont += 1
    # for value in data.resources[key]:
    #     sparql += f"""
    #     UNION
    #         {{
    #         <{value}> tlo:has_timeline ?tl.
    #     OPTIONAL {{
    #         <{value}> rdfs:label ?_label_pt. 
    #         FILTER(lang(?_label_pt)="pt") 
    #     }}
    #     OPTIONAL {{
    #         <{value}> rdfs:label ?_label. 
    #     }}
    #     BIND(COALESCE(?_label_pt,?_label) AS ?__label)
    #     BIND(COALESCE(?__label,<{value}>) AS ?label)
    #     ?inst tl:timeLine ?tl;
    #         tlo:has_update ?update;
    #         tl:atDate ?date.      
    #     ?update a tlo:Update;
    #         tlo:property ?property;
    #         tlo:old_value ?va;
    #         tlo:new_value ?vn. 
    #         }}"""
    sparql += "}ORDER BY ?date"
    print('----sparql-----\n',sparql)
    res = api.Global(repo).execute_sparql_query({'query': sparql})
    print('*** TIMELINE >>>', res)
    result = api.Global(repo).agroup_instants_in_timeline(res)
    print('*** SAMEAS AGRUPADO >>> ', result)
    return result




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