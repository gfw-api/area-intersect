"""API ROUTER"""

import logging

from flask import jsonify, Blueprint, request
from area_intersect.utils import getlist

router_endpoints = Blueprint('router_endpoints', __name__)





@router_endpoints.route('/area-intersect', strict_slashes=False, methods=['GET'])
def area_intersect():
    """World Endpoint"""
    #parser = reqparse.RequestParser()
    #parser.add_argument('geostore',)
    #parser.add_argument('ws', action='append')
    logging.info('[ROUTER]: Parse webservics')

    #args = parser.parse_args()

    #geostore_id = args['geostore']
    #webservices = args['ws']

    args = request.args

    geostore_id = request.args.get('geostore', None)
    webservices = getlist('ws', args)

    result = {"geostore": geostore_id, "webservices":str(webservices),
              "args": args}

    return jsonify(data=result), 200
