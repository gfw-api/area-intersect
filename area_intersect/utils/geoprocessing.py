from shapely.geometry import shape, mapping
from shapely.ops import cascaded_union

def intersection(geom1,geom2):
    inter = list()
    for feature1 in geom1['features']:
        poly1 = shape(feature1['geometry'])
        for feature2 in geom2['features']:
            poly2 = shape(feature2['geometry'])
            inter.append(poly1.intersection(poly2))

    union = cascaded_union(inter)

    return mapping(union)

