import requests
import json
from area_intersect.routes.api import error
import logging
from flask import jsonify


def get_service_info(service_url):

    try:

        logging.info('[UTILS]: FeatureService: {}'.format(service_url))
        r = requests.get(service_url + '?f=pjson')
        logging.info('[UTILS]: FeatureService response: {}'.format(r.text))

        if r.status_code == 200:
            info = r.json()

            if "type" in info.keys():
                type_ = info["type"]
            else:
                type_ = None
            logging.debug('[UTILS]: type: {}'.format(type_))
            assert (type_ == "Feature Layer"), "Not a feature layer"

            if "geometryType" in info.keys():
                geometry_type = info["geometryType"]
            else:
                geometry_type = None
            logging.debug('[UTILS]: geometry_type: {}'.format(geometry_type))
            assert (geometry_type == "esriGeometryPolygon"), "Not a polygon geometry"

            if "currentVersion" in info.keys():
                version = info["currentVersion"]
            else:
                version = None
            logging.debug('[UTILS]: version: {}'.format(version))
            assert (version is not None), "Feature Service has no currentVersion number"

            if "name" in info.keys():
                name = info["name"]
            else:
                name = None
            logging.debug('[UTILS]: name: {}'.format(name))

            if "fields" in info.keys():
                fields = info["fields"]
            else:
                fields = None
            logging.debug('[UTILS]: fields: {}'.format(fields))
            assert (isinstance(fields, list)), "Layer has no fields"

            objectid = get_objectid(fields)
            logging.debug('[UTILS]: objectid: {}'.format(objectid))
            assert (objectid is not None), "Layer has no object id"

            logging.debug('[UTILS]: name, objectid, version: {}, {}, {}'.format( name, objectid, version))

            return {"name": name, "objectid": objectid, "version": version}

        else:
            logging.error('[UTILS]: Feature layer response {}'.format(r.text))
            return {"errors":[{"status":r.status_code, "detail":r.text}]}

    except AssertionError as e:
        logging.error('[UTILS]: Feature layer assertation {}'.format(str(e)))
        return {"errors":[{"status":400, "detail":str(e)}]}

    except:
        logging.error('[UTILS]: Feature layer request')
        return {"errors":[{"status":400, "detail":"Not a valid request"}]}


def get_objectid(fields):

    for field in fields:
        if field["type"] == "esriFieldTypeOID":
            return field["name"]
    return None


def get_features(service_url, fields, geometry, where='1=1', format='geojson'):

    #service_url = "https://gis.forest-atlas.org/server/rest/services/cod/Affectation_des_terres_en/MapServer/112"

    logging.debug('[UTILS]: service_url: {}'.format(service_url))
    logging.debug('[UTILS]: fields: {}'.format(fields))
    logging.debug('[UTILS]: geometry: {}'.format(geometry))
    logging.debug('[UTILS]: where: {}'.format(where))
    logging.debug('[UTILS]: format: {}'.format(format))

    # TODO assess: geometry is esrijson

    payload = {"where": (None, where),
               "geometry": (None, json.dumps(geometry)),
               "geometryType": (None, "esriGeometryPolygon"),
               "spatialRel": (None, "esriSpatialRelIntersects"),
               "outFields": (None, fields),
               "returnGeometry": (None, "true"),
               "f": (None, format)
               }

    logging.debug('[UTILS]: payload: {}'.format(payload))

    try:
        r = requests.post(service_url + "/query", files=payload)

        logging.info('[UTILS]: FeatureService response: {}'.format(r.text))
        if r.status_code == 200:
                return r.json()
        else:
                return {"errors":[{"status":r.status_code, "detail":r.text}]}
    except:
       return {"errors":[{"status":400, "detail":"Not a valid request"}]}
