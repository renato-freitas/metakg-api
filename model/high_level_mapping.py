from commons import Functions
from models import HighLevelMapping

@app.post("/high-level-mappings")
def register_high_level_mapping(data: HighLevelMapping):
  """Regista Mapeamento de Alto Nível"""

  Functions.create_high_level_mapping(data)


  return data