from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, VSKG
from uuid import uuid4
from model.datasource_model import DataSourceModel
from controller import global_controller
import json
# import tboxies as file

# CLASSE = "dcat:Dataset"
# vskg_tbox = json.loads(file)



def create(data: DataSourceModel):
    uuid = uuid4()
    uri = f'{ns.META_EKG}DataSource/{uuid}'

    query = Prefixies.DATASOURCE + f"""INSERT DATA {{
        <{uri}> {VSKG.P_IS_A} {VSKG.C_DATA_SOURCE}; 
            {VSKG.P_LABEL} "{data.label}"; 
            {VSKG.P_DC_DESCRIPTION} "{data.description}";
            {VSKG.P_DATASOURCE_TYPE} "{data.type}";
        """
    
    if data.type == "http://rdbs-o#Relational_Database":
        query += f"""
            {VSKG.P_DB_CONNECTION_URL} "{data.connection_url}";    
            {VSKG.P_DB_USERNAME} "{data.username}";
            {VSKG.P_DB_PASSWORD} "{data.password}";
            {VSKG.P_DB_JDBC_DRIVER} "{data.jdbc_driver}".
        }}"""
    elif data.type == "https://www.ntnu.no/ub/ontologies/csv#CsvDocument":
        query += f"""
            {VSKG.P_CSV_FILE_PATH} "{data.csv_file}". 
        }}"""
    

    sparql = {"update": query}
    print('RDF QUE SERÁ INSERIDO', sparql)
    response = api.create_resource(sparql, VSKG.C_DATA_SOURCE, data.label)
    return response



def read_resources():

    sparql = Prefixies.DATASOURCE + f""" SELECT * WHERE {{ 
            ?uri {VSKG.P_IS_A} {VSKG.C_DATA_SOURCE};
                {VSKG.P_DATASOURCE_TYPE} ?type;
                {VSKG.P_LABEL} ?label;
                {VSKG.P_DC_DESCRIPTION} ?description.
        }}
        """
    query = {"query": sparql}
    print('CONSULTA SPARQL PARA OBTER AS FONTES DE DADOS', query)
    response = api.execute_query(query)
    return response

def update(uri:str, data:DataSourceModel):
    uri_decoded = unquote_plus(uri)
    print('como tá chegando', uri_decoded)
    existe = api.check_resource(uri_decoded) # Primeiro, pegar o recurso que existe
    if(existe is None):
        return "not found$$$"
    else:
        print('E', existe)
        query = Prefixies.DATASOURCE + f"""
            DELETE {{ 
                <{uri_decoded}> ?o ?p .
            }}
            INSERT {{
                <{uri_decoded}> {VSKG.P_IS_A} {VSKG.C_DATA_SOURCE} ; 
                    {VSKG.P_LABEL} "{data.label}"; 
                    {VSKG.P_DC_DESCRIPTION} "{data.description}";
                    {VSKG.P_DATASOURCE_TYPE} "{data.type}";
        """

        if data.type == "http://rdbs-o#Relational_Database":
            query += f"""
                {VSKG.P_DB_CONNECTION_URL} "{data.connection_url}";    
                {VSKG.P_DB_USERNAME} "{data.username}";
                {VSKG.P_DB_PASSWORD} "{data.password}";
                {VSKG.P_DB_JDBC_DRIVER} "{data.jdbc_driver}".
            """
        elif data.type == "https://www.ntnu.no/ub/ontologies/csv#CsvDocument":
            query += f"""
                {VSKG.P_CSV_FILE_PATH} "{data.csv_file}". 
            """
        query += f"""}}
                WHERE {{
                    <{uri_decoded}> ?o ?p .
                }}"""
        print('',query)
        sparql = {"update": query}

        # Chamar a API
        response = api.update_resource(sparql)
        return response


def delete(uri:str):
    uri_decoded = unquote_plus(uri)
    
    existe = api.check_resource(uri_decoded) # Primeiro, pegar o recurso que existe
    if(existe is None):
        return "not found"
    else:
        print('E', existe)
        query = Prefixies.DATASOURCE + f"""
            DELETE WHERE {{ 
                <{uri_decoded}> ?o ?p .
            }}
        """
        print('',query)
        sparql = {"update": query}

        response = api.update_resource(sparql)
        return response


# def check_resource(uri:str):
#     sparql = Prefixies.DATASOURCE + f""" select * where {{ 
#             <{uri}> ?p ?o.
#         }} limit 1
#         """
#     print('sparql, ', sparql)
#     query = {"query": sparql}
#     response = api.read_resource(query)
#     return response

# $ java -jar r2rml.jar --connectionURL jdbc:mysql://localhost/r2rml \
#   --user foo --password bar \
#   --mappingFile mapping.ttl \
#   --outputFile output.ttl \
#   --format TURTLE