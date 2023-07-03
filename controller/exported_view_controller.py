import api
from commons import NameSpaces as ns, Functions, Prefixies, Ontology as o
from uuid import uuid4
from models import DataSource
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

def read_resources():

    # Montar SPARQL
    sparql = Prefixies.DATASOURCE + f""" select * where {{ 
            ?s rdf:type {CLASSE};
               rdfs:label ?l.
        }} limit 100 
        """
    query = {"query": sparql}

    # Chamar a API
    response = api.read_resources(query)
    return response


def materializa(visao_exportada):
    """Materializa uma fonte de dados de acordo com as regras de mapeamentos."""
    fonte = visao_exportada.fonte
    mapping = visao_exportada.mapping
    str_materializacao = f"java -jar r2rml.jar --connectionURL {fonte.connection_url} --user {fonte.username} --password {fonte.password} --mappingFile {mapping.file} --outputFile output.ttl --format TURTLE"