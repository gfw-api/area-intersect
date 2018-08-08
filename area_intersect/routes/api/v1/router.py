"""API ROUTER"""

import logging
import flask
from flask import jsonify, Blueprint, request
from area_intersect.utils import getlist
from area_intersect.utils.geostore import get_geostore

router_endpoints = Blueprint('router_endpoints', __name__)





@router_endpoints.route('/area-intersect', strict_slashes=False, methods=['GET'])
def area_intersect():
    """World Endpoint"""

    logging.info('[ROUTER]: Parse webservics')

    args = request.args

    geostore_id = request.args.get('geostore', None)
    webservices = getlist('ws', args)

    geostore = get_geostore(geostore_id=geostore_id, format="geojson")

    result = {"geostore": geostore, "webservices":str(webservices),
              "args": args, "flask": flask.__version__}

    return jsonify(data=result), 200
