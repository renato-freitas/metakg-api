import os
import requests
from unidecode import unidecode
from models import DataSource, HighLevelMapping, DataProperty

  
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


class Endpoint:
  def __init__(self): pass
  METAKG = "http://localhost:7200/repositories/metagraph"
  TIMELINE_TBOX = "http://localhost:7200/repositories/TIMELINE_TBOX"
  SEFAZMA_VEKG_ABOX = "http://10.33.96.18:7200/repositories/VEKG"
  VSKG_ABOX = "http://localhost:7200/repositories/VSKG_ABOX" # só pra testar pegando os metaEKG
  METADADOS_TULIO = "http://localhost:7200/repositories/Metadados_Tulio"

class NameSpaces:
  def __init__(self): pass
  SEFAZMA = "http://www.sefaz.ma.gov.br/ontology/"
  BASE = "http://www.sefaz.ma.gov.br/resource/"
  VSKG = "http://www.arida.ufc.br/VSKG/"
  VSKGR = "http://www.arida.ufc.br/VSKG/resource/"
  META_EKG = "http://www.arida.ufc.br/meta-ekg/resource/"

class Prefixies:
  def __init__(self): pass
  RDF = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
  RDFS = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
  OWL = "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
  XSD = "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
  FOAF = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n"
  VCARD = "PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>\n"
  DC = "PREFIX dc: <http://purl.org/dc/elements/1.1/>\n"
  DC_TERMS = "PREFIX dcterms: <http://purl.org/dc/terms/>\n"
  TL = "PREFIX tl: <http://purl.org/NET/c4dm/timeline.owl#>\n"
  MOKG = "PREFIX mokg: <http://www.arida.ufc.br/metadata-of-knowledge-graph#>\n"
  VSKG = "PREFIX vskg: <http://www.arida.ufc.br/VSKG/>\n"
  VSKGR = "PREFIX vskgr: <http://www.arida.ufc.br/VSKG/resource/>\n"
  DRM = "PREFIX drm: <http://vocab.data.gov/def/drm#>\n"
  SEFAZMA = "PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>\n"
  SFZ = "PREFIX sfz: <http://www.sefaz.ma.gov.br/ontology/>\n"
  SFZR = "PREFIX sfzr: <http://www.sefaz.ma.gov.br/resource/>\n"
  META_EKG = "PREFIX metaekg: <http://www.arida.ufc.br/meta-ekg/>\n"
  ALL = RDF + RDFS + OWL + FOAF + VCARD + XSD + DC + DC_TERMS + TL + SFZ + SEFAZMA + SFZR + MOKG + VSKG + VSKGR + DRM
  DATASOURCE = RDF + RDFS + VSKG + DRM + DC
  EXPORTED_VIEW = RDF + RDFS + VSKG + DRM + DC
  MAPPING = RDF + RDFS + DC + VSKG + META_EKG

class Headers:
  def __init__(self): pass
  GET = { "Accept": "application/sparql-results+json" }
  POST = { "Content-type": "application/rdf+xml", "Accept": "application/json" }

class RoutesPath:
  def __init__(self): pass
  META_MASHUP = "/meta-mashup"
  META_EKG = "/meta-ekg"

class Ontology:
  def __init__(self): pass
  """Mantém as classes e propriedades da ontologia VSKG"""
  P_TYPE = "rdf:type"
  P_LABEL = "rdfs:label"
  P_DOMAIN = "rdfs:domain"
  P_RANGE = "rdfs:range"
  P_DC_IDENTIFIER = "dc:identifier"
  P_DC_DESCRIPTION = "dc:description"
  P_HAS_APPLICATION = "vskg:hasApplication"

  C_META_EKG = "vskg:MetadataGraphEKG"
  # C_META_EKG = "vskg:MetadataGraphEKG"
  C_META_MASHUP = "vskg:MetadataGraphMashup"
  C_MASHUP_VIEW_SPEC = "vskg:MashupViewSpecification"
  C_DATA_ASSET = "drm:DataAsset"
  C_EXPORTED_VIEW = "vskg:LocalGraph"