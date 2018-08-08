"""API ROUTER"""

import logging
from flask import jsonify, Blueprint, request
from area_intersect.utils import getlist
from area_intersect.utils.geostore import get_geostore
from area_intersect.utils.feature_service import get_service_info, get_features
from area_intersect.utils.geoprocessing import intersection

from area_intersect.routes.api import error

router_endpoints = Blueprint('router_endpoints', __name__)

@router_endpoints.route('/area-intersect', strict_slashes=False, methods=['GET'])
def area_intersect():
    """World Endpoint"""

    logging.info('[ROUTER]: Parse webservics')

    args = request.args

    geostore_id = request.args.get('geostore', None)
    webservices = getlist('ws', args)
    logging.debug('[ROUTER]: Webserivce: {}'.format(webservices))

    logging.info('[ROUTER]: Fetch geostore')
    geostore = get_geostore(geostore_id=geostore_id, format="esri")

    if "errors" in geostore.keys():
        logging.debug('[ROUTER]: ERROR while fetching geostore: {}'.format(geostore))

        if geostore['errors'][0]['status'] == 404:
            return error(status=404, detail="GeoStore not found")
        else:
            return error(status=400, detail="Error while fetching geostore")

    geometry = geostore["data"]["attributes"]["esrijson"]

    intersecting_geoms = list()

    for webservice in webservices:
        response = get_service_info(webservice)
        logging.debug('[ROUTER]: service info response: {}'.format(response))
        if "errors" in response.keys():
            logging.error('[ROUTER]: {}'.format(response["errors"]))
            return error(status=response["errors"][0]["status"],
                         detail=response["errors"][0]["detail"])
        else:
            geoms = get_features(webservice, response["objectid"], geometry)
        if "errors" in geoms.keys():
            logging.error('[ROUTER]: {}'.format(geoms["errors"]))
            return error(status=geoms["errors"][0]["status"],
                         detail=geoms["errors"][0]["detail"])
        else:
            intersecting_geoms.append(geoms)

        for geom in intersecting_geoms:
            inter = intersection(geostore["data"]["attributes"]["geojson"],geom)


    result = {"geostore": geostore, "webservices":str(webservices),
              "args": args, "geoms": intersecting_geoms, "inter": inter}

    return jsonify(data=result), 200
