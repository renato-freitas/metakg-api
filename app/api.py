import os
from fastapi import FastAPI, HTTPException, status
import uuid
import requests
# from unidecode import unidecode
from commons import Prefixies, NameSpaces as ns, Endpoint, EndpointDEV, Headers, Functions, VSKG as o, NamedGraph
from commons import VSKG, ENVIROMENT, TBOX_SAVED_QUERY
# from models import DataSource, MetaMashupModel, HighLevelMapping, DataProperty, AddGCLMashupModel, AssociaMetaEKGAoMetaMashupModel
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv
# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()
# dotenv = Dotenv(".env")

ENVIROMENT = os.getenv("DEPLOY")
print('ENVIROMENT', os.getenv("DEPLOY"))

def read_resources_metakg(query):
    try:
        r = requests.get(Endpoint.METAKG, params=query, headers=Headers.GET)
        return r.json()['results']['bindings']
    except Exception as err:
        return err
    
def update_resource_kg_metadata(sparql):
    try:
        r = requests.post(EndpointDEV.PRODUCTION + "/statements", params=sparql, headers=Headers.POST)
        print('*** response', r)
        if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
            return {"code": 204, "message": "Criado com Sucesso!"}
        else:
            return {"code": 400, "message": "Não foi criado!"}
    except Exception as err:
        return err

def delete_resource_metakg(query):
    try:
        r = requests.post(Endpoint.METAKG, params=query, headers=Headers.GET)
        return r.json()['results']['bindings']
    except Exception as err:
        return err





class Global:
    def __init__(self, repo:str): 
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo).PRODUCTION

    def execute_sparql_query(self, query):
        """Função genérica. Entrada: sparql. Saída: json."""
        try:
            result = requests.get(self.endpoint, params=query, headers=Headers.GET)
            return result.json()['results']['bindings']
        except Exception as err:
            return err
    
    # NEW
    def get_properties_of_resource_in_exported_view(self, sparql:str):
        try:
            r = requests.get(self.endpoint, params={'query': sparql}, headers=Headers.GET)
            print('------ RESUTL -------\n', r.json()['results']['bindings'])
            # return r.json()['results']['bindings']
            return agroup_properties_in_exported_view(r.json()['results']['bindings'])
        
        except Exception as err:
            return err
    
    # def get_properties_of_resource_in_exported_view(self, uri:str):
    #     try:
    #         sparql = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #         PREFIX owl: <http://www.w3.org/2002/07/owl#>
    #         SELECT ?origin ?p ?label ?o WHERE {{
    # BIND(<{uri}> AS ?origin)
    #                 <{uri}> ?p ?o. 
    #                 OPTIONAL {{
    #     ?p rdfs:label ?label.
    #     FILTER(lang(?label)="pt")    
    # }}
    # # BIND(COALESCE(?_label,?p) AS ?label)
    # FILTER(!CONTAINS(STR(?o),"_:node") && !(?p = owl:topDataProperty) && !(?p = owl:sameAs))}}
    # ORDER BY ?label"""
    #         print('===sparql: get_properities===\n', sparql)
    # # FILTER(!CONTAINS(STR(?o),"_:node") && !(?p = owl:topDataProperty) && !(?p = owl:sameAs))}}"""
    #         r = requests.get(self.endpoint, params={'query': sparql}, headers=Headers.GET)
    #         print('------ RESUTL -------\n', r.json()['results']['bindings'])
    #         # return r.json()['results']['bindings']
    #         return agroup_properties(r.json()['results']['bindings'])
        
    #     except Exception as err:
    #         return err
        
#old
    # def get_properties(self, uri:str):
    #     try:
    #         sparql = f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #         PREFIX owl: <http://www.w3.org/2002/07/owl#>
    #         SELECT ?p ?label ?o WHERE {{
    #                 <{uri}> ?p ?o. 
    #                 OPTIONAL {{
    #     ?p rdfs:label ?label.
    #     FILTER(lang(?label)="pt")    
    # }}
    # # BIND(COALESCE(?_label,?p) AS ?label)
    # FILTER(!CONTAINS(STR(?o),"_:node") && !(?p = owl:topDataProperty) && !(?p = owl:sameAs))}}
    # ORDER BY ?label"""
    #         print('===sparql: get_properities===\n', sparql)
    # # FILTER(!CONTAINS(STR(?o),"_:node") && !(?p = owl:topDataProperty) && !(?p = owl:sameAs))}}"""
    #         r = requests.get(self.endpoint, params={'query': sparql}, headers=Headers.GET)
    #         print('------ RESUTL -------\n', r.json()['results']['bindings'])
    #         return agroup_properties(r.json()['results']['bindings'])
    #     except Exception as err:
    #         return err

    # new
    def get_properties_from_resources_in_unification_view(self, sparql:str):
        print('-------api:get_properties_from_resources_in_unification_view----------')
        try:
            r = requests.get(self.endpoint, params={'query': sparql}, headers=Headers.GET)
            return agroup_properties_in_unification_view(r.json()['results']['bindings'])
        except Exception as err:
            return err
        

    def get_properties_from_resources_in_fusion_view(self, sparql:str):
        print('-------api:get_properties_from_resources_in_fusion_view----------')
        try:
            r = requests.get(self.endpoint, params={'query': sparql}, headers=Headers.GET)
            # print('***', r.json()['results']['bindings'])
            # return r.json()['results']['bindings']
            # return agroup_properties_in_fu(r.json()['results']['bindings'])
            return self.agroup_properties_in_fusion_view2(r.json()['results']['bindings'])
        except Exception as err:
            print('-----err--\n', err)
            return err
   
    # old
    # def get_properties_from_sameAs_resources(self, sparql:str):
    #     print('-------api:get_properties_from_sameAs_resources----------')
    #     try:
    #         r = requests.get(self.endpoint, params={'query': sparql}, headers=Headers.GET)
    #         print('***', r.json()['results']['bindings'])
    #         return agroup_properties_in_sameas(r.json()['results']['bindings'])
    #     except Exception as err:
    #         return err
        

    def agroup_resources(self, resources):
        agrouped = dict()
        for resource in resources:
            if not resource['origin']['value'] in agrouped:
                agrouped[resource['origin']['value']] = []
            agrouped[resource['origin']['value']].append(resource['target']['value'])
        return agrouped
    
    def agroup_instants_in_timeline(self, resources):
        agrouped = dict()
        for resource in resources:
            if not resource['inst']['value'] in agrouped:
                agrouped[resource['inst']['value']] = []
            agrouped[resource['inst']['value']].append(resource)
        return agrouped
    
   
    def agroup_properties_in_fusion_view2(self, properties):
        print('--------api:agroup_properties_in_fusion_view------')
        _agrouped = dict()
        _can = properties[0]['can']['value']
        _agrouped[_can] = {}
        count = 1
        for prop in properties:
            print(count, ' - ', prop, '\n')
            count += 1
            _label =  prop['label']['value'] if "label" in prop else ""
            _label_o = prop['label_o']['value'] if "label_o" in prop else ""
            _prov = prop['prov']['value'] if "prov" in prop else ""
            if not prop['p']['value'] in _agrouped[_can]:
                _agrouped[_can][prop['p']['value']] = [[prop['o']['value'], _label, _prov, _label_o]] 
            else:
                _agrouped[_can][prop['p']['value']].append([prop['o']['value'], _label, _prov, _label_o])
        # print('---fusion view-------\n', _agrouped)
        return _agrouped




    # ACHO QUE DEVE PASSA UMA LISTA DO ASSERTION FUSION PROPERTIES
    def agroup_properties_in_fusion_view(self, properties):
        print('--------api:agroup_properties_in_fusion_view------')
        _agrouped = dict()
        count = 1
        _origin = properties[0]['origin']['value']
        _agrouped[_origin] = {}
        for prop in properties:
            print(count, ' - ', prop, '\n')
            count += 1
            _label = ""
            if not prop['p']['value'] in _agrouped[_origin]:
                _agrouped[_origin][prop['p']['value']] = []
            if "label" in prop:
                _label = prop['label']['value']
            
            # if "target" == prop:
            #     _agrouped[_origin][prop['p']['value']].append([prop['target']['value'], _label, prop['prov']['value']])
            # if "http://xmlns.com/foaf/0.1/name" == prop['p']['value'] and "name" in prop:
            #     _agrouped[_origin][prop['p']['value']] = [[prop['name']['value'], _label, prop['prov']['value']]]
            #     print('-----TEM NAME---------\n', _agrouped)
            # if "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" in prop['p']['value']:
            #     _agrouped[_origin][prop['p']['value']].append([prop['o']['value'], _label, prop['prov']['value']])
            # if "http://schema.org/thumbnail" in prop['p']['value']:
            #     _agrouped[_origin][prop['p']['value']].append([prop['o']['value'], _label, prop['prov']['value']])
            # else:
            _agrouped[_origin][prop['p']['value']] = [[prop['o']['value'], _label, prop['prov']['value']]]
        print('---fusion view-------\n', _agrouped)
        return _agrouped



class KG_Metadata:
    def __init__(self, repo): 
        self.repo = repo
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo).PRODUCTION

    def add_rdf(self, rdf:str):
        try:
            r = requests.post(url=f"http://localhost:7200/repositories/metagraph/rdf-graphs/KG-METADATA", data=rdf, headers=Headers.POST_KG_METADATA)
            print('*** r',r)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Criado com Sucesso!"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi criado!")
        except Exception as err:
            return err

    def create_resource(self, sparql, classe, label):
        try:
            # verificar se o recurso já existe, pela URI (genérico)
            existe = get_one_resource_kg_metadata(classe, label)

            if (len(existe) > 0):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Um recurso dessa classe com essa label já existe!")
            
            r = requests.post(self.endpoint + "/statements", params=sparql, headers=Headers.POST)
            # print('response', r)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Criado com Sucesso!"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi criado!")
        except Exception as err:
            # print('EXCEÇÃO', err)
            return err

    def check_resource(self, resourceURI:str):
        """Verifica se o recurso existe no grafo nomeado de metadados"""
        print('*** API, CHECK IF RESOURCE EXISTS')
        sparql = Prefixies.DATASOURCE + f"""SELECT * FROM <{NamedGraph(self.repo).KG_METADATA}> {{ 
            <{resourceURI}> ?p ?o. 
        }} LIMIT 1"""
        query = {"query": sparql}
        print('*** API, query', sparql)
        try:
            result = requests.get(self.endpoint, params=query, headers=Headers.GET)
            return result.json()['results']['bindings']
        except Exception as err:
            return err



class CompetenceQuestion:
    def __init__(self, repo:str): 
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo).PRODUCTION
    
    def obtem_uma_questao_competencia(self, name:str, repository:str):
        # sparql = Prefixies.QUERIES + f"""SELECT * FROM <http://localhost:7200/repositories/{repository}/rdf-graphs/KG_QUERY> {{ 
        sparql = Prefixies.COMPETENCE_QUESTION + f"""SELECT * FROM <{NamedGraph(repository).KG_COMPETENCE_QUESTION}> {{ 
            ?s {VSKG.P_IS_A} {VSKG.C_COMPETENCE_QUESTION};
             {VSKG.P_NAME} "{name}".
        }} LIMIT 1"""

        query = {"query": sparql}
        print('*** API, query', sparql)
        try:
            result = requests.get(self.endpoint, params=query, headers=Headers.GET)
            return result.json()['results']['bindings']
        except Exception as err:
            return err

    def execute_query_insert_data(self, query, name, repository):
        try:
            exists = self.obtem_uma_questao_competencia(name, repository)
            print('---------existe----------\n', exists)
            if (len(exists) > 0):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Uma questão de competência com esse nome já existe!")
            
            r = requests.post(self.endpoint + "/statements", params=query, headers=Headers.POST)
            print('=========', r.text)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Criado com Sucesso!"}
            else:
                return {"code": 400, "message": "Não foi criado!"}
        except Exception as err:
            print('***\n', err)
            return err
        

class PropertyFunctionAssertion:
    def __init__(self, repo:str): 
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo)(repo).PRODUCTION
    
    def obtem_uma_pfa(self, name:str, repository:str):
        # sparql = Prefixies.QUERIES + f"""SELECT * FROM <http://localhost:7200/repositories/{repository}/rdf-graphs/KG_QUERY> {{ 
        sparql = Prefixies.COMPETENCE_QUESTION + f"""SELECT * FROM <{NamedGraph(repository).KG_PFA}> {{ 
            ?s {VSKG.P_IS_A} {VSKG.C_PFA};
             {VSKG.P_NAME} "{name}".
        }} LIMIT 1"""

        query = {"query": sparql}
        print('*** API, query', sparql)
        try:
            result = requests.get(self.endpoint, params=query, headers=Headers.GET)
            return result.json()['results']['bindings']
        except Exception as err:
            return err

    def execute_query_insert_data(self, query, name, repository):
        try:
            exists = self.obtem_uma_pfa(name, repository)
            print('---------existe----------\n', exists)
            if (len(exists) > 0):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Uma assertiva de fusão de propriedade com esse nome já existe!")
            
            r = requests.post(self.endpoint + "/statements", params=query, headers=Headers.POST)
            print('=========', r.text)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Criado com Sucesso!"}
            else:
                return {"code": 400, "message": "Não foi criado!"}
        except Exception as err:
            print('***\n', err)
            return err
        

class ConsultaSalva:
    def __init__(self, repo:str): 
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo).PRODUCTION
    
    def obtem_uma_consulta_salva(self, name:str, repository:str):
        sparql = Prefixies.QUERIES + f"""SELECT * FROM <http://localhost:7200/repositories/{repository}/rdf-graphs/KG_QUERY> {{ 
            ?s {TBOX_SAVED_QUERY.P_IS_A} {TBOX_SAVED_QUERY.C_SAVED_QUERY};
             {TBOX_SAVED_QUERY.P_NAME} "{name}"@pt.
        }} LIMIT 1"""
        query = {"query": sparql}
        print('*** API, query', sparql)
        try:
            result = requests.get(self.endpoint, params=query, headers=Headers.GET)
            return result.json()['results']['bindings']
            # print('*** API, REPONSE ***',response)
            # return response
        except Exception as err:
            return err

    def execute_query_data(self, query, name, repository):
        try:
            exists = self.obtem_uma_consulta_salva(name, repository)
            print('---------existe----------\n', exists)
            if (len(exists) > 0):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Uma consulta com esse nome já existe!")
            
            # r = requests.post(self.endpoint, data=query, headers=Headers.)
            r = requests.post(self.endpoint + "/statements", params=query, headers=Headers.POST)
            print('=========', r.text)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Criado com Sucesso!"}
            else:
                return {"code": 400, "message": "Não foi criado!"}
        except Exception as err:
            print('***\n', err)
            return err

    # def retrive_queries(self):

    
    def execute_query(self):
        try:
            result = requests.get(self.endpoint)
            print('****\n',result.json())
            return result.json()
        except Exception as err:
            print('***\n', err)
            return err

    def update_saved_query(self, query):
        try:
            r = requests.post(self.endpoint + "/statements", params=query, headers=Headers.POST)
            print('*** response', r)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Atualizado com Sucesso!"}
            else:
                return {"code": 400, "message": "Não foi atualizado!"}
        except Exception as err:
            return err

    def get_one_saved_query(self, name:str):
        try:
            q = self.endpoint + f'?name={name}'
            result = requests.get(q, headers={ "Accept": "application/json" })
            return result.json()
        except Exception as err:
            return err
    # def get_one_saved_query(self, name:str):
    #     try:
    #         q = self.endpoint + f'?name={name}'
    #         result = requests.get(q, headers={ "Accept": "application/json" })
    #         return result.json()
    #     except Exception as err:
    #         return err
        

    # def delete_one_saved_query(self, name:str):
    #     try:
    #         q = self.endpoint + f'?name={name}'
    #         r = requests.delete(q, headers={ "Accept": "*/*" })
    #         if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
    #             return {"code": 204, "message": "Deletado com Sucesso!"}
    #         else:
    #             return {"code": 400, "message": "Consulta não existe!"}
    #     except Exception as err:
    #         return err
    def delete_one_saved_query(self, query:str):
        try:
            r = requests.post(self.endpoint + "/statements", params=query, headers=Headers.POST)
            print('*** response', r)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return {"code": 204, "message": "Deletado com Sucesso!"}
            else:
                return {"code": 400, "message": "Não foi deletado!"}
        except Exception as err:
            return err

# métodos globais
def get_one_resource_kg_metadata(classe:str, label:str):
    try:
        sparql = Prefixies.ALL + \
            f"""SELECT DISTINCT ?l FROM <{NamedGraph.KG_METADATA}> {{ ?s a {classe}; rdfs:label "{label}". }}"""
        query = {'query': sparql}
        response = requests.get(EndpointDEV.PRODUCTION, params=query, headers=Headers.GET)
        return response.json()['results']['bindings']
    except Exception as err:
        return err
    

def check_resource_in_kg_metadata(uri:str):
    """Verifica se o recurso existe no grafo nomeado de metadados"""
    print('*** API, CHECK IF RESOURCE EXISTS')
    sparql = Prefixies.DATASOURCE + f"""SELECT * FROM <{NamedGraph.KG_METADATA}> {{ 
        <{uri}> ?p ?o. 
    }} LIMIT 1"""
    query = {"query": sparql}
    print('*** API, query', sparql)
    # response = execute_query_on_kg_metadata(query)
    # response =   execute_sparql_query(query)
    try:
        result = requests.get(self.endpoint, params=query, headers=Headers.GET)
        return result.json()['results']['bindings']
        print('*** API, REPONSE ***',response)
        return response
    except Exception as err:
        return err


def execute_query_on_kg_metadata(query):
    """Função genérica. Entrada: sparql. Saída: json."""
    try:
        print('*** API, EXECUTE QUERY ON KG METADATA ***')
        r = requests.get(EndpointDEV.PRODUCTION, params=query, headers=Headers.GET)
        print('*** API, RESPONSE ***', r.json()['results']['bindings'])
        if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
            return r.json()['results']['bindings']
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi criado!")
    except Exception as err:
        return err


def execute_sparql_query_in_kg_metadata(query):
    """Função genérica. Entrada: sparql. Saída: json."""
    try:
        print('*** api ***')
        r = requests.post(EndpointDEV.METAKG + "/statements", params=query, headers=Headers.POST)
        # r = requests.post(EndpointDEV.METAKG, params=query, headers=Headers.POST)
        print('*** r',r)
        if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
            return {"code": 204, "message": "Criado com Sucesso!"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi criado!")
    except Exception as err:
        return err


def agroup_properties_in_exported_view(properties):
    print('--------api:agroup_properties_in_exported_view------')
    _agrouped = dict()
    count = 1
    _origin = properties[0]['origin']['value']
    _agrouped[_origin] = {}
    for row in properties:
        print(count, ' - ', row, '\n')
        count += 1
        _label = ""
        _label_o = ""
        if "p" in row:
            if not row['p']['value'] in _agrouped[_origin]:
                _agrouped[_origin][row['p']['value']] = []
            if "label" in row:
                _label = row['label']['value']
            if "label_o" in row:
                _label_o = row['label_o']['value']
            # if "http://www.w3.org/2002/07/owl#sameAs" == prop['p']['value']:
            _agrouped[_origin][row['p']['value']].append([row['o']['value'], _label, "", _label_o])
            # _agrouped[_origin][row['p']['value']].append([_label_o, _label, "", _label_o])
        else:
            print('sem p')
            if not "http://www.w3.org/2002/07/owl#sameAs" in _agrouped[_origin]:
                _agrouped[_origin]["http://www.w3.org/2002/07/owl#sameAs"] = []
            if "target" in row:
                _agrouped[_origin]["http://www.w3.org/2002/07/owl#sameAs"].append([row['target']['value'], _label, "",""])
    print('---------api:exported_view_agrouped----------\n', _agrouped)
    return _agrouped

# NEW 10/06/2024
# def agroup_properties_in_exported_view(properties):
#     print('--------api:agroup_properties_in_exported_view------')
#     _agrouped = dict()
#     count = 1
#     _origin = properties[0]['origin']['value']
#     _agrouped[_origin] = {}
#     _provenance = Functions.getContextFromURI(_origin)
#     for row in properties:
#         print(count, ' - ', row, '\n')
#         count += 1
#         _label = ""
#         if "p" in row:
#             if not row['p']['value'] in _agrouped[_origin]:
#                 _agrouped[_origin][row['p']['value']] = []
#             if "label" in row:
#                 _label = row['label']['value']
#             # if "http://www.w3.org/2002/07/owl#sameAs" == prop['p']['value']:
#             _agrouped[_origin][row['p']['value']].append([row['o']['value'], _label, _provenance])
#         else:
#             print('sem p')
#             if not "http://www.w3.org/2002/07/owl#sameAs" in _agrouped[_origin]:
#                 _agrouped[_origin]["http://www.w3.org/2002/07/owl#sameAs"] = []
#             if "target" in row:
#                 _agrouped[_origin]["http://www.w3.org/2002/07/owl#sameAs"].append([row['target']['value'], _label, ""])
#     print('---------api:exported_view_agrouped----------\n', _agrouped)
#     return _agrouped


# def agroup_properties(properties):
#     print('--------api:agroup_properties------')
#     _agrouped = dict()
#     count = 1
#     _origin = properties[0]['origin']['value']
#     _agrouped[_origin] = {}
#     _provenance = Functions.getContextFromURI(_origin)
#     for prop in properties:
#         print(count, ' - ', prop, '\n')
#         count += 1
#         _label = ""
#         if not prop['p']['value'] in _agrouped[_origin]:
#             _agrouped[_origin][prop['p']['value']] = []
#         if "label" in prop:
#             _label = prop['label']['value']
#         # if "http://www.w3.org/2002/07/owl#sameAs" == prop['p']['value']:
#         # if "target" == prop:
#             # _agrouped[_origin][prop['p']['value']].append([prop['target']['value'], _label, prop['prov']['value']])
#         # else:
#         _agrouped[_origin][prop['p']['value']].append([prop['o']['value'], _label, _provenance])
#         print(_agrouped)
#     return _agrouped
# old
# def agroup_properties(properties):
#     agrouped = dict()
#     for prop in properties:
#         if not prop['p']['value'] in agrouped:
#             agrouped[prop['p']['value']] = []
#         if "label" in prop:
#             agrouped[prop['p']['value']].append([prop['o']['value'], prop['label']['value'], []])
#         else: 
#             agrouped[prop['p']['value']].append([prop['o']['value'], "", []])
#     return agrouped


# new
def agroup_properties_in_unification_view(properties):
    print('--------api:agroup_properties_in_unification_view------')
    _agrouped = dict()
    count = 1
    _origin = properties[0]['origin']['value']
    _agrouped[_origin] = {}
    for prop in properties:
        print(count, ' - ', prop, '\n')
        count += 1
        _label = ""
        _label_o = ""
        if not prop['p']['value'] in _agrouped[_origin]:
            _agrouped[_origin][prop['p']['value']] = []
        if "label" in prop:
            _label = prop['label']['value']
        if "label_o" in prop:
            _label_o = prop['label_o']['value']
        # if "http://www.w3.org/2002/07/owl#sameAs" == prop['p']['value']:
        if "target" == prop:
            _agrouped[_origin][prop['p']['value']].append([prop['target']['value'], _label, prop['prov']['value'], _label_o])
        else:
            _agrouped[_origin][prop['p']['value']].append([prop['o']['value'], _label, prop['prov']['value'], _label_o])
    agrouped = verifica_valores_divergentes(_agrouped, _origin)
    # print('G - ', _agrouped)
    return agrouped

# old
# def agroup_properties_in_sameas(properties):
#     _agrouped = dict()
#     for prop in properties:
#         if not prop['p']['value'] in _agrouped:
#             _agrouped[prop['p']['value']] = []
#         if "label" in prop:
#             _agrouped[prop['p']['value']].append([prop['o']['value'], prop['label']['value'], prop['prov']['value']])
#         else: 
#             _agrouped[prop['p']['value']].append([prop['o']['value'], "", prop['prov']['value']])
#     agrouped = verify_values_divergency(_agrouped)
#     return agrouped


# new
def verifica_valores_divergentes(agrouped_props, resource_origin):
    print('-------api:verifica_valores_divergentes----------')
    # print('valores agrupadaos:', agrouped_props)
    _agrouped_props = dict()
    if resource_origin not in _agrouped_props: 
        _agrouped_props[resource_origin] = {}
    for p in agrouped_props[resource_origin]:
        if (p not in ["http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                      "http://www.w3.org/2000/01/rdf-schema#label", "http://www.w3.org/2000/01/rdf-schema#seeaAlso"
                      "http://purl.org/dc/elements/1.1/identifier", "http://www.w3.org/2002/07/owl#sameAs",
                      "http://purl.org/dc/terms/identifier", "http://schema.org/thumbnail"]):

            if p not in _agrouped_props[resource_origin]:
                _agrouped_props[resource_origin][p] = []

            current_value = agrouped_props[resource_origin][p][0][0] if "http://" not in agrouped_props[resource_origin][p][0][0] else agrouped_props[resource_origin][p][0][3]
            print('-- currente value --', p, current_value)
            for dado in agrouped_props[resource_origin][p]:
                # precisa verificar os labels dos owl:ObjectProperties
                _dado = dado[0] if not "http" in dado else dado[3]
                if (_dado != current_value and "http://" not in dado[0]): 
                    _agrouped_props[resource_origin][p].append([dado[0], dado[1], dado[2], dado[3], True])
                elif (_dado != current_value and "http://" in dado[0]): 
                    _agrouped_props[resource_origin][p].append([dado[0], dado[1], dado[2], dado[3], True])
                else:
                    _agrouped_props[resource_origin][p].append([dado[0], dado[1], dado[2], dado[3], False])
        else:
            _agrouped_props[resource_origin][p] = agrouped_props[resource_origin][p]
    # print(_agrouped_props)
    return _agrouped_props


# # new -> precisa de um novo new (agora é old, 2024-08-28)
# def verifica_valores_divergentes(agrouped_props, resource_origin):
#     print('-------api:verifica_valores_divergentes----------')
#     print('valores agrupadaos:', agrouped_props)
#     _agrouped_props = dict()
#     if resource_origin not in _agrouped_props: 
#         _agrouped_props[resource_origin] = {}
#     for p in agrouped_props[resource_origin]:
#         # print('-----------novo group-----------\n',p)
#         # if _agrouped_props[resource_origin][p] = []
#         if (p not in ["http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
#                       "http://www.w3.org/2000/01/rdf-schema#label", "http://www.w3.org/2000/01/rdf-schema#seeaAlso"
#                       "http://purl.org/dc/elements/1.1/identifier", "http://www.w3.org/2002/07/owl#sameAs",
#                       "http://purl.org/dc/terms/identifier", "http://schema.org/thumbnail"]):
#             # print('------ avaliar apenas datatype properties ------', p)
#             # exemplo: [['valor','propriedade','proveniência'], ...]

#             if p not in _agrouped_props[resource_origin]:
#                 _agrouped_props[resource_origin][p] = []


#             current_value = agrouped_props[resource_origin][p][0][0]
#             for dado in agrouped_props[resource_origin][p]:
#                 # "http://" not in dado[0] => para não verificar os object-propeties
#                 if (dado[0] != current_value and "http://" not in dado[0]): 
#                     _agrouped_props[resource_origin][p].append([dado[0], dado[1], dado[2], dado[3], True])
#                 else:
#                     _agrouped_props[resource_origin][p].append([dado[0], dado[1], dado[2], dado[3], False])
#         else:
#             _agrouped_props[resource_origin][p] = agrouped_props[resource_origin][p]
#     print(_agrouped_props)
#     return _agrouped_props
# old
# def verify_values_divergency(agrouped_props):
#     _agrouped_props = dict()
#     for prop in agrouped_props:
#         _agrouped_props[prop] = []
#         if (prop != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and
#             prop != "http://www.w3.org/2000/01/rdf-schema#label" and
#             prop != "http://www.bigdatafortaleza.com/ontology#uri" and
#             prop != "http://purl.org/dc/elements/1.1/identifier" and
#             prop != "http://purl.org/dc/terms/identifier"):
#             print('*** DIVERGENCY ***\n', agrouped_props[prop] )
#             # exemplo: [['valor','propriedade','proveniência'], ...]
#             current_value = agrouped_props[prop][0][0]
#             for dado in agrouped_props[prop]:
#                 # "http://" not in dado[0] => para não verificar os object-propeties
#                 if (dado[0] != current_value and "http://" not in dado[0]): 
#                     _agrouped_props[prop].append([dado[0], dado[1], dado[2], True])
#                 else:
#                     _agrouped_props[prop].append([dado[0], dado[1], dado[2], False])
#         else:
#             _agrouped_props[prop] = agrouped_props[prop]
#     print('**** novo group: ',_agrouped_props)
#     return _agrouped_props






# SELECT DISTINCT ?same ?p ?o 
# FROM <http://localhost:7200/repositories/metagraph/rdf-graphs/KG-METADATA> {
# 	?s ?p ?o. 
#     BIND(?s as ?same).
# }
# ORDER BY ?same ?p


# def execute_query_production(query):
#     """Função genérica. Entrada: sparql. Saída: json."""
#     try:
#         r = requests.get(Endpoint.SEFAZMA_VEKG_ABOX, params=query, headers=Headers.GET)
#         return r.json()['results']['bindings']
#     except Exception as err:
#         return err

# def get_properties(uri:str, expande_sameas:bool):
#     try:
#         selection_triple = f"<{uri}> ?p ?o. "
#         if expande_sameas == True:
#             print('VISÃO UNIFICADA DEVE SER EXIBIDA')
#             selection_triple= f"""
#                 {{
#                     <{uri}> ?p ?o .
#                 }}
#                 UNION{{
#                     {{
#                         <{uri}> owl:sameAs ?same.
#                         ?same ?p ?o.
#                         FILTER(!CONTAINS(STR(?same),"http://www.sefaz.ma.gov.br/resource/App"))
#                     }}
#                 }}
#                 FILTER(?p != owl:sameAs)
#             """
#         sparql = f"""SELECT ?p ?o ?label WHERE {{
#                     {selection_triple}
#                     OPTIONAL {{ ?o rdfs:label ?label .}}   
#                 }} ORDER BY ?p"""
#         query = {'query': sparql}

#         if(ENVIROMENT=="DEV"):
#             r = requests.get(EndpointDEV.RESOURCES, params=query, headers=Headers.GET)
#         else:
#             r = requests.get(Endpoint.METAKG, params=query, headers=Headers.GET)
#         return r.json()['results']['bindings']
#     except Exception as err:
#         return err


# def get_properties_kg_metadata(uri:str):
#     try:
#         # print('*** API, GET PROPERTIES IN KG METADATA')
#         # sparql = f"""{Prefixies.DATASOURCE} SELECT DISTINCT ?p ?o FROM <{NamedGraph.KG_METADATA}> {{
#         #         <{uri}> ?p ?o. 
#         #         FILTER(?p != {VSKG.P_DB_HAS_TABLE})
#         #     }}
#         #     ORDER BY ?same ?p"""
#         # query = {'query': sparql}
#         # print('*** query', query)
#         r = requests.get(EndpointDEV.PRODUCTION, params=query, headers=Headers.GET)
#         # print('*** resulta get properties:',r.json())
#         return r.json()['results']['bindings']
#     except Exception as err:
#         return err


def get_schema_from_datasource(db_conn_url, db_name, db_username, db_password):
    # print('*** obter schemas 5 ***')
    # dialect+driver://username:password@host:port/database
    engine = create_engine(f"postgresql://{db_username}:{db_password}@{db_conn_url}:5432/{db_name}")
    schema = dict()
    with engine.connect() as connection:
        result = connection.execute(text("select  * from information_schema.tables where table_schema not in ('pg_catalog', 'information_schema') AND table_type = 'BASE TABLE';"))
        # df =pd.DataFrame(result)
        # print(df)
        for row in result:
            table_name = row['table_name']
            schema[table_name] = []
            result_col = connection.execute(text(f"SELECT column_name, data_type, is_nullable, maximum_cardinality FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"))
            for _x in result_col:
                schema[table_name].append(_x)
    # print(schema)

    # connection =  get_connection(db_conn_url, db_name, db_username, db_password)
    # df = pd.read_sql("select  * from information_schema.tables where table_schema not in ('pg_catalog', 'information_schema') AND table_type = 'BASE TABLE';", con=connection)
    # tables = df['table_name']
    # for key, value in tables.items():
    #     query = f"SELECT column_name, data_type, is_nullable, maximum_cardinality FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{value}';"
    #     df_col = pd.read_sql(query, con=connection)
    #     schemas.update({ f"{value}": df_col })
    # connection.close()
    return schema


def get_columns_from_table(table_name, db_conn_url, db_name, db_username, db_password):
    print('get_columns_from_table')
    connection =  get_connection(db_conn_url, db_name, db_username, db_password)
    query = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"
    df_col = pd.read_sql(query, con=connection)
    print('colunas da table', table_name, df_col)

    connection.close()
    return df_col

def get_connection(host, dbname, user, password):
    conn_str = "host={} dbname={} user={} password={}".format(host, dbname, user, password)
    # print(conn_str)
    conn = psycopg2.connect(conn_str)
    print('**** STATUS DA CONEXÃO COM A FONTE DE DADOS', conn.status)
    return conn
    

# def record_tables(connection):
def get_properties_datakg(uri:str, expand_sameas:bool):
    print('OBTEM AS PROPRIEDADES DE UM RECURSO SELECIONADO')
    properties_o = {}
    try:
        select = f"""SELECT DISTINCT ?same ?p ?o WHERE {{"""
        selection_triple = f"""{{ 
                <{uri}> ?p ?o. 
                BIND(<{uri}> as ?same).
            }}
            UNION
            {{
                ?uri owl:sameAs <{uri}>. 
                ?uri owl:sameAs ?sam.
                # FILTER(!CONTAINS(STR(?sam),"http://www.sefaz.ma.gov.br/resource/App")).
                FILTER(!CONTAINS(STR(?sam),"{uri}")).
                BIND(<{uri}> as ?same).
                BIND(owl:sameAs as ?p).
                BIND(?sam as ?o).
            }}
            UNION
            {{
                ?u owl:sameAs <{uri}>. 
                BIND(<{uri}> as ?same).
                BIND(owl:sameAs as ?p).
                BIND(?u as ?o).
            }}
            """
        if expand_sameas == True:
            print('VISÃO UNIFICADA DEVE SER EXIBIDA')
            select = f"select ?same ?p ?o where {{"
            selection_triple= f"""
                {{
                    <{uri}> ?p ?o .
                    BIND (<{uri}> AS ?same)
                }}
                UNION{{
                    {{
                        <{uri}> owl:sameAs ?same.
                        ?same ?p ?o.
                        FILTER(!CONTAINS(STR(?same),"http://www.sefaz.ma.gov.br/resource/App"))
                    }}
                    UNION{{ 
                        ?same owl:sameAs <{uri}>.
                        ?same ?p ?o.
                        FILTER(!CONTAINS(STR(?same),"http://www.sefaz.ma.gov.br/resource/App")).
                    }}
                }}
                FILTER(?p != owl:sameAs)
        """
        # sparql = f"""SELECT ?p ?o ?label WHERE {{
        #             {selection_triple}
        #             OPTIONAL {{ ?o rdfs:label ?label .}}   
        #         }} ORDER BY ?p"""
        sparql = f"""{select}
            {selection_triple} 
        }} ORDER BY ?same ?p"""

        query = {'query': sparql}

        # if(ENVIROMENT=="DEV"):
        #     results = requests.get(EndpointDEV.RESOURCES, params=query, headers=Headers.GET)
        # else:
        results = requests.get(Endpoint.METAKG, params=query, headers=Headers.GET)
        # print(r.json()['results']['bindings'])
        for r in results.json()['results']['bindings']:
            print(r, end='\n\n')
            if not r['p']['value'] in properties_o:
                properties_o[r['p']['value']] = [r]
            else:
                properties_o[r['p']['value']].append(r)
        # return r.json()['results']['bindings']
        print()
        return properties_o
    except Exception as err:
        return err


class RDB:
    def __init__(self, repo): 
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo)(repo).PRODUCTION
    def get_data_from_table(db_conn_url, db_name, db_username, db_password, table_name):
        engine = create_engine(f"postgresql://{db_username}:{db_password}@{db_conn_url}:5432/{db_name}")
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM '{table_name}';"))
            return result
    
    def get_credentials(self, uri_datasource):
        props = get_properties_kg_metadata(uri_datasource) # para saber qual o tipo da fonte de dados
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
        return db_conn_url, db_name, db_username, db_password, db_jdbc_driver

class ExportedView:
    def __init__(self, repo): 
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo).PRODUCTION

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
    def __init__(self, repo): 
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo)(repo).PRODUCTION


    # def cria_um_recurso_meta_mashup(self, obj: MetaMashupModel):
    #     """Cria uma instância de Grafo de Metadados Mashup"""
    #     try:
    #         identifier = str(uuid.uuid4())
    #         rotulo_com_underscore = Functions.removeAcentosEAdicionaUnderscore(obj.label)
    #         # nome_app = Functions.removeAcentosEAdicionaUnderscore(obj.app_name)

    #         existe = self.obtem_meta_mashup_by_uri(ns.VSKGR + rotulo_com_underscore)
    #         if (len(existe) > 0):
    #             return {"code": 409, "message": "URI Já existe!"}
            
            # <{obj.uri_camada_app}> 
                #         {o.P_HAS_APPLICATION} <{obj.namespace_base + nome_app}> .
                # <{obj.namespace_base + nome_app}>
                        # {o.P_LABEL} "{obj.app_name}" ;
                        # {o.P_DC_DESCRIPTION} "{obj.app_description}".
#  <{obj.namespace_base}MVS_{rotulo_com_underscore}> rdf:type vskg:MashupViewSpecification ;
#                         rdfs:label "MVS {obj.label}" .                    


        #     q = Prefixies.ALL + f"""INSERT DATA {{
        #         <{ns.VSKGR + rotulo_com_underscore}> rdf:type vskg:MetadataGraphMashup ;
        #             {o.P_LABEL} "{obj.label}" ;
        #             {o.P_DC_IDENTIFIER} "{identifier}" ;
        #             vskg:has_mashup_view <{ns.VSKGR}MVS_{rotulo_com_underscore}> .
        #         <{ns.VSKGR}MVS_{rotulo_com_underscore}> {o.P_IS_A} {o.C_MASHUP_VIEW_SPEC} ;
        #             {o.P_LABEL} "MVS {obj.label}" .
        #       }} """
        #     sparql = {"update": q}
        #     r = requests.post(Endpoint(repo).METAKG + "/statements", params=sparql, headers=Headers.POST)
        #     if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
        #         return {"code": 204, "message": "Criado com Sucesso!"}
        #     else:
        #         return {"code": 400, "message": "Não foi criado!"}
        # except Exception as err:
        #     return err
        


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
            r = requests.get(Endpoint(repo).METAKG, params=sparql, headers=Headers.GET)
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
            
            r = requests.get(Endpoint(repo).METAKG, params={'query': sparql}, headers=Headers.GET)
            if(r.status_code == 200):
                return r.json()['results']['bindings']
            else:
                return {"code": 400, "message": "Não Encontrado!"}
        except Exception as err:
            return err


    # def associa_metaEKG(self, obj: AssociaMetaEKGAoMetaMashupModel):
    #     """Registra o KG de Metadados cujos metadados serão utilizados"""
    #     try:
    #         q = Prefixies.ALL + f"""INSERT DATA {{ 
    #             <{obj.uri_meta_mashup}> vskg:reuse_metadata_from <{obj.uri_meta_ekg}> . 
    #         }}"""
    #         sparql = {"update": q}
    #         r = requests.post(Endpoint(repo).METAKG + "/statements", params=sparql, headers=Headers.POST)
    #         if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
    #             return {"code": 204, "message": "Criado com Sucesso!"}
    #         else:
    #             return {"code": 400, "message": "Não foi criado!"}
    #     except Exception as err:
    #         return err







    def obtem_meta_mashup_by_uri(self, uri: str):
        """Obtém uma instância de MetaMashup a partir de uma uri"""
        try:
            q = Prefixies.ALL + \
                f"SELECT DISTINCT ?l WHERE {{ <{uri}> rdfs:label ?l . }}"
            sparql = {'query': q}
            r = requests.get(Endpoint(repo).METAKG,
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
            # r = requests.get(Endpoint(repo).METADADOS_TULIO,
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
            r = requests.get(Endpoint(repo).METADADOS_TULIO,
                            params=sparql, headers=Headers.GET)
            return r.json()['results']['bindings']
        except Exception as err:
            return err


    # def add_gcl_visao_semantica_mashup(self, data: AddGCLMashupModel):
    #     """Adiciona um GCL à Especifiação da Visão Semântica o MetaMashup.
    #     A ideia é fazer uma cópia do GCL escolhido no EKG e depois selecionar as propriedades 
    #     que comporão o mashup"""
    #     try:
    #         # Verificar se a uri já existe
    #         # existe = self.obtem_meta_mashup_by_uri(uri_resource + rotulo_com_underscore)
    #         # if (len(existe) > 0):
    #         #     return {"code": 409, "message": "Já existe essa uri!"}

    #         q = Prefixies.ALL + f"""INSERT DATA {{ 
    #             <{data.uri_visao_semantica_mashup}> vskg:hasLocalGraph <{data.uri_gcl}> ;
    #                                       rdfs:label "{data.label_gcl}" .
    #           }} """
    #         sparql = {"update": q}
    #         r = requests.post(Endpoint(repo).METAKG + "/statements",
    #                           params=sparql, headers=Headers.POST)
    #         if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
    #             return {"code": 204, "message": "Criado com Sucesso!"}
    #         else:
    #             return {"code": 400, "message": "Não foi criado!"}
    #     except Exception as err:
    #         return err


class MetaEKG:
    def __init__(self, repo): 
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo).PRODUCTION

    # Genérica
    def lista_recursos_meta_ekg(self):
        """Encontra instâncias de META-EKG"""
        try:
            sparql = Prefixies.ALL + f"""SELECT * WHERE {{ 
                ?uri {o.P_IS_A} {o.C_META_EKG} ;
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
        




# default
# engine = create_engine("mysql://scott:tiger@localhost/foo")

# mysqlclient (a maintained fork of MySQL-Python)
# engine = create_engine("mysql+mysqldb://scott:tiger@localhost/foo")

# PyMySQL
# engine = create_engine("mysql+pymysql://scott:tiger@localhost/foo")
        
# engine = create_engine("oracle://scott:tiger@127.0.0.1:1521/sidname")

# engine = create_engine("oracle+cx_oracle://scott:tiger@tnsname")
        
        # pyodbc
# engine = create_engine("mssql+pyodbc://scott:tiger@mydsn")

# pymssql
# engine = create_engine("mssql+pymssql://scott:tiger@hostname:port/dbname")
        
class Tbox:
    def __init__(self, repo:str): 
        self.endpoint = EndpointDEV(repo).PRODUCTION if ENVIROMENT == "DEV" else Endpoint(repo).PRODUCTION

    def execute_query(self, query):
        """Função genérica. Entrada: sparql. Saída: json."""
        try:
            print('\n---api..Tbox.execute_query---')
            print('+ endpoint:', self.endpoint)
            r = requests.get(self.endpoint, params=query, headers=Headers.GET)
            print('+ result of sparql:', r.json()['results']['bindings'])
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return r.json()['results']['bindings']
            else:
                print(r.text)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi criado!")
        except Exception as err:
            return err       
        


class Repository:
    def __init__(self): 
        self.endpoint = EndpointDEV().REPOSITORIES if ENVIROMENT == "DEV" else Endpoint().REPOSITORIES

    def retrieve_all(self):
        """"""
        try:
            r = requests.get(self.endpoint, headers=Headers.GET)
            if(r.status_code == 200 or r.status_code == 201 or r.status_code == 204):
                return r.json()['results']['bindings']
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi criado!")
        except Exception as err:
            return err  