from urllib.parse import unquote_plus
import api
from model.query_model import QueryModel

def create_queries(data: QueryModel, repo:str):
    query = f"""{{ 
      "name": "{data.name}",
      "body": "{data.body}",
      "shared": "{data.shared}",
      "owner": "{data.owner}",
      "repository": "{data.repository}"
    }}"""
    result = api.ConsultaSalva(repo).execute_query_data(name=data.name, query=query)
    return result



def retrieve_queries(repo:str):
    """Recupera recursos do repositório usando paginação. [falta testar paginação]"""
    result = api.ConsultaSalva(repo).execute_query()
    return result



def update_saved_query(data: QueryModel, repo:str):
    query = f"""{{ 
      "name": "{data.name}",
      "body": "{data.body}",
      "shared": "{data.shared}",
      "owner": "{data.owner}",
      "repository": "{data.repository}"
    }}"""
    result = api.ConsultaSalva(repo).update_saved_query(name=data.name, query=query)
    return result


def delete_saved_query(name: str, repo:str):
    result = api.ConsultaSalva(repo).delete_one_saved_query(name)
    return result