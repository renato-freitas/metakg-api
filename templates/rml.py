def source(nome_mapeamento_alto_nivel: str, url_or_path: str):
  return f"""
    :{nome_mapeamento_alto_nivel} a csvw:Table;
    csvw:url "{url_or_path}";
    csvw:dialect [ 
      a csvw:Dialect;
      csvw:delimiter ";";
      csvw:encoding "UTF-8";
      csvw:header "1"^^xsd:boolean
    ].
  """