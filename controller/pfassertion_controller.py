from fastapi import FastAPI, HTTPException, status
from urllib.parse import unquote_plus
import api
from model.global_model import PropertyFunctionAssertionModel
from commons import NameSpaces as ns, Prefixies, VSKG, TBOX_SAVED_QUERY, NamedGraph
from uuid import uuid4
from controller import global_controller


def create_pfa(data:PropertyFunctionAssertionModel, repo:str):
    print('---------create_pfa------------\n')
    uuid = uuid4()
    resource = f'{ns.ARIDA_R}PFA/{uuid}'
#   <http://localhost:7200/repositories/{data.repository}/rdf-graphs/KG_COMPETENCE_QUESTION> {{
    sparql = Prefixies.COMPETENCE_QUESTION + f"""INSERT DATA {{
    <{NamedGraph(data.repository).KG_PFA}> {{
        <{resource}> {VSKG.P_IS_A} {VSKG.C_PFA}; 
            {VSKG.P_DC_IDENTIFIER} "{uuid}"; 
            {VSKG.P_LABEL} "{data.name}"; 
            {VSKG.P_NAME} "{data.name}"; 
            {VSKG.P_GENERALIZATION_CLASS} "{data.generalizationClass}"; 
            {VSKG.P_DC_DESCRIPTION} \"""{data.description}\""";
            {VSKG.P_PFA_FUNCTION} \"""{data.function}\""".
        }}
    }}"""
    
    _query = {"update": sparql}
    print('-----------sparql-----\n', sparql)
    result = api.PropertyFunctionAssertion(repo).execute_query_insert_data(query=_query, name=data.name, repository=data.repository)
    return result



def retrieve_pfa_by_class(classGen:str, repo:str):
    """Recupera recursos do repositório usando paginação. [falta testar paginação]"""
    sparql = Prefixies.COMPETENCE_QUESTION + f"""SELECT * FROM <{NamedGraph(repo).KG_PFA}> {{ 
    ?uri {VSKG.P_IS_A} {VSKG.C_PFA};
            {VSKG.P_DC_IDENTIFIER} ?identifier; 
            {VSKG.P_LABEL} ?label; 
            {VSKG.P_NAME} ?name; 
            {VSKG.P_PFA_FUNCTION} ?function;
            {VSKG.P_GENERALIZATION_CLASS} "{classGen}".
      OPTIONAL {{ ?uri {VSKG.P_DC_DESCRIPTION} ?description. }}
    }}"""
    query = {"query": sparql}
    print('----controller:sparql---------\n', sparql)
    response = api.Global(repo).execute_sparql_query(query)

    
   
    return response
    # result = api.ConsultaSalva(repo).execute_query()
    # return result


# def retrieve_one_competence_question(uri:str, repo:str):
#     uri_decoded = unquote_plus(uri)
#     sparql = F"""SELECT * FROM
#       <{NamedGraph(repo).KG_COMPETENCE_QUESTION}> {{
#         <{uri_decoded}> ?p ?o. 
#       }}"""
#     result = api.Global(repo).execute_sparql_query({"query": sparql})
#     return result


# def execute_competence_question(uri:str, repo:str):
#     _sparql = ""
#     uri_decoded = unquote_plus(uri)
#     exist = retrieve_one_competence_question(uri_decoded, repo)
#     if(len(exist) == 0):
#         return "not found"
#     else:
#       print('-------existe\n', exist)
#       for row in exist:
#           if row["p"]["value"] == ns.VSKG + "sparql":
#             print('>>>>>>>>>>>', row)
#             _sparql = row["o"]["value"]
#           continue
#       print('\n\n----------_sparql---\n', _sparql)
#       query = {"query": _sparql}
#       response = api.Global(repo).execute_sparql_query(query)
#     return response

