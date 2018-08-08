from CTRegisterMicroserviceFlask import request_to_microservice
from area_intersect.routes.api import error


def get_geostore(geostore_id, format='esri'):

    """ make request to geostore microservice for user given geostore ID """

    config = {
            'uri': '/geostore/{}?format={}'.format(geostore_id, format),
            'method': 'GET',
    }

    return request_to_microservice(config)

