"""API ROUTER"""

import logging

from flask import jsonify, Blueprint, request
import re
from area_intersect.routes.api import error
import json
import CTRegisterMicroserviceFlask
#from flask_restful import reqparse


router_endpoints = Blueprint('router_endpoints', __name__)


def getlist(k, args):
    # find multiple keys with same name in MultiDict and return their values as list
    # replaces the request.args.getlist function
    # which is somehow not working for me

    l = list()
    for key in args.keys():
        a = re.search('{}(?=\[[0-9]\])'.format(k), key)

        if k == key or (a is not None and a.group() == k):
            l.append(args[key])
    return l


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
