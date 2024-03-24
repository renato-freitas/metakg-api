from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from commons import NameSpaces as ns
from controller import datasource_controller
router = APIRouter()
TAG = "DataSources" 

# para avaliar a qualidade observar:
# Completude: de todos os registros fornecidos, qual porcentagem dos campos disponíveis tem um valor? 
# Duplicação: qual porcentagem de todos os registros são duplicados? Taxa de duplicação = [# duplicatas detectadas] / [# total de registros no conjunto de dados]
# Consistência: quão consistentes são os dados em formato e estrutura dentro e entre conjuntos de dados? 
# Cobertura: Field Coverage = [# real-world entities in the dataset] / [# real-world entities]

@router.post("/datasources/", tags=[TAG])
async def create_datasource(data: DataSourceModel):
    """
    Cria um recurso do tipo dcat:Dataset.

    Propriedades da Fonte de dados:
    nome, tipo de conexão (Mysql, Postgres,), nome_host, nome_banco_dados, num_porta, nome_usuario, senha
    No Pentaho existem as Conexões que podem ser globais. 
    No MetaEKG teremos as FD.
    """
    try:
        response = datasource_controller.create(data)
        return response
    except Exception as err:
        return err


@router.get("/datasources/", tags=[TAG])
async def read_data_sources():
    response = datasource_controller.read_resources()
    return response


@router.get("/datasources/{uri}/properties/", tags=[TAG])
async def read_properties(uri:str):
    """Obtém as propriedades de uma FD."""
    try:
        response = datasource_controller.read_properties(uri)
        # print('response ',response)
        return response
    except Exception as err:
        return err


@router.put("/datasources/{uri}", tags=[TAG])
async def update_data_source(uri:str, data: DataSourceModel):
    """
    Atualiza um recurso fonte de dados do tipo drm:DataAsset.
    """
    try:
        response = datasource_controller.update(uri, data)
        return response
    except Exception as err:
        return err


@router.delete("/datasources/{uri}", tags=[TAG])
async def delete_table(uri:str):
    """
    Apaga um recurso fonte de dados do tipo drm:DataAsset.
    """
    try:
        response = datasource_controller.delete(uri)
        return response
    except Exception as err:
        return err



    

@router.post("/datasources/{uri}/schema/", tags=[TAG])
async def add_schema_metadata(uri:str):
    """ Obter e registrar o esquema de uma fonte de dados no kg de metadados. """
    try:
        print('*** 1. router post ***')
        response = datasource_controller.add_schema_metadata(uri)
        # print('*** response',response)
        return response
    except Exception as err:
        return err


@router.get("/datasources/{uri}/schema/", tags=[TAG])
async def get_tables_schemas(uri:str):
    """ Obter o esquema de uma fonte de dados no grafo de metadados. """
    try:
        print('*** 1. router get ***')
        response = datasource_controller.read_tables_schemas(uri)
        return response
    except Exception as err:
        return err
    

@router.delete("/tables/{uri_table}", tags=[TAG])
async def delete_table(uri_table:str):
    """
    Apaga um recurso fonte de dados do tipo vskg:Table.
    """
    try:
        print('*** del table start')
        response = datasource_controller.delete(uri_table)
        return response
    except Exception as err:
        return err
    

@router.get("/datasources/tables/{uri_table}/columns/", tags=[TAG])
async def read_columns(uri_table:str):
    """ Ler colunas do tipo vskg:Column. """
    try:
        print('*** route get columns')
        response = datasource_controller.get_columns_schemas(uri_table)
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