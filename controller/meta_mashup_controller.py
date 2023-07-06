import os
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, RMLConstructs
from uuid import uuid4
from model.datasource_model import DataSourceModel

CLASSE = 'drm:DataAsset'

def materialize_exported_view(uri:str):
    """Entrada: URI da visão exporta do mekg, classe da OL, lista colunas:str"""
    # <http://www.arida.ufc.br/VSKG/ExportedView_RFB_SEFAZ_MA> vskg:hasMappings ?mapping .
    uri_decoded = unquote_plus(uri)
    
    existe = api.check_resource(uri_decoded) # Primeiro, pegar o recurso que existe
    if(existe is None):
        return "not found"
    else:
      sparql = Prefixies.META_MASHUP + f""" select * where {{ 
        <{uri_decoded}> vskg:hasMappings ?mapping .
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
          filter(str(?pomColumn) IN ("CNPJ", "ROTULO"))
      }}"""
      query = {"query": sparql}
      res_exp_view = api.execute_query(query)

      # print('res exp view', res_exp_view)
      construct_prefixies = res_exp_view[0]['prefixies']['value']
      sql_query = res_exp_view[0]['sqlQuery']['value']
      classes = res_exp_view[0]['classes']['value']
      template = res_exp_view[0]['template']['value']

      for p in res_exp_view:
         pomColumn = p['pomColumn']['value']
         pomDatatype = p['pomDatatype']['value']
         pomType = p['pomType']['value']
         predicate = p['predicate']['value']
        #  pomTemplate = p['pomTemplate']['value'] or None
         print('pom:', pomColumn, pomType, predicate)

      # print('pom', poms)

      file_name = str(res_exp_view[0]['map_label']['value']).replace('"', '')
      mapping_file = open(f".{os.sep}mappings{os.sep}{file_name}.ttl", "w", encoding='utf-8')
      

      # 1. Construir o arquivo RML
      ev = api.ExportedView()
      res_datasource = ev.get_datasource_properties(uri_decoded) # 2. trazer os dados de acesso à fonte.
      propriedade_para_str_triplificacao = res_datasource[0]

      # 3. Adicionar o código que define o acesso ao BD ao arquivo de mapeamento RML.IO
      construct_rml_source = RMLConstructs.construct_rml_code_source(propriedade_para_str_triplificacao['conn']['value'],
                                            propriedade_para_str_triplificacao['jdbc_driver']['value'],
                                            propriedade_para_str_triplificacao['un']['value'],
                                            propriedade_para_str_triplificacao['pwd']['value'])
      construct_rml_logical_source = RMLConstructs.construct_rml_code_logical_source("", sql_query)

      construct_rml_subject = RMLConstructs.construct_rml_code_subject(template, classes)
      construt_rml_triples_map = RMLConstructs.construct_rml_code_triple_map(construct_rml_subject, "")

      # 4. Escrever o arquivo
      mapping_file.write(construct_prefixies + "\n\n")
      mapping_file.write(construct_rml_source + "\n\n")
      mapping_file.write(construct_rml_logical_source + "\n\n")
      mapping_file.write(construt_rml_triples_map + "\n\n")


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
