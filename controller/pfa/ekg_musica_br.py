def fusionFoafName(c, v):
  """
  c: canonical uri
  v: set of values of p foaf:name
  """
  out = None
  for foafName in v[c]["http://xmlns.com/foaf/0.1/name"]:
    if (foafName[2] == "MusicBrainz"):
      out = [[foafName[0], foafName[1], foafName[2]]]
      break
  v[c]["http://xmlns.com/foaf/0.1/name"] = out
  return v


def fusionFoafHomepage(c, v):
  """
  c: canonical uri
  v: set of values of p foaf:homepage
  """
  out = None
  for foafName in v[c]["http://xmlns.com/foaf/0.1/homepage"]:
    print('-----valor atual-----: ', foafName)
    if (foafName[2] == "MusicBrainz"):
      out = [[foafName[0], foafName[1], foafName[2]]]
      break
  v[c]["http://xmlns.com/foaf/0.1/homepage"] = out
  return v