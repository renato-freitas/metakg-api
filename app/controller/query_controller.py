from fastapi import FastAPI, HTTPException, status
from urllib.parse import unquote_plus
import api
from model.query_model import SavedQueryModel
from commons import NameSpaces as ns, Prefixies, VSKG, TBOX_SAVED_QUERY, NamedGraph
from uuid import uuid4
from controller import global_controller


def create_saved_query(data:SavedQueryModel, repo:str):
    print('---------create_saved_query------------\n')
    uuid = uuid4()
    resource = f'{ns.ARIDA_R}SavedQuery/{uuid}'
    sparql = Prefixies.QUERIES + f"""INSERT DATA {{
  <http://localhost:7200/repositories/{data.repository}/rdf-graphs/KG_QUERY> {{
        <{resource}> {TBOX_SAVED_QUERY.P_IS_A} {TBOX_SAVED_QUERY.C_SAVED_QUERY}; 
            {TBOX_SAVED_QUERY.P_DC_IDENTIFIER} "{uuid}"; 
            {TBOX_SAVED_QUERY.P_LABEL} "{data.name}"@pt; 
            {TBOX_SAVED_QUERY.P_NAME} "{data.name}"@pt; 
            {TBOX_SAVED_QUERY.P_DC_DESCRIPTION} \"""{data.description}\"""@pt;
            {TBOX_SAVED_QUERY.P_GENERALIZATION_CLASS} "{data.generalizationClass}";
            {TBOX_SAVED_QUERY.P_SPARQL} \"""{data.sparql}\""".
        }}
    }}"""
    
    _query = {"update": sparql}
    print('-----------sparql-----\n', sparql)
    result = api.ConsultaSalva(repo).execute_query_data(query=_query, name=data.name, repository=data.repository)
    return result




def retrieve_queries(repo:str):
    """Recupera recursos do repositório usando paginação. [falta testar paginação]"""
    sparql = Prefixies.QUERIES + f"""SELECT * FROM <{NamedGraph(repo).KG_QUERY}> {{ 
    ?uri {TBOX_SAVED_QUERY.P_IS_A} {TBOX_SAVED_QUERY.C_SAVED_QUERY};
            {TBOX_SAVED_QUERY.P_DC_IDENTIFIER} ?identifier; 
            {TBOX_SAVED_QUERY.P_LABEL} ?label; 
            {TBOX_SAVED_QUERY.P_NAME} ?name; 
            {TBOX_SAVED_QUERY.P_SPARQL} ?sparql.
      OPTIONAL {{ ?uri {TBOX_SAVED_QUERY.P_DC_DESCRIPTION} ?description. }}
      OPTIONAL {{ ?uri {TBOX_SAVED_QUERY.P_GENERALIZATION_CLASS} ?generalizationClass. }}
    }}"""
    query = {"query": sparql}
    print('----controller:sparql---------\n', sparql)
    response = api.Global(repo).execute_sparql_query(query)
    return response
    # result = api.ConsultaSalva(repo).execute_query()
    # return result

def retrieve_one_saved_query(uri:str, repo:str):
    uri_decoded = unquote_plus(uri)
    sparql = F"""SELECT * FROM
      <{NamedGraph(repo).KG_QUERY}> {{
        <{uri_decoded}> ?p ?o. 
      }}"""
    # print(f'sparql: {sparql}')
    result = api.Global(repo).execute_sparql_query({"query": sparql})
    return result


def update(uri:str, data:SavedQueryModel, repo:str):
    uri_decoded = unquote_plus(uri)
    print('--------como tá chegando--------\n', uri_decoded)
    exist = global_controller.check_resource(uri_decoded, repo)
    if(len(exist) == 0):
        return "not found"
    else:
        print('---------exist----------\n', exist)
        sparql = Prefixies.QUERIES + f"""
            DELETE {{ 
                GRAPH <{NamedGraph(repo).KG_QUERY}> {{
                    <{uri_decoded}> ?o ?p .
                }}
            }}
            INSERT {{
                GRAPH <{NamedGraph(repo).KG_QUERY}> {{
                    <{uri_decoded}> {TBOX_SAVED_QUERY.P_IS_A} {TBOX_SAVED_QUERY.C_SAVED_QUERY} ; 
                        {TBOX_SAVED_QUERY.P_DC_IDENTIFIER} "{data.identifier}"; 
                        {TBOX_SAVED_QUERY.P_LABEL} "{data.name}"@pt; 
                        {TBOX_SAVED_QUERY.P_NAME} "{data.name}"@pt; 
                        {TBOX_SAVED_QUERY.P_DC_DESCRIPTION} \"""{data.description}\"""@pt;
                        {TBOX_SAVED_QUERY.P_GENERALIZATION_CLASS} "{data.generalizationClass}";
                        {TBOX_SAVED_QUERY.P_SPARQL} \"""{data.sparql}\""".
                }}
            }}
            WHERE {{
                GRAPH <{NamedGraph(repo).KG_QUERY}> {{
                    <{uri_decoded}> ?o ?p .
                }}
            }}"""
        print('-----------sparql update--------\n',sparql)
        query = {"update": sparql}

        response = api.ConsultaSalva(repo).update_saved_query(query)
        return response


# DELETAR UM RECURSO DEVIA SER GLOBAL
def delete_one_saved_query(uri: str, repo:str):
    uri_decoded = unquote_plus(uri)
    exist = global_controller.check_resource(uri_decoded, repo)
    print('------existe--\n', exist)
    if(len(exist) == 0):
        return "not found"
    else:
      sparql = f"""DELETE WHERE {{ GRAPH <{NamedGraph(repo).KG_QUERY}> {{
                  <{uri_decoded}> ?o ?p .
                  }}
              }}
          """
      print('-------controller:sparl-------------\n',sparql)
      query = {"update": sparql}
      result = api.ConsultaSalva(repo).delete_one_saved_query(query)
    return result



def execute_saved_query(uri:str, repo:str):
    
    _sparql = ""
    
    uri_decoded = unquote_plus(uri)
    # print('--------como tá chegando--------\n', uri_decoded)
    exist = retrieve_one_saved_query(uri_decoded, repo)
    if(len(exist) == 0):
        return "not found"
    else:
      # print('save query to be exeucted', exist)
      for row in exist:
          if row["p"]["value"] == ns.SAVED_QUERY + "sparql":
            print('>>>>>>>>>>>', row)
            _sparql = row["o"]["value"]
          continue
      print('\n\n----------_sparql---\n', _sparql)
      query = {"query": _sparql}
      response = api.Global(repo).execute_sparql_query(query)
    return response


# ========================
# old
# def create_query(data: QueryModel, repo:str):
#     query = f"""{{ 
#       "name": "{data.name}",
#       "body": "{data.body}",
#       "shared": "{data.shared}",
#       "owner": "{data.owner}",
#       "repository": "{data.repository}"
#     }}"""
#     result = api.ConsultaSalva(repo).execute_query_data(name=data.name, query=query)
#     return result


# def update_saved_query(data: QueryModel, repo:str):
#     query = f"""{{ 
#       "name": "{data.name}",
#       "body": "{data.body}",
#       "shared": "{data.shared}",
#       "owner": "{data.owner}",
#       "repository": "{data.repository}"
#     }}"""
#     result = api.ConsultaSalva(repo).update_saved_query(name=data.name, query=query)
#     return result