from CTRegisterMicroserviceFlask import request_to_microservice
from area_intersect.routes.api import error
from area_intersect.utils.reproject import reproject_esrijson

def get_geostore(geostore_id, format='esri'):

    """ make request to geostore microservice for user given geostore ID """

    config = {
            'uri': '/geostore/{}?format={}'.format(geostore_id, format),
            'method': 'GET',
    }

    return request_to_microservice(config)

def get_esrijson_wm(geostore_id):

    """ get esrijson from geostore and reproject is into webmercator """

    geostore = get_geostore(geostore_id)

    if "errors" in geostore.keys():
        return error(status=400, detail=geostore["errors"])
    else:
        esrijson = reproject_esrijson(geostore["data"]["attributes"]["esrijson"])

    return esrijson
