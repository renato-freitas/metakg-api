import uuid
import requests
# from unidecode import unidecode
from commons import Prefixies, NameSpaces as ns, Endpoint, Headers, Functions, Ontology as o
from models import DataSource, MetaMashupModel, HighLevelMapping, DataProperty, AddGCLMashupModel, AssociaMetaEKGAoMetaMashupModel

def create_resource(sparql, classe, label):
    try:
        # verificar se o recurso já existe pela URI (genérico)
        existe = obtem_recurso(classe, label)
        if (len(existe) > 0):
            return {"code": 409, "message": "Um recurso dessa classe com essa label já existe!"}

        
        r = requests.post(Endpoint.METAKG + "/statements", params=sparql, headers=Headers.POST)
        print('response', r)
        if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
            return {"code": 204, "message": "Criado com Sucesso!"}
        else:
            return {"code": 400, "message": "Não foi criado!"}
    except Exception as err:
        return err

def update_resource(sparql):
    try:
        r = requests.post(Endpoint.METAKG + "/statements", params=sparql, headers=Headers.POST)
        print('response', r)
        if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
            return {"code": 204, "message": "Criado com Sucesso!"}
        else:
            return {"code": 400, "message": "Não foi criado!"}
    except Exception as err:
        return err

def obtem_recurso(classe:str, label:str):
    try:
        q = Prefixies.ALL + \
            f"""SELECT DISTINCT ?l WHERE {{ ?s a {classe}; rdfs:label "{label}". }}"""
        sparql = {'query': q}
        r = requests.get(Endpoint.METAKG, params=sparql, headers=Headers.GET)
        return r.json()['results']['bindings']
    except Exception as err:
        return err
    
def read_resources(query):
    try:
        r = requests.get(Endpoint.METAKG, params=query, headers=Headers.GET)
        return r.json()['results']['bindings']
    except Exception as err:
        return err

def read_resource(query):
    try:
        r = requests.get(Endpoint.METAKG, params=query, headers=Headers.GET)
        return r.json()['results']['bindings']
    except Exception as err:
        return err


def delete_resourde(query):
    try:
        r = requests.post(Endpoint.METAKG, params=query, headers=Headers.GET)
        return r.json()['results']['bindings']
    except Exception as err:
        return err

def get_properties(uri:str):
    try:
        sparql = f"""SELECT ?p ?o WHERE {{
                    <{uri}> ?p ?o.    
                }} ORDER BY ?p"""
        query = {'query': sparql}
        r = requests.get(Endpoint.METAKG, params=query, headers=Headers.GET)
        print('rr',r)
        return r.json()['results']['bindings']
    except Exception as err:
        return err


class ExportedView:
    def __init__(self): pass

    def get_datasource_properties(self, exported_view_uri:str):
        try:
            sparql = Prefixies.EXPORTED_VIEW + f"""SELECT * WHERE {{
                        <{exported_view_uri}> vskg:hasDataSource ?ds;
                            vskg:hasMappings ?m.
                        ?ds vskg:connection_url ?conn;
                            vskg:jdbc_driver ?jdbc_driver;
                            vskg:password ?pwd;
                            vskg:username ?un.
                        ?m vskg:file_path ?f. 
                    }}"""
            query = {'query': sparql}
            # print('q', query)
            r = requests.get(Endpoint.METAKG, params=query, headers=Headers.GET)
            print('rr',r)
            return r.json()['results']['bindings']
        except Exception as err:
            return err

class MetaMashup:
    def __init__(self): pass


    def cria_um_recurso_meta_mashup(self, obj: MetaMashupModel):
        """Cria uma instância de Grafo de Metadados Mashup"""
        try:
            identifier = str(uuid.uuid4())
            rotulo_com_underscore = Functions.removeAcentosEAdicionaUnderscore(obj.label)
            # nome_app = Functions.removeAcentosEAdicionaUnderscore(obj.app_name)

            existe = self.obtem_meta_mashup_by_uri(ns.VSKGR + rotulo_com_underscore)
            if (len(existe) > 0):
                return {"code": 409, "message": "URI Já existe!"}
            
            # <{obj.uri_camada_app}> 
                #         {o.P_HAS_APPLICATION} <{obj.namespace_base + nome_app}> .
                # <{obj.namespace_base + nome_app}>
                        # {o.P_LABEL} "{obj.app_name}" ;
                        # {o.P_DC_DESCRIPTION} "{obj.app_description}".
#  <{obj.namespace_base}MVS_{rotulo_com_underscore}> rdf:type vskg:MashupViewSpecification ;
#                         rdfs:label "MVS {obj.label}" .                    


            q = Prefixies.ALL + f"""INSERT DATA {{
                <{ns.VSKGR + rotulo_com_underscore}> rdf:type vskg:MetadataGraphMashup ;
                    {o.P_LABEL} "{obj.label}" ;
                    {o.P_DC_IDENTIFIER} "{identifier}" ;
                    vskg:has_mashup_view <{ns.VSKGR}MVS_{rotulo_com_underscore}> .
                <{ns.VSKGR}MVS_{rotulo_com_underscore}> {o.P_TYPE} {o.C_MASHUP_VIEW_SPEC} ;
                    {o.P_LABEL} "MVS {obj.label}" .
              }} """
            sparql = {"update": q}
            r = requests.post(Endpoint.METAKG + "/statements", params=sparql, headers=Headers.POST)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Criado com Sucesso!"}
            else:
                return {"code": 400, "message": "Não foi criado!"}
        except Exception as err:
            return err
        


    def lista_recursos_meta_mashup(self):
        """Obtém instâncias de Grafo de Metadados Mashup"""
        try:
            q = Prefixies.ALL + f"""SELECT * WHERE {{ 
                    ?uri rdf:type vskg:MetadataGraphMashup ;
                         rdfs:label ?uri_l ;
                         {o.P_DC_IDENTIFIER} ?identifier ;
                         vskg:has_mashup_view ?uri_mashup_view .
                    OPTIONAL {{ ?uri vskg:reuse_metadata_from ?uri_metaEKG .
                        OPTIONAL {{    ?uri_metaEKG rdfs:label ?uri_metaEKG_l . }}
                    }}
                }}"""
            sparql = {'query': q}
            r = requests.get(Endpoint.METAKG, params=sparql, headers=Headers.GET)
            print(r.json())
            if(r.status_code == 200):
                return r.json()['results']['bindings']
            else:
                return {"code": 400, "message": "Não Encontrado!"}
        except TypeError as err:
            return err


    def encontra_propriedades(self, uri:str):
        """Retorna as propriedades de um uri"""
        try:
            print(uri)
            sparql = Prefixies.ALL + f"""SELECT * WHERE {{ 
                <{uri}> ?p ?o . 
                OPTIONAL {{ ?p {o.P_LABEL} ?l . }}
            }}"""
            
            r = requests.get(Endpoint.METAKG, params={'query': sparql}, headers=Headers.GET)
            if(r.status_code == 200):
                return r.json()['results']['bindings']
            else:
                return {"code": 400, "message": "Não Encontrado!"}
        except Exception as err:
            return err


    def associa_metaEKG(self, obj: AssociaMetaEKGAoMetaMashupModel):
        """Registra o KG de Metadados cujos metadados serão utilizados"""
        try:
            q = Prefixies.ALL + f"""INSERT DATA {{ 
                <{obj.uri_meta_mashup}> vskg:reuse_metadata_from <{obj.uri_meta_ekg}> . 
            }}"""
            sparql = {"update": q}
            r = requests.post(Endpoint.METAKG + "/statements", params=sparql, headers=Headers.POST)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Criado com Sucesso!"}
            else:
                return {"code": 400, "message": "Não foi criado!"}
        except Exception as err:
            return err







    def obtem_meta_mashup_by_uri(self, uri: str):
        """Obtém uma instância de MetaMashup a partir de uma uri"""
        try:
            q = Prefixies.ALL + \
                f"SELECT DISTINCT ?l WHERE {{ <{uri}> rdfs:label ?l . }}"
            sparql = {'query': q}
            r = requests.get(Endpoint.METAKG,
                             params=sparql, headers=Headers.GET)
            return r.json()['results']['bindings']
        except Exception as err:
            return err

    def obtem_gcl(self):
        """Obtém a partir de uma uri do gcl"""
        try:
            return None
            # q = Prefixies.ALL + \
            #     f"""SELECT * WHERE {{ 
            #         <{uri_meta_mashup}> ?p ?o . 
            #     }}"""
            # print(f'query: {q}')
            # sparql = {'query': q}
            # r = requests.get(Endpoint.METADADOS_TULIO,
            #                 params=sparql, headers=Headers.GET)
            # return r.json()['results']['bindings']
        except Exception as err:
            return err

    def obtem_gcl_by_uri(self, uri_gcl: str):
        """Obtém a partir de uma uri do gcl"""
        try:
            q = Prefixies.ALL + \
                f"SELECT * WHERE {{ <{uri_gcl}> ?p ?o . }}"
            print(f'query: {q}')
            sparql = {'query': q}
            r = requests.get(Endpoint.METADADOS_TULIO,
                            params=sparql, headers=Headers.GET)
            return r.json()['results']['bindings']
        except Exception as err:
            return err


    def add_gcl_visao_semantica_mashup(self, data: AddGCLMashupModel):
        """Adiciona um GCL à Especifiação da Visão Semântica o MetaMashup.
        A ideia é fazer uma cópia do GCL escolhido no EKG e depois selecionar as propriedades 
        que comporão o mashup"""
        try:
            # Verificar se a uri já existe
            # existe = self.obtem_meta_mashup_by_uri(uri_resource + rotulo_com_underscore)
            # if (len(existe) > 0):
            #     return {"code": 409, "message": "Já existe essa uri!"}

            q = Prefixies.ALL + f"""INSERT DATA {{ 
                <{data.uri_visao_semantica_mashup}> vskg:hasLocalGraph <{data.uri_gcl}> ;
                                          rdfs:label "{data.label_gcl}" .
              }} """
            sparql = {"update": q}
            r = requests.post(Endpoint.METAKG + "/statements",
                              params=sparql, headers=Headers.POST)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Criado com Sucesso!"}
            else:
                return {"code": 400, "message": "Não foi criado!"}
        except Exception as err:
            return err


class MetaEKG:
    def __init__(self): pass

    # Genérica
    def lista_recursos_meta_ekg(self):
        """Encontra instâncias de META-EKG"""
        try:
            sparql = Prefixies.ALL + f"""SELECT * WHERE {{ 
                ?uri {o.P_TYPE} {o.C_META_EKG} ;
                    {o.P_LABEL} ?uri_l .
            }}"""
            
            # r = requests.get(Endpoint.SEFAZMA_VEKG_ABOX, params={'query': sparql}, headers=Headers.GET)
            r = requests.get(Endpoint.VSKG_ABOX, params={'query': sparql}, headers=Headers.GET)
            if(r.status_code == 200):
                return r.json()['results']['bindings']
            else:
                return {"code": 400, "message": "Não Encontrado!"}
        except Exception as err:
            return err
    
    def encontra_propriedades(self, uri:str):
        """Retorna as propriedades de um uri"""
        try:
            print(uri)
            sparql = Prefixies.ALL + f"""SELECT * WHERE {{ 
                <{uri}> ?p ?o . 
                OPTIONAL {{ ?p {o.P_LABEL} ?l . }}
                FILTER(LANG(?l) = 'pt')
            }}"""
            
            r = requests.get(Endpoint.SEFAZMA_VEKG_ABOX, params={'query': sparql}, headers=Headers.GET)
            if(r.status_code == 200):
                return r.json()['results']['bindings']
            else:
                return {"code": 400, "message": "Não Encontrado!"}
        except Exception as err:
            return err


    def obtem_meta_ekg(self):
        """Obtém instâncias de Grafo de Metadados EKG"""
        try:
            q = Prefixies.ALL + \
                "SELECT * WHERE { ?s rdf:type vskg:MetadataGraphEKG . }"
            sparql = {'query': q}
            r = requests.get(Endpoint.SEFAZMA_VEKG_ABOX,
                             params=sparql, headers=Headers.GET)
            print(r)
            if(r.status_code == 200):
                return r.json()
            else:
                return {"code": 400, "message": "Não foi criado!"}
        except Exception as err:
            return err

    def lista_gcl_do_meta_ekg(self, uri_meta_ekg):
        """Lista os Grafos de Conhecimento Locais do Meta-EKG"""
        try:
            print(f'LISTAR TODOS OS GCL DO EKG')
            q = Prefixies.ALL + \
                f"""SELECT ?grafo_local ?grafo_local_l WHERE {{ 
                    <{uri_meta_ekg}> vskg:hasSemanticMetadata ?camada_semantica . 
                    ?camada_semantica vskg:hasSemanticView ?visao_semantica .
                    ?visao_semantica vskg:hasLocalGraph ?grafo_local .
                    ?grafo_local rdfs:label ?grafo_local_l .
                }}"""
            sparql = {'query': q}
            r = requests.get(Endpoint.SEFAZMA_VEKG_ABOX,
                             params=sparql, headers=Headers.GET)
            if(r.status_code == 200):
                return r.json()['results']['bindings']
            else:
                return {"code": 400, "message": "Não Encontrado!"}
        except Exception as err:
            return err