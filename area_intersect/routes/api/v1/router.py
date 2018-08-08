"""API ROUTER"""

import logging
from flask import jsonify, Blueprint, request
from area_intersect.utils import getlist
from area_intersect.utils.geostore import get_geostore
from area_intersect.routes.api import error

router_endpoints = Blueprint('router_endpoints', __name__)

@router_endpoints.route('/area-intersect', strict_slashes=False, methods=['GET'])
def area_intersect():
    """World Endpoint"""

    logging.info('[ROUTER]: Parse webservics')

    args = request.args

    geostore_id = request.args.get('geostore', None)
    webservices = getlist('ws', args)

    logging.info('[ROUTER]: Fetch geostore')
    geostore = get_geostore(geostore_id=geostore_id, format="esri")

    if "errors" in geostore.keys():
        logging.debug('[ROUTER]: ERROR: {}'.format(geostore))

        if geostore['errors'][0]['status'] == 404:
            return error(status=404, detail="GeoStore not found")
        else:
            return error(status=400, detail="Error while fetching geostore")

    for webservice in webservices:
        pass

    result = {"geostore": geostore, "webservices":str(webservices),
              "args": args}

    return jsonify(data=result), 200
