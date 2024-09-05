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
        break
    v[c]["http://schema.org/thumbnail"] = out
  return v



def fusionGenres(c, v):
  """
  c: canonical uri
  v: set of values of p 'foaf:name'
  """
  out = None
  if "http://www.arida.ufc.br/ontologies/music#genres" in v[c]:
    for foafName in v[c]["http://www.arida.ufc.br/ontologies/music#genres"]:
      if (foafName[2] == "Spotify"):
        out = [[foafName[0], foafName[1], foafName[2]]]
        break
    v[c]["http://www.arida.ufc.br/ontologies/music#genres"] = out
  return v