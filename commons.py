import requests
import os
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
    
  def salvaFonteDeDados():
    """Salvar um arquivo .properties"""

  def obtem_arquivos(path):
    """Lista todos os arquivo de uma pasta"""
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            return file
  

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
  TESTE = "http://localhost:7200/repositories/metagraph"
  TIMELINE_TBOX = "http://localhost:7200/repositories/TIMELINE_TBOX"

class NameSpaces:
  def __init__(self): pass
  SEFAZMA = "http://www.sefaz.ma.gov.br/ontology/"
  BASE = "http://www.sefaz.ma.gov.br/resource/"

class Prefixies:
  def __init__(self): pass
  RDF = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
  RDFS = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
  OWL = "PREFIX owl: <http://www.w3.org/2002/07/owl#>\n"
  XSD = "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
  FOAF = "PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n"
  VCARD = "PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>\n"
  TL = "PREFIX tl: <http://purl.org/NET/c4dm/timeline.owl#>\n"
  MOKG = "PREFIX mokg: <http://arida.ufc/metadata-of-kg#>\n"
  VSKG = "PREFIX vskg: <http://arida.ufc/VSKG#>\n"
  DRM = "PREFIX drm: <http://vocab.data.gov/def/drm#>\n"
  SEFAZMA = "PREFIX sefazma: <http://www.sefaz.ma.gov.br/ontology/>\n"
  SFZ = "PREFIX sfz: <http://www.sefaz.ma.gov.br/ontology/>\n"
  SFZR = "PREFIX sfzr: <http://www.sefaz.ma.gov.br/resource/>\n"
  ALL = RDF + RDFS + OWL + FOAF + VCARD + XSD + TL + SFZ + SEFAZMA + SFZR + MOKG + VSKG + DRM