def fusionFoafName(c, v):
  """
  c: canonical uri
  v: set of values of p 'foaf:name'
  """
  out = None
  if "http://xmlns.com/foaf/0.1/name" in v[c]:
    for foafName in v[c]["http://xmlns.com/foaf/0.1/name"]:
      if (foafName[2] == "MusicBrainz"):
        out = [[foafName[0], foafName[1], foafName[2]]]
        break
    v[c]["http://xmlns.com/foaf/0.1/name"] = out
  return v


def fusionFoafHomepage(c, v):
  """
  c: canonical uri
  v: set of values of p 'foaf:homepage'
  """
  out = None
  if "http://xmlns.com/foaf/0.1/homepage" in v[c]:
    for foafName in v[c]["http://xmlns.com/foaf/0.1/homepage"]:
      if (foafName[2] == "MusicBrainz"):
        out = [[foafName[0], foafName[1], foafName[2]]]
        break
    v[c]["http://xmlns.com/foaf/0.1/homepage"] = out
  return v

def fusionSchemaThumbnail(c, v):
  """
  c: canonical uri
  v: set of values of p 'schema:thumbnail'
  """
  out = None
  if "http://schema.org/thumbnail" in v[c]:
    for schemaThumb in v[c]["http://schema.org/thumbnail"]:
      if (schemaThumb[2] == "Spotify"):
        out = [[schemaThumb[0], schemaThumb[1], schemaThumb[2]]]
        break
      else:
        out = [[schemaThumb[0], schemaThumb[1], schemaThumb[1]]]
    v[c]["http://schema.org/thumbnail"] = out
  return v




def fusionGenres_Union(c, v):
    """
    c: canonical uri
    v: set of values of p 'vsm:genres'
    """
    out, prov, prop, completed = set(), "", "", 0 
    if "http://www.arida.ufc.br/ontologies/music#genres" in v[c]:
      for genre in v[c]["http://www.arida.ufc.br/ontologies/music#genres"]:
        aux = set(genre[0].split(","))
        out = out.union(aux)
        print('aux->', aux, 'tam aux', len(aux))
        if (len(aux) > completed):
          completed = len(aux)
          prov = genre[2]
          prop = genre[1]
      print('out -> ', [[", ".join(list(out)), prop, prov]])
      v[c]["http://www.arida.ufc.br/ontologies/music#genres"] = [[", ".join(list(out)), prop, prov]]
    return v


function_resolution_artists_genres = """
def fusionGenres_Union(c, v):
  out, prov, prop, completed = set(), "", "", 0 
  if "http://www.arida.ufc.br/ontologies/music#genres" in v[c]:
    for genre in v[c]["http://www.arida.ufc.br/ontologies/music#genres"]:
      aux = set(genre[0].split(","))
      out = out.union(aux)
      print('aux->', aux, 'tam aux', len(aux))
      if (len(aux) > completed):
        completed = len(aux)
        prov = genre[2]
        prop = genre[1]
    print('out -> ', [[", ".join(list(out)), prop, prov]])
    v[c]["http://www.arida.ufc.br/ontologies/music#genres"] = [[", ".join(list(out)), prop, prov]]
  return v

_out = fusionGenres_Union(can_uri, _out)
"""