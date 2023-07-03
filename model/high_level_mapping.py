from commons import Endpoint, Prefixies, Functions
from models import DataSource, MetaMashupModel, HighLevelMapping

@app.post("/high-level-mappings")
def register_high_level_mapping(data: HighLevelMapping):
  """Regista Mapeamento de Alto Nível"""

  Functions.create_high_level_mapping(data)


  return data