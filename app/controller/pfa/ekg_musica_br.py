function_artist_name = """
def fusion_foaf_name(c, v):
  out = ""
  if "http://xmlns.com/foaf/0.1/name" in v[c]:
    for foafName in v[c]["http://xmlns.com/foaf/0.1/name"]:
      if (foafName[2] == "MusicBrainz"):
        out = [[foafName[0], foafName[1], foafName[2]]]
        break
    v[c]["http://xmlns.com/foaf/0.1/name"] = out
  return v

_out = fusion_foaf_name(can_uri, _out)
"""




fusion_resolution_artist_thumbnail = """
def fusion_schema_thumbnail(c, v):
  out = None
  if "http://schema.org/thumbnail" in v[c]:
    for schemaThumb in v[c]["http://schema.org/thumbnail"]:
      if (schemaThumb[2] == "Spotify"):
        out = [[schemaThumb[0], schemaThumb[1], schemaThumb[2]]]
        break
    v[c]["http://schema.org/thumbnail"] = out
    return v
_out = fusion_schema_thumbnail(can_uri, _out)
"""


# execute_fusion_resolution_artist_thumbnail = ""






function_resolution_artists_genres = """
def fusionGenres_Union(c, v):
  out, prov, prop, completed = set(), "", "", 0 
  if "http://www.arida.ufc.br/ontologies/music#genres" in v[c]:
    for genre in v[c]["http://www.arida.ufc.br/ontologies/music#genres"]:
      aux = set(genre[0].split(","))
      out = out.union(aux)
      if (len(aux) > completed):
        completed = len(aux)
        prov = genre[2]
        prop = genre[1]
    v[c]["http://www.arida.ufc.br/ontologies/music#genres"] = [[", ".join(list(out)), prop, prov]]
  return v

_out = fusionGenres_Union(can_uri, _out)
"""


function_resolution_artists_categories = """
def fusion_only_one_category(c, v):
  out = ""
  if "http://www.arida.ufc.br/ontologies/music#artistType" in v[c]:
    for category in v[c]["http://www.arida.ufc.br/ontologies/music#artistType"]:
      if (category[2] == "MusicBrainz"):
        out = [[category[0], category[1], category[2]]]
        break
    v[c]["http://www.arida.ufc.br/ontologies/music#artistType"] = out
  return v
_out = fusion_only_one_category(can_uri, _out)
"""


function_artists_albuns = """
def fusion_artists_albuns(c, v):
  out = []
  if "http://xmlns.com/foaf/0.1/made" in v[c]:
    atual = v[c]["http://xmlns.com/foaf/0.1/made"][0]
    for album in v[c]["http://xmlns.com/foaf/0.1/made"][1:]:
      if str(atual[3]).lower() != str(album[3]).lower():
        out.append(atual)
        atual = album
      else:
        if atual[2] == "MusicBrainz": 
          atual = atual
        elif album[2] == "MusicBrainz": 
          atual = album
    v[c]["http://xmlns.com/foaf/0.1/made"] = out
  return v
_out = fusion_artists_albuns(can_uri, _out)
"""
