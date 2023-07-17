import os, platform
from fastapi import FastAPI, HTTPException, status
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, RMLConstructs, OperationalSystem, VSKG
from uuid import uuid4
from model.datasource_model import DataSourceModel
from model.meta_mashup_model import MetaMashupModel, AddExporteViewsModel, AddSparqlQueryParamsModel


def create(data: MetaMashupModel):
    uuid = uuid4()
    uri = f'{ns.META_EKG}MetaMashup_{uuid}'
    sparql = Prefixies.META_MASHUP + f"""INSERT DATA {{
        <{uri}> rdf:type {VSKG.C_META_MASHUP}; 
            rdfs:label "{data.label}"; 
            dc:description "{data.description}";
            vskg:fusionClass "{data.fusionClass}".
        }}"""
    query = {"update": sparql}
    response = api.create_resource(query, VSKG.C_META_MASHUP, data.label)
    return response


def read_resources():
    sparql = Prefixies.ALL + f""" select * where {{ 
            ?uri rdf:type {VSKG.C_META_MASHUP};
               rdfs:label ?label.
               OPTIONAL {{ ?uri vskg:hasFusionKG ?fusionKG.
                    ?fusionKG vskg:hasFusionRules ?fusionRules.
                    ?fusionRules vskg:hasFusionClass ?fusionClass.
                 }}
               OPTIONAL {{ ?uri vskg:fusionClass ?fusionClass. }}
               OPTIONAL {{ ?uri vskg:mashupClass ?mashupClass. }}
               OPTIONAL {{ ?uri dc:description ?description. }}
        }}
        """
    query = {"query": sparql}
    response = api.execute_query(query)
    return response


def update(uri:str, data:MetaMashupModel):
    uri_decoded = unquote_plus(uri)
    existe = api.check_resource(uri_decoded)
    if(existe is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurso não existe!")
    else:
        print('E', existe)
        sparql = Prefixies.ALL + f"""
            DELETE {{ 
                <{uri_decoded}> rdf:type {VSKG.C_META_MASHUP} ; 
                    rdfs:label ?l; 
                    dc:description ?d;
                    vskg:fusionClass ?fusionClass.
            }}
            INSERT {{
                <{uri_decoded}> rdf:type {VSKG.C_META_MASHUP} ; 
                    rdfs:label "{data.label}"; 
                    dc:description "{data.description}";
                    vskg:fusionClass "{data.fusionClass}".
            }}
            WHERE {{
                <{uri_decoded}> rdf:type {VSKG.C_META_MASHUP} ; 
                    rdfs:label ?l; 
                    dc:description ?d;
                    vskg:fusionClass ?fusionClass.
            }}
        """
        query = {"update": sparql}
        response = api.update_resource(query)
        return response


def delete(uri:str):
    uri_decoded = unquote_plus(uri)
    existe = api.check_resource(uri_decoded) 
    if(existe is None):
        return "not found"
    else:
        query = Prefixies.ALL + f"""
            DELETE WHERE {{ 
                <{uri_decoded}> ?o ?p .
            }}
        """
        sparql = {"update": query}
        response = api.update_resource(sparql)
        return response


def add_exported_views(uri:str, data:AddExporteViewsModel):
    uri_decoded = unquote_plus(uri)
    existe = check_exist_exported_view_on_meta_mashup(uri_decoded)

    print('EXISTE:', existe)
    evs = []
    for e in data.exportedViewCheckeds:
        evs.append(f'<{e}>')
    evs_str = ",".join(evs)
    print('eeee:', evs_str)

    sparql = Prefixies.ALL
    if(existe is None or len(existe)==0):
        print("CRIAR")
        sparql += f"""
            INSERT DATA {{
                <{uri_decoded}> rdf:type {VSKG.C_META_MASHUP} ; 
                    vskg:hasExportedView {evs_str}.
            }}
        """
    else:
        print("ATUALIZAR")
        sparql += f"""
            DELETE {{ 
                <{uri_decoded}> rdf:type {VSKG.C_META_MASHUP} ; 
                    vskg:hasExportedView ?evs.
            }}
            INSERT {{
                <{uri_decoded}> rdf:type {VSKG.C_META_MASHUP} ; 
                    vskg:hasExportedView {evs_str}.
            }}
            WHERE {{
                <{uri_decoded}> rdf:type {VSKG.C_META_MASHUP} ; 
                    vskg:hasExportedView ?evs.
            }}
        """

    query = {"update": sparql}
    print('', query)
    response = api.update_resource(query)
    return response


def add_sparql_params_to_reuse_mappings(uri:str, data:AddSparqlQueryParamsModel):
    uuid = uuid4()
    uri_sqp = f'{ns.META_EKG}SparqlQueryParams_{uuid}'

    print('>uri_meta_mashup<', uri)
    _uri_meta_mashup = unquote_plus(uri)

    sparql = Prefixies.META_MASHUP + f"""INSERT DATA {{
        <{uri_sqp}> rdf:type {VSKG.C_META_MASHUP_SPARQL_QUERY_PARAMS}; 
            rdfs:label "{data.label}"; 
            vskg:exportedViewURI "{data.exportedViewURI}";
            vskg:localOntologyClass "{data.localOntologyClass}";
            vskg:sqpCol "{data.sqpCol}".
        <{_uri_meta_mashup}> vskg:sparqlQueryParams <{uri_sqp}>.
        }}"""
    query = {"update": sparql}
    response = api.create_resource(query, VSKG.C_META_MASHUP_SPARQL_QUERY_PARAMS, data.label)
    return response

def reade_sparql_params_to_reuse_mappings(uri:str):
    uri_decoded = unquote_plus(uri)
    sparql = Prefixies.ALL + f""" select * where {{ 
            <{uri_decoded}> rdf:type {VSKG.C_META_MASHUP};
              vskg:sparqlQueryParams ?sqp.
              ?sqp rdfs:label ?label. 
        }}
        """
    query = {"query": sparql}
    print('...', query)
    response = api.execute_query(query)
    return response

def check_exist_exported_view_on_meta_mashup(uri:str):
    sparql = Prefixies.ALL + f""" select * where {{ 
        <{uri}> rdf:type {VSKG.C_META_MASHUP}; 
            vskg:hasExportedView ?evs.
    }} limit 1"""
    query = {"query": sparql}
    response = api.execute_query(query)
    return response

def materialize_exported_view(uri: str):
    """Entrada: URI da visão exporta do mekg, classe da OL, lista colunas:str"""
    # <http://www.arida.ufc.br/VSKG/ExportedView_RFB_SEFAZ_MA> vskg:hasMappings ?mapping .

    uri_decoded = unquote_plus(uri)

	# Primeiro, pegar o recurso que existe
    existe = api.check_resource(uri_decoded)
    if(existe is None):
       return "not found"
    else:
        sparql = Prefixies.META_MASHUP + f""" select * where {{
			<http://www.arida.ufc.br/meta-ekg/resource/ExportedView/aeb43c62-1945-4e38-ab9a-2638960b6cbf> vskg:hasMappings ?mapping .
			?mapping rdfs:label ?map_label.
			?mapping vskg:hasTriplesMap ?tm.
			?mapping vskg:prefixies ?prefixies.
			?tm rr:logicalTable ?logicalSource.
			?logicalSource rr:sqlQuery ?sqlQuery.
			?tm rr:subject ?sub.
			?sub rr:class rfb:Estabelecimento.
			?sub rr:class ?classes.
			?sub rr:template ?template.
			?tm rr:predicateObjectMap ?pom.
			?pom vskg:pomColumn ?pomColumn.
			?pom vskg:pomDatatype ?pomDatatype.
			?pom vskg:pomType ?pomType.
			?pom vskg:predicate ?predicate.
			OPTIONAL {{ ?pom vskg:pomTemplate ?pomTemplate }}
			filter(str(?pomColumn) IN ("CNPJ", "ROTULO", "RAZAO_SOCIAL", "INSCRICAO_ESTADUAL"))
        }}"""

        query = {"query": sparql}
        res_exp_view = api.execute_query(query)

        prefixies = res_exp_view[0]['prefixies']['value']
        sql_query = res_exp_view[0]['sqlQuery']['value']
        classes = res_exp_view[0]['classes']['value']
        template = res_exp_view[0]['template']['value']

        props = {}
        for p in res_exp_view:
            pomColumn = p['pomColumn']['value']
            pomType = p['pomType']['value']
            predicate = p['predicate']['value']

            if p.get("pomTemplate") is not None:
                props[p['pomColumn']['value']] = [pomColumn, pomType, predicate, p['pomTemplate']['value']]
            else:
                props[p['pomColumn']['value']] = [pomColumn, pomType, predicate, ""]

            if p.get("pomDatatype") is not None:
                props[p['pomColumn']['value']].append(p['pomDatatype']['value'])
            else:
                props[p['pomColumn']['value']].append("")

        file_name = str(res_exp_view[0]['map_label']['value']).replace('"', '')
        mapping_file = open(f".{os.sep}mappings{os.sep}{file_name}.ttl", "w", encoding='utf-8')

        # 1. Construir o arquivo RML
        ev = api.ExportedView()
        # 2. trazer os dados de acesso à fonte.
        res_datasource = ev.get_datasource_properties(uri_decoded)
        propriedade_para_str_triplificacao = res_datasource[0]

        # 3. Adicionar o código que define o acesso ao BD ao arquivo de mapeamento RML.IO
        construct_prefixies = RMLConstructs.construct_rml_prefixies(prefixies)
        construct_rml_source = RMLConstructs.construct_rml_source(propriedade_para_str_triplificacao['conn']['value'],
                                            propriedade_para_str_triplificacao['jdbc_driver']['value'],
                                            propriedade_para_str_triplificacao['un']['value'],
                                            propriedade_para_str_triplificacao['pwd']['value'])
        construct_rml_logical_source = RMLConstructs.construct_rml_logical_source("", sql_query)
        construct_rml_subject = RMLConstructs.construct_rml_subject(template, classes)
        construct_props = RMLConstructs.construct_rml_datatype_or_object_property(props)
        construt_rml_triples_map = RMLConstructs.construct_rml_triple_map(construct_rml_subject, construct_props)

        # 4. Escrever o arquivo
        mapping_file.write(construct_prefixies + "\n")
        mapping_file.write(construct_rml_source + "\n\n")
        mapping_file.write(construct_rml_logical_source + "\n\n")
        mapping_file.write(construt_rml_triples_map + "\n\n")

        mapping_file.close()
        # Antes de materializar, verificar se o arquivo rml existe
        operational_system = platform.system()
        r = 'responsta'
        if(operational_system == OperationalSystem.WINDOWS):
            # r = os.system(".\\d2rq-dev\\dump-rdf.bat -u ufc_sem -p ufcsemantic22_ -f N-TRIPLE -j jdbc:oracle:thin:@10.1.1.188:1521/bigsem.sefaz.ma.gov.br C:\\Users\\Adm\\ldif-0.5.2\\gcl\\mappings\\map-rfb-old-maranhao.ttl > C:\\Users\\Adm\\graphdb-import\\can-delete-this.nt")
            r = os.system("java -jar .\\tools\\rmlmapper-6.2.0-r368-all.jar -m .\\mappings\\map-ufc.ttl -o .\\aboxies\\teste-ufc-postman-01.ttl -s turtle")
            return r
        elif operational_system == OperationalSystem.LINUX:
            r = os.system("ls -a")
            return r

        return res_exp_view














# def read_resources():
#     # classe = 'drm:DataAsset'

#     # Montar SPARQL
#     sparql = Prefixies.DATASOURCE + f""" select * where {{ 
#             ?uri rdf:type {CLASSE};
#                rdfs:label ?label.
#         }}
#         """
#     query = {"query": sparql}

#     # Chamar a API
#     response = api.read_resources(query)
#     return response

# def update(uri:str, data:DataSourceModel):
#     uri_decoded = unquote_plus(uri)
    
#     existe = check_resource(uri_decoded) # Primeiro, pegar o recurso que existe
#     if(existe is None):
#         return "not found"
#     else:
#         print('E', existe)
#         query = Prefixies.DATASOURCE + f"""
#             DELETE {{ 
#                 <{uri_decoded}> ?o ?p .
#             }}
#             INSERT {{
#                 <{uri_decoded}> rdf:type {CLASSE} ; 
#                     rdfs:label "{data.label}"; 
#                     dc:description "{data.description}";
#                     vskg:type "{data.type}";
#                     vskg:connection_url "{data.connection_url}";    
#                     vskg:username "{data.username}";
#                     vskg:password "{data.password}";
#                     vskg:jdbc_driver "{data.jdbc_driver}".
#             }}
#             WHERE {{
#                 <{uri_decoded}> ?o ?p .
#             }}
#         """
#         print('',query)
#         sparql = {"update": query}

#         # Chamar a API
#         response = api.update_resource(sparql)
#         return response


# def delete(uri:str):
#     uri_decoded = unquote_plus(uri)
    
#     existe = check_resource(uri_decoded) # Primeiro, pegar o recurso que existe
#     if(existe is None):
#         return "not found"
#     else:
#         print('E', existe)
#         query = Prefixies.DATASOURCE + f"""
#             DELETE WHERE {{ 
#                 <{uri_decoded}> ?o ?p .
#             }}
#         """
#         print('',query)
#         sparql = {"update": query}

#         response = api.update_resource(sparql)
#         return response


# def check_resource(uri:str):
#     sparql = Prefixies.DATASOURCE + f""" select * where {{ 
#             <{uri}> ?p ?o.
#         }} limit 1
#         """
#     print('sparql, ', sparql)
#     query = {"query": sparql}
#     response = api.read_resource(query)
#     return response
