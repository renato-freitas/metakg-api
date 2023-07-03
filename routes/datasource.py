from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from commons import NameSpaces as ns
from controller import datasource_controller

router = APIRouter()
TAG = "datasources" 
ROTA = f'/{TAG}/'
# PADRAO_URI = f'{ns.VSKGR}DataSource'


@router.get(ROTA, tags=[TAG])
async def read_data_sources():
    response = datasource_controller.read_resources()
    return response


@router.get(ROTA+"me", tags=[TAG])
async def read_data_source():
    return {"username": "fakecurrentuser"}


@router.get(ROTA+"{username}", tags=[TAG])
async def read_user(username: str):
    return {"username": username}


@router.post(ROTA, tags=[TAG])
async def create_data_source(data: DataSourceModel):
    """
    Cria um recurso fonte de dados do tipo drm:DataAsset.

    Propriedades da Fonte de dados:
    nome, tipo de conexão (Mysql, Postgres,), nome_host, nome_banco_dados, num_porta, nome_usuario, senha
    No Pentaho existem as Conexões que podem ser globais. 
    No MetaEKG teremos as FD.
    """
    # chamar o controller
    try:
        response = datasource_controller.create(data)
        return response
    except Exception as err:
        print('err',err)
        return err


@router.put(ROTA + "{uri}", tags=[TAG])
async def update_data_source(uri:str, data: DataSourceModel):
    """
    Atualiza um recurso fonte de dados do tipo drm:DataAsset.
    """
    try:
        print('><-><', uri)
        response = datasource_controller.update(uri, data)
        return response
    except Exception as err:
        return err


# @router.post("/datasources/record/")
# def register_data_source(data: DataSource):
#   """Por enquanto só relacional e csv"""

#   file_name = f'datasources\\{data.label.lower().replace(" ", "_")}.txt'
  
#   print(Functions.obtem_arquivos('datasources\\'))
  
#   with open(file_name, 'w') as file:
#     file.write(data.url_or_path)
#   # fonte_dados = Functions.encontraUm(f'<{NameSpaces.SEFAZMA}{data.label}>')
#   # uuid = uuid4()
#   # q = Prefixies.ALL + f"""
#   #   INSERT DATA {{
#   #   vskg:{data.label} rdf:type drm:DataAsset, <{data.type}> ; 
#   #     dc:identifier "{uuid}" ;
#   #     rdfs:label "{data.label}" ;
#   #     dc:description "{data.description}" .
#   # }}"""
  
#   # sparql = { 'query': q }
#   # headers = {'Accept': 'routerlication/x-turtle', "Content-type": "application/x-www-form-urlencoded"}

#   # r = requests.post(Endpoint.TESTE, params=sparql, headers=headers)

#   # print(r)
#   # if(r.status_code == 200):
#   #   return r.content
#   # else:
#   #   return r.content
#   return data

# @app.get("/datasources")
# def get_data_sources():
#   q = Prefixies.MOKG + "SELECT * WHERE { ?s a mokg:DataSource . } limit 10"
#   sparql = { 'query': q }
#   r = requests.get(Endpoint.METAKG, params=sparql)

#   print(r)
#   if(r.status_code == 200):
#     return r.content
#   else:
#     return r.content