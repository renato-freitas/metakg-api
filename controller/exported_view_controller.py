import os
import platform
from urllib.parse import quote_plus, unquote_plus
import api
from commons import NameSpaces as ns, Functions, Prefixies, Ontology as o, OperationalSystem
from uuid import uuid4
from model.exported_view_model import ExportedViewModel

CLASSE = o.C_EXPORTED_VIEW

def create(data: ExportedViewModel):
    uuid = uuid4()
    uri = f'{ns.META_EKG}ExportedView/{uuid}'

    query = Prefixies.DATASOURCE + f"""INSERT DATA {{
        <{uri}> rdf:type {CLASSE}; 
            rdfs:label "{data.label}";
            dc:description "{data.description}";
            vskg:hasDataSource <{data.hasDataSource}>;
            vskg:hasMappings <{data.hasMappings}>;
            vskg:hasLocalOntology <{data.hasLocalOntology}>.
        }}"""
    sparql = {"update": query}

    response = api.create_resource(sparql, CLASSE, data.label)
    return response


def update(uri:str, data:ExportedViewModel):
    uri_decoded = unquote_plus(uri)
    
    existe = check_resource(uri_decoded) # Primeiro, pegar o recurso que existe
    if(existe is None):
        return "not found"
    else:
        print('E', existe)
        query = Prefixies.EXPORTED_VIEW + f"""
            DELETE {{ 
                <{uri_decoded}> ?o ?p .
            }}
            INSERT {{
                <{uri_decoded}> rdf:type {CLASSE} ; 
                    rdfs:label "{data.label}"; 
                     dc:description "{data.description}";
                    vskg:hasDataSource <{data.hasDataSource}>;
                    vskg:hasMappings <{data.hasMappings}>;
                    vskg:hasLocalOntology <{data.hasLocalOntology}>.
            }}
            WHERE {{
                <{uri_decoded}> ?o ?p .
            }}
        """
        print('',query)
        sparql = {"update": query}

        # Chamar a API
        response = api.update_resource(sparql)
        return response


def read_resources():
    sparql = Prefixies.EXPORTED_VIEW + f""" select * where {{ 
            ?s rdf:type {CLASSE};
               rdfs:label ?l.
        }} limit 100 
        """
    query = {"query": sparql}

    response = api.read_resources(query)
    return response


def check_resource(uri:str):
    sparql = Prefixies.EXPORTED_VIEW + f""" select * where {{ 
            <{uri}> ?p ?o.
        }} limit 1
        """
    query = {"query": sparql}
    response = api.read_resource(query)
    return response


def materialize(visao_exportada):
    """Essa função considera que o arquivo RML já existe"""
    uri_decoded = unquote_plus(visao_exportada)
    existe = check_resource(uri_decoded) # 1. verificar se a visão exportada existe.
    if(existe is None):
        return "not found"
    else:
        ev = api.ExportedView()
        response = ev.get_datasource_properties(uri_decoded) # 2. trazer os dados de acesso à fonte.
        # print('get get', response[0])
        propriedade_para_str_triplificacao = response[0]
        file_path_witH_separator_slash = str(propriedade_para_str_triplificacao['f']['value']).replace('/', os.sep)
        # str_materializacao = f"java -jar r2rml.jar --connectionURL {propriedade_para_str_triplificacao['conn']['value']} --user {propriedade_para_str_triplificacao['un']['value']} --password {propriedade_para_str_triplificacao['pwd']['value']} --mappingFile {file_path_witH_separator_slash} --outputFile output.ttl --format TURTLE"
        # print('**str_materializacao', str_materializacao)

        # 3. Adicionar o código que define o acesso ao BD ao arquivo de mapeamento RML.IO
        code = Functions.construct_rml_code_db_credentials(propriedade_para_str_triplificacao['conn']['value'],
                                             propriedade_para_str_triplificacao['jdbc_driver']['value'],
                                             propriedade_para_str_triplificacao['un']['value'],
                                             propriedade_para_str_triplificacao['pwd']['value'])
        # print('code rml.io', code)
        
        operational_system = platform.system()
        r = 'responsta'
        if(operational_system == OperationalSystem.WINDOWS):
            # r = os.system(".\\d2rq-dev\\dump-rdf.bat -u ufc_sem -p ufcsemantic22_ -f N-TRIPLE -j jdbc:oracle:thin:@10.1.1.188:1521/bigsem.sefaz.ma.gov.br C:\\Users\\Adm\\ldif-0.5.2\\gcl\\mappings\\map-rfb-old-maranhao.ttl > C:\\Users\\Adm\\graphdb-import\\can-delete-this.nt")
            r = os.system("java -jar .\\tools\\rmlmapper-6.2.0-r368-all.jar -m .\\mappings\\map-fno.ttl -o .\\aboxies\\teste-fno-01.ttl -s turtle")
            return r
        elif operational_system == OperationalSystem.LINUX:
            r = os.system("ls -a")
            return r
