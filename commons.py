import os
import requests
from unidecode import unidecode
from models import DataSource, HighLevelMapping, DataProperty

ENVIROMENT:str = "DEV"
EKG:str = "EKG_CONTEXT"
class TEXTS:  
  def __init__(self): pass
  GENERALIZATION = "0"
  EXPORTED = "1"
  METADATA = "2"

  
def transforma_basemodel_em_json(p):
  return dict(p)

class Functions:
  def __init__(self): pass

  def encontraUm(uri, classe):
    q = Prefixies.ALL + f"""SELECT * WHERE {{ 
      {uri} a {classe}
    }}"""
    sparql = { 'query': q }
    r = requests.get(Endpoint.TIMELINE_TBOX, params=sparql)
    if(r.status_code == 200):
      return r.text
    else:
      return 404
  
  def verifica_uri_existe(uri:str):
    q = f"""SELECT * WHERE {{ {uri} ?p ?o . }}"""
    r = requests.get(Endpoint.METAKG, params={ 'query': q })
    return True if r.status_code == 200 else False
    
  def salvaFonteDeDados():
    """Salvar um arquivo .properties"""

  def obtem_arquivos(path):
    """Lista todos os arquivo de uma pasta"""
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            return file
        
  def removeAcentosEAdicionaUnderscore(rotulo:str = ""):
    """Usado para transformar o nome do recurso que será usado para montar a URI.
    Remove os acentos e substitui espaço por underscore
    Ex: até amanhã -> ate_amanha"""
    return unidecode(rotulo).replace(" ", "_")

  
  

  def create_high_level_mapping(data: HighLevelMapping):
    file_name = f'mappings\\{data.table_or_file_name}.py'
    with open(file_name, 'w') as file:
      txt = f"""{{
      'nome': '{data.table_or_file_name}',
      'uri': '{data.uri}',
      'chaves': {data.keys},
      'tipos': {data.types},
      'propriedade_de_dados': {list(map(transforma_basemodel_em_json, data.data_properties))},
      'propriedade_de_objeto': {list(map(transforma_basemodel_em_json, data.object_properties))}\n}}"""
      file.write(txt)


  

class RMLConstructs:
  def __init__(self): pass

  def construct_rml_prefixies(mapping_prefixies):
    return f"""{mapping_prefixies}
  @prefix rml: <http://semweb.mmlab.be/ns/rml#> .
  @prefix d2rq: <http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#> .
  @prefix ql: <http://semweb.mmlab.be/ns/ql#> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
  @prefix csvw: <http://www.w3.org/ns/csvw#> .
  @prefix fnml: <http://semweb.mmlab.be/ns/fnml#> .
  @prefix fno: <https://w3id.org/function/ontology#> .
  @prefix grel: <http://users.ugent.be/~bjdmeest/function/grel.ttl#> .
  @base <http://arida.ufc.br/meta-ekg/resource> ."""

  def construct_rml_source(conn, jdbc_driver, username, password):
    """Constrói o trecho com as credencias do BD"""
    return f"""<#DB_source> a d2rq:Database;
    d2rq:jdbcDSN "{conn}";
    d2rq:jdbcDriver "{jdbc_driver}";
    d2rq:username "{username}";
    d2rq:password "{password}"."""
  
  def construct_rml_logical_source(tableName, sqlQuery):
    return f"""<#LogicalSource> a rml:LogicalSource;
    rml:source <#DB_source>;
    rr:sqlVersion rr:SQL2008;
    rr:tableName "{tableName}"; 
    rml:query "\"\"{sqlQuery}\"\"";
    rml:referenceFormulation ql:CSV."""
  
  def construct_rml_subject(template, classe):
    return f"""rr:subjectMap [
        rr:template {template};
        rr:class <{classe}>
    ];"""


  def construct_rml_datatype_or_object_property(props):
    print('', props)
    last_key = list(props) [-1]
    _props = ""
    for k in props:
      print(k, props[k])
      if(props[k][1] == "DatatypeProperty"):
        _props += f"""rr:predicateObjectMap [
       rr:predicate <{props[k][2]}> ;
       rr:objectMap [ rml:reference "{k}" ]
    ]"""
      else:
        _props += f""""""
      _props += "." if k == last_key else ";\n\t"
    return _props
  
  

  def construct_rml_triple_map(subject, properties):
    return f"""<#MyTriplesMap> a rr:TriplesMap;
    rml:logicalSource <#LogicalSource>;
    {subject}
    {properties}
    """


class OperationalSystem:
  def __init__(self): pass
  WINDOWS = "Windows"
  LINUX = "Linux"

class Endpoint:
  def __init__(self): pass
  NAME = "GRAFO_PRODUCAO_BIGSEMFORTALEZA"
  REPOSITORIES = "http://localhost:7200/repositories/metagraph"
  PRODUCTION = f"http://localhost:7200/repositories/{NAME}"
  METAKG = "http://localhost:7200/repositories/metagraph"
  TIMELINE_TBOX = "http://localhost:7200/repositories/TIMELINE_TBOX"
  SEFAZMA_VEKG_ABOX = "http://10.33.96.18:7200/repositories/VEKG"
  VSKG_ABOX = "http://localhost:7200/repositories/VSKG_ABOX" # só pra testar pegando os metaEKG
  METADADOS_TULIO = "http://localhost:7200/repositories/Metadados_Tulio"


class EndpointDEV:
  def __init__(self, repo:str=None):
    # self.name = name
    self.PRODUCTION = f"http://localhost:7200/repositories/{repo}"
    self.REPOSITORIES = "http://localhost:7200/repositories"
  NAME = "GRAFO_PRODUCAO_BIGSEMFORTALEZA"
  # NAME = "EKG_CONTEXT"
  # ONTOLOGIA_DOMINIO = "http://localhost:7200/repositories/metagraph"
  METAKG = "http://localhost:7200/repositories/metagraph"
  # REPOSITORIES = f"http://localhost:7200/repositories"
  # PRODUCTION = f"http://localhost:7200/repositories/{NAME}"
  TIMELINE_TBOX = "http://localhost:7200/repositories/TIMELINE_TBOX"
  SEFAZMA_VEKG_ABOX = "http://10.33.96.18:7200/repositories/VEKG"
  VSKG_ABOX = "http://localhost:7200/repositories/VSKG_ABOX" # só pra testar pegando os metaEKG
  METADADOS_TULIO = "http://localhost:7200/repositories/Metadados_Tulio"
  
  ONTOLOGIA_DOMINIO = f"http://localhost:7200/repositories/{NAME}"
  RESOURCES = f"http://localhost:7200/repositories/{NAME}"
  GRAPHDB_BROWSER = "http://localhost:7200/graphs-visualizations"
  GRAPHDB_BROWSER_CONFIG = "&config=63b76b9865064cd8a9775e1e2f46ff4d"
  ENDPOINT_HISTORY = "http://localhost:7200/repositories/{NAME}"
  USE_N_ARY_RELATIONS = False
  USE_LABELS = True #Set True to get labels for resources. When querying virtual repositories maybe be better set to False
  # HIGHLIGHT_CLASSES = ['http://xmlns.com/foaf/0.1/Organization','http://www.sefaz.ma.gov.br/ontology/Estabelecimento', 'http://xmlns.com/foaf/0.1/Person', 'http://www.sefaz.ma.gov.br/ontology/Sociedade'] #A list with URIs of highlighted classes
  HIGHLIGHT_CLASSES = ['http://www.bigdatafortaleza.com/ontology#Crianca_de_0_a_3_anos']


class NamedGraph:
  def __init__(self, repo:str):
    self.repo = repo
    self.IP = "localhost"
    self.PORT = "7200"
    self.TBOX = f"http://{self.IP}:{self.PORT}/repositories/{repo}/rdf-graphs/TBOX"
    self.REPOSITORY_ID = "GRAFO_PRODUCAO_BIGDATAFORTALEZA"
    # REPOSITORY_ID = "EKG_CONTEXT"
    self.TBOX = f"http://{self.IP}:{self.PORT}/repositories/{repo}/rdf-graphs/TBOX"
    self.TBOX_METADATA = f"http://{self.IP}:{self.PORT}/repositories/{repo}/rdf-graphs/TBOX_METADATA"
    self.KG_METADATA = f"http://{self.IP}:{self.PORT}/repositories/{repo}/rdf-graphs/KG_METADATA"
  # KG_TBOX = "http://www.sefaz.ma.gov.br/named-graph/TBOX"
  # KG_METADATA_BIGDATAFORTALEZA = f"http://{IP}:{PORT}/repositories/{REPOSITORY_ID}/rdf-graphs/KG_METADATA"
  # KG_TBOX_BIGDATAFORTALEZA = f"http://{IP}:{PORT}/repositories/{REPOSITORY_ID}/rdf-graphS/KG_TBOX"


class NameSpaces:
  def __init__(self): pass
  SEFAZMA = "http://www.sefaz.ma.gov.br/ontology/"
  BASE = "http://www.sefaz.ma.gov.br/resource/"
  VSKG = "http://www.arida.ufc.br/VSKG/"
  VSKGR = "http://www.arida.ufc.br/VSKG/resource/"
  META_EKG = "http://www.arida.ufc.br/meta-ekg/resource/"
  D2RQ = "http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#"

class Prefixies:
  def __init__(self): pass
  RDF = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
  RDFS = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
  OWL = "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
  FOAF = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n"
  VCARD = "PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>\n"
  D2RQ = "PREFIX d2rq: <http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#>\n"
  XSD = "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
  DC = "PREFIX dc: <http://purl.org/dc/elements/1.1/>\n"
  DC_TERMS = "PREFIX dcterms: <http://purl.org/dc/terms/>\n"
  RR = "PREFIX rr: <http://www.w3.org/ns/r2rml#>\n"
  VOID = "PREFIX void: <http://rdfs.org/ns/void#>\n"
  DRM = "PREFIX drm: <http://vocab.data.gov/def/drm#>\n"
  DCAT = "PREFIX dcat: <http://www.w3.org/ns/dcat#>\n"
  TL = "PREFIX tl: <http://purl.org/NET/c4dm/timeline.owl#>\n"
  VSKG = "PREFIX vskg: <http://www.arida.ufc.br/VSKG#>\n"
  MOKG = "PREFIX mokg: <http://www.arida.ufc.br/metadata-of-knowledge-graph#>\n"
  SEFAZMA = "PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>\n"
  SFZ = "PREFIX sfz: <http://www.sefaz.ma.gov.br/ontology/>\n"
  SFZR = "PREFIX sfzr: <http://www.sefaz.ma.gov.br/resource/>\n"
  RFB = "PREFIX rfb: <http://www.sefaz.ma.gov.br/RFB/ontology/>\n"
  META_EKG = "PREFIX metaekg: <http://www.arida.ufc.br/meta-ekg/resource/>\n"
  ALL = RDF + RDFS + OWL + FOAF + VCARD + D2RQ + XSD + DC + DC_TERMS + RR + VOID + DCAT + DRM + TL + VSKG + SFZ + SEFAZMA + SFZR + MOKG 
  DATASOURCE = RDF + RDFS + VSKG + DCAT + DRM +  D2RQ + DC + FOAF + DC_TERMS
  EXPORTED_VIEW = RDF + RDFS + VSKG + DRM + DC
  MAPPING = RDF + RDFS + DC + VSKG + META_EKG
  META_MASHUP = RDF + RDFS + DC + META_EKG + VSKG

  

class Headers:
  def __init__(self): pass
  GET = { "Accept": "application/sparql-results+json" }
  GET_JSON = { "Accept": "application/json" }
  POST = { "Content-type": "application/rdf+xml", "Accept": "application/json" }
  POST_KG_METADATA = { "Content-type": "text/turtle", "Accept": "application/json" }

class RoutesPath:
  def __init__(self): pass
  META_MASHUP = "/meta-mashup"
  META_EKG = "/meta-ekg"

class VSKG:
  def __init__(self): pass
  """Mantém as classes e propriedades da ontologia VSKG"""

  P_IS_A = "rdf:type"
  P_LABEL = "rdfs:label"
  P_NAME = "foaf:name"
  P_DOMAIN = "rdfs:domain"
  P_RANGE = "rdfs:range"
  P_DC_IDENTIFIER = "dc:identifier"
  P_COMMENT = "rdfs:comment"
  P_DC_DESCRIPTION = "dc:description"
  P_DCTERMS_DESCRIPTION = "dcterms:description"
  P_HAS_APPLICATION = "vskg:hasApplication"
  # FONTE DE DADOS
  P_DATASOURCE_TYPE = "vskg:datasourceType"
  P_DB_USERNAME = "d2rq:username"
  P_DB_PASSWORD = "d2rq:password"
  P_DB_JDBC_DRIVER = "d2rq:jdbcDriver"
  P_DB_CONNECTION_URL = "d2rq:jdbcDSN"
  P_CSV_FILE_PATH = "vskg:csvFilePath"
  P_DB_HAS_TABLE = "vskg:hasTable"
  P_DB_HAS_COLUMN = "vskg:hasColumn"
  P_DB_COL_DATATYPE = "vskg:datatype"
  P_DB_COL_NULLABLE = "vskg:nullable"
  P_DB_COL_CARDINALITY = "vskg:cardinality"
  # META-MASHUP
  P_MASHU_CLASS = "vskg:mashupClass" 
  P_META_MASHUP_EXPORTED_VIEW_URI = "vskg:exportedViewURI"
  P_META_MASHUP_LOCAL_ONTOLOGY_CLASS = "vskg:localOntologyClass"
  P_META_MASHUP_SQP_COLUMN = "vskg:sqpCol"


  #====================
  C_META_EKG = "vskg:MetadataGraphEKG"
  C_DATA_SOURCE = "dcat:Dataset"
  C_DATA_ASSET = "drm:DataAsset"
  C_RDB = "http://rdbs-o#Relational_Database"
  C_RDB_TABLE = "vskg:Table"
  C_RDB_COLUMN = "vskg:Column"
  C_CSV_FILE = "https://www.ntnu.no/ub/ontologies/csv#CsvDocument"
  C_EXPORTED_VIEW = "vskg:LocalGraph"
  
  C_META_MASHUP = "vskg:MetadataGraphMashup"
  C_MASHUP_VIEW_SPEC = "vskg:MashupViewSpecification"
  C_META_MASHUP_SPARQL_QUERY_PARAMS = "vskg:SparqlQueryParams"
  C_META_MASHUP_SPARQL_QUERY_PARAMS = "vskg:SparqlQueryParams"
  