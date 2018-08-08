from pyproj import Proj, transform
import logging


def reproject_esrijson(esrijson, s_epsg=4326, t_epsg=3857, t_wkid=102100):

    """
    Reproject ESRI JSON from s_epsg to t_epsg
    default WGS84 -> Web Mercator
    Need Proj.4 library to work
    """

    s_proj = Proj(init='EPSG:{}'.format(s_epsg))
    t_proj = Proj(init='EPSG:{}'.format(t_epsg))

    json_in = esrijson

    logging.debug('[UTIL]: esrijson: {}'.format(esrijson))

    # Define dictionary representation of output feature collection
    json_out = {'rings': [],
              'type': 'polygon',
              '_ring': 0,
              'spatialReference': {'wkid': t_wkid, 'latestWkid': t_epsg}
              }

    # Iterate through each feature of the feature collection
    for ring in json_in['rings']:
        # Project/transform coordinate pairs of each ring
        # (iteration required in case geometry type is MultiPolygon, or there are holes)
        x1, y1 = zip(*ring)
        x2, y2 = transform(s_proj, t_proj, x1, y1)
        ring = list(zip(x2, y2))
        # Append rings to output esrijson
        json_out['rings'].append([list(coord) for coord in ring])

    logging.debug('[UTIL]: esrijson_wm: {}'.format(json_out))

    return json_out
