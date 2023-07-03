import platform
import os
from fastapi import APIRouter
from model.datasource_model import DataSourceModel
from model.exported_view_model import ExportedViewModel
from commons import NameSpaces as ns, Ontology as o
from controller import exported_view_controller
router = APIRouter()

CLASSE = "ExportedView"
TAG = "exportedviews" 
ROTA = f'/{TAG}/'
PADRAO_URI = f'{ns.VSKGR}{CLASSE}'


@router.get(ROTA, tags=[TAG])
async def read_data_sources():
    response = datasource_controller.read_resources()
    return response


# @router.get(ROTA+"me", tags=[TAG])
# async def read_data_source():
#     return {"username": "fakecurrentuser"}


# @router.get(ROTA+"{username}", tags=[TAG])
# async def read_user(username: str):
#     return {"username": username}


@router.post(ROTA, tags=[TAG])
async def create_exported_view(data: ExportedViewModel):
    """
    Cria um recurso visão exportada do tipo vskg:LocalGraph.
    """
    try:
        response = exported_view_controller.create(data)
        return response
    except Exception as err:
        return err


# https://janakiev.com/blog/python-shell-commands/
# @app.get("/triplify")
@router.post(ROTA + "triplify", tags=[TAG])
def run_triplification():
  operational_system = platform.system()
  if(operational_system == 'Windows'):
    # r = os.system(".\\d2rq-dev\\dump-rdf.bat -u ufc_sem -p ufcsemantic22_ -f N-TRIPLE -j jdbc:oracle:thin:@10.1.1.188:1521/bigsem.sefaz.ma.gov.br C:\\Users\\Adm\\ldif-0.5.2\\gcl\\mappings\\map-rfb-old-maranhao.ttl > C:\\Users\\Adm\\graphdb-import\\can-delete-this.nt")
    r = os.system("""java -jar .\\tools\\rmlmapper-6.1.3-r367-all.jar -m .\\mappings\\map_ufc2.ttl -o .\\aboxies\\teste-ufc.ttl -s turtle""")
   
    return r
  elif operational_system == 'Linux':
    r = os.system("ls -a")
    return r