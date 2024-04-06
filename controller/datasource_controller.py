from urllib.parse import unquote_plus
import api
from commons import NameSpaces as ns, Prefixies, VSKG, EndpointDEV, NamedGraph
from uuid import uuid4
from model.datasource_model import DataSourceModel, TableQualityModel
import pandas as pd

def create(data: DataSourceModel):
    uuid = uuid4()
    uri = f'{ns.META_EKG}DataSource/{uuid}'

    query = Prefixies.DATASOURCE + f"""INSERT DATA {{
        <{NamedGraph.KG_METADATA}> {{
        <{uri}> {VSKG.P_IS_A} {VSKG.C_DATA_SOURCE}; 
            {VSKG.P_LABEL} "{data.label}"; 
            {VSKG.P_NAME} "{data.name}"; 
            {VSKG.P_DC_DESCRIPTION} "{data.description}";
            {VSKG.P_DATASOURCE_TYPE} "{data.type}";
        """
    
    if data.type == VSKG.C_RDB :
        query += f"""
            {VSKG.P_DB_CONNECTION_URL} "{data.connection_url}";    
            {VSKG.P_DB_USERNAME} "{data.username}";
            {VSKG.P_DB_PASSWORD} "{data.password}";
            {VSKG.P_DB_JDBC_DRIVER} "{data.jdbc_driver}".
        }}
        }}"""
    elif data.type == VSKG.C_CSV_FILE:
        query += f"""
            {VSKG.P_CSV_FILE_PATH} "{data.csv_file}". 
        }}
        }}"""

    sparql = {"update": query}
    print('*** RDF QUE SERÁ INSERIDO', sparql)
    response = api.create_resource_kg_metadata(sparql, VSKG.C_DATA_SOURCE, data.label)
    return response


def read_data_sources():
    print('*** CONTROLLER, read data sources')
    sparql = Prefixies.DATASOURCE + f"""SELECT * FROM <{NamedGraph.KG_METADATA}> {{ 
        ?uri {VSKG.P_IS_A} {VSKG.C_DATA_SOURCE};
            {VSKG.P_DATASOURCE_TYPE} ?type;
            {VSKG.P_LABEL} ?label;
            {VSKG.P_DC_DESCRIPTION} ?description.
    }}"""
    query = {"query": sparql}
    print('*** CONTROLLER, sparql data sources', query['query'])
    response = api.execute_query_on_kg_metadata(query)
    return response


def update(uri:str, data:DataSourceModel):
    uri_decoded = unquote_plus(uri)
    print('*** como tá chegando', uri_decoded)
    existe = api.check_resource_in_kg_metadata(uri_decoded) # Primeiro, pegar o recurso que existe
    if(existe is None):
        return "not found$$$"
    else:
        print('*** existe', existe)
        query = Prefixies.DATASOURCE + f"""
            DELETE {{ 
                GRAPH <{NamedGraph.KG_METADATA}> {{
                    <{uri_decoded}> ?o ?p .
                }}
            }}
            INSERT {{
                GRAPH <{NamedGraph.KG_METADATA}> {{
                    <{uri_decoded}> {VSKG.P_IS_A} {VSKG.C_DATA_SOURCE} ; 
                        {VSKG.P_LABEL} "{data.label}"; 
                        {VSKG.P_DC_DESCRIPTION} "{data.description}";
                        {VSKG.P_DATASOURCE_TYPE} "{data.type}";  
        """

        if data.type == "http://rdbs-o#Relational_Database":
            query += f"""
                {VSKG.P_NAME} "{data.name}";    
                {VSKG.P_DB_CONNECTION_URL} "{data.connection_url}";    
                {VSKG.P_DB_USERNAME} "{data.username}";
                {VSKG.P_DB_PASSWORD} "{data.password}";
                {VSKG.P_DB_JDBC_DRIVER} "{data.jdbc_driver}".
            """
        elif data.type == "https://www.ntnu.no/ub/ontologies/csv#CsvDocument":
            query += f"""
                {VSKG.P_NAME} "{data.name}";    
                {VSKG.P_CSV_FILE_PATH} "{data.csv_file}". 
            """
        query += f"""}} }}
            WHERE {{
                GRAPH <{NamedGraph.KG_METADATA}> {{
                    <{uri_decoded}> ?o ?p .
                }}
            }}"""
        print('',query)
        sparql = {"update": query}

        # Chamar a API
        response = api.update_resource_kg_metadata(sparql)
        return response


def delete(uri:str):
    uri_decoded = unquote_plus(uri)
    
    existe = api.check_resource_in_kg_metadata(uri_decoded) # Primeiro, pegar o recurso que existe
    if(existe is None):
        return "not found"
    else:
        print('*** del existe', existe)
        query = Prefixies.DATASOURCE + f"""DELETE WHERE {{ GRAPH <{NamedGraph.KG_METADATA}> {{
                <{uri_decoded}> ?o ?p .
                }}
            }}
        """
        print('',query)
        sparql = {"update": query}

        response = api.update_resource_kg_metadata(sparql)
        return response

def read_properties(uri:str):
    print('*** CONTROLLER, read data source properties')
    uri_decoded = unquote_plus(uri)
    existe = api.check_resource_in_kg_metadata(uri_decoded) 
    if(existe is None):
        return "not found"
    else:
        response = api.get_properties_kg_metadata(uri_decoded)
        return response


# METADADOS DO ESQUEMA DA FONTE DE DADOS
def add_schema_metadata(uri:str):
    print('*** 2. controller add ***')
    uri_decoded = unquote_plus(uri)
    existe = api.check_resource_in_kg_metadata(uri_decoded)
    if(existe is None):
        return "not found"
    else:
        props = api.get_properties_kg_metadata(uri_decoded) # para saber qual o tipo da fonte de dados
        _datasourceType, db_name, db_username, db_password, db_jdbc_driver, db_conn_url = "","","","","",""
        for p in props:
            if p['o']['value'] == VSKG.C_RDB: 
                _datasourceType = VSKG.C_RDB
            elif p['o']['value'] == VSKG.C_CSV_FILE: 
                _datasourceType = VSKG.C_CSV_FILE
            elif p['p']['value'] == 'http://xmlns.com/foaf/0.1/name': 
                db_name = p['o']['value']
            elif p['p']['value'] == 'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#username':
                db_username = p['o']['value']
            elif p['p']['value'] == 'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#password':
                db_password = p['o']['value']
            elif p['p']['value'] == 'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#jdbcDriver':
                db_jdbc_driver = p['o']['value']
            elif p['p']['value'] == 'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#jdbcDSN':
                db_conn_url = p['o']['value']
        if _datasourceType == VSKG.C_RDB:
            schema = api.get_schema_from_datasource(db_conn_url, db_name, db_username, db_password)
            if (schema):
                createdTables = create_datasource_schema_in_kg_metadata(uri_decoded, schema)
        return createdTables
        # return "createdTables"


def read_tables_schemas(uri:str):
    """
    - PARAMS: uri = URI encoded
    """
    print('*** CONTROLLER, READ TABLES SCHEMAS')
    uri_datasource_decoded = unquote_plus(uri)
    existe = api.check_resource_in_kg_metadata(uri_datasource_decoded)
    if(existe is None):
        return "not found"
    else:
        sparql = Prefixies.DATASOURCE + f""" SELECT * FROM <{NamedGraph.KG_METADATA}> {{ 
            <{uri_datasource_decoded}> {VSKG.P_DB_HAS_TABLE} ?uri.
            ?uri {VSKG.P_LABEL} ?label.
        }}
        """
        query = {"query": sparql}
        print('*** query', sparql)
        response = api.execute_query_on_kg_metadata(query)
        return response
         

def create_datasource_schema_in_kg_metadata(datasource, schema):
    _sparql = Prefixies.DATASOURCE + "\n"
    _sparql_columns = ""
    _sparql_has_table = ""
    for table, cols in schema.items():
        uuid = uuid4()
        uri_table = f'{ns.META_EKG}Table/{uuid}'
        
        _sparql_has_table += f"""<{datasource}> {VSKG.P_DB_HAS_TABLE} <{uri_table}>.\n"""
        _sparql += f"""<{uri_table}> {VSKG.P_IS_A} {VSKG.C_RDB_TABLE}; 
            {VSKG.P_LABEL} "{table}";
            {VSKG.P_DB_HAS_COLUMN}"""
        
        count = 0
        for col_name, col_type, col_nullabel, col_cardinality in cols:
            count += 1
            uuid_col = uuid4()
            uri_col = f'{ns.META_EKG}Column/{uuid_col}'
            pointOrComma = '.' if count == len(cols) else ','
            _sparql += f""" <{uri_col}>{pointOrComma}"""
            _sparql_columns += f"""<{uri_col}> {VSKG.P_IS_A} {VSKG.C_RDB_COLUMN};
                {VSKG.P_LABEL} "{col_name}";
                {VSKG.P_DB_COL_DATATYPE} "{col_type}";
                {VSKG.P_DB_COL_NULLABLE} "{col_nullabel}";
                {VSKG.P_DB_COL_CARDINALITY} "{col_cardinality}".
            """
        _sparql += "\n"
    _sparql += _sparql_columns
    _sparql += _sparql_has_table
    # _sparql += "\t}\n}"

    print('query\n', _sparql)
    # _query = {'update':_sparql}
    response = api.KG_Metadata().add_rdf(rdf=_sparql)
    print('*** execute statement *** ',response)
    if response:
        return read_tables_schemas(datasource)




def get_columns_schemas(uri_table:str):
    print('*** controller - read schemas***', uri_table)
    uri_table_decoded = unquote_plus(uri_table)
    existe = api.check_resource_in_kg_metadata(uri_table_decoded)
    if(existe is None):
        return "not found"
    else:
        sparql = Prefixies.DATASOURCE + f""" SELECT * FROM <{NamedGraph.KG_METADATA}> {{ 
            <{uri_table_decoded}> {VSKG.P_DB_HAS_COLUMN} ?o.
            ?o            {VSKG.P_LABEL} ?label.
        }}
        """
        query = {"query": sparql}
        print('*** query', query)
        response = api.execute_query_on_kg_metadata(query)
        return response






def quality_datasource(uri_datasource:str):
    uri_datasource_decoded = unquote_plus(uri_datasource)
    print('*** CONTROLLER, QUALITA DATA SOURCE ***', uri_datasource_decoded)
    existe = api.check_resource_in_kg_metadata(uri_datasource_decoded) # Primeiro, pegar o recurso que existe
    print('*** CONTROLLER, EXISTE ***', existe)
    if(existe is None or len(existe) > 0):
        print('*** recurso existe:', existe)
        db_name, db_username, db_password, db_jdbc_driver, db_conn_url = api.RDB().get_credentials(uri_datasource_decoded)


        # OBTER AS TABELAS DA FONTE DE DADOS
        tables = read_tables_schemas(uri_datasource)
        print('*** CONTROLLER, TABLES ****', tables)

        # OBTER OS DADOS DA 1ª TABELA - TESTANDO
        table_2 = tables[1]
        
        return db_conn_url, db_name, db_username, db_password
    else:
        print('não existe')
        






# $ java -jar r2rml.jar --connectionURL jdbc:mysql://localhost/r2rml \
#   --user foo --password bar \
#   --mappingFile mapping.ttl \
#   --outputFile output.ttl \
#   --format TURTLE