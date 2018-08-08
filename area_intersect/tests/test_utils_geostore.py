import unittest
from unittest import mock
import json
import logging
from area_intersect import app
from area_intersect.utils.geostore import reproject_esrijson
from area_intersect.utils.geostore import get_esrijson_wm
from area_intersect.utils.geostore import get_geostore


with open('area_intersect/tests/fixtures/geojson.json') as src:
    geojson = json.load(src)

with open('area_intersect/tests/fixtures/esrijson.json') as src:
    esrijson = json.load(src)

with open('area_intersect/tests/fixtures/esrijson_wm.json') as src:
    esrijson_wm = json.load(src)

with open('area_intersect/tests/fixtures/geostore.json') as src:
    geostore = json.load(src)

geostore_id = "204c6ff1dae38a10953b19d452921283"
service_url = 'https://gis.forest-atlas.org/server/rest/services/eth/EthiopiaRestoration/ImageServer'


def mocked_get_geostore(*args, **kwargs):

    """ mock the get_geostore function so that we don't need geostore to be up during testing """

    logging.debug('[MOCK]: args: {}'.format(args))
    if args[0] == geostore_id:
        return geostore
    else:
        return None


def mocked_request_to_microservice(*args, **kwargs):

    """ mock geostore response """

    logging.debug('[MOCK]: args: {}'.format(args))

    if args[0]['uri'] == '/geostore/{}?format={}'.format(geostore_id, 'esri') and \
            args[0]['method'] == 'GET':
        return geostore
    else:
        return None


class UtilsTest(unittest.TestCase):

    """ Test class for utils module """

    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    @mock.patch('area_intersect.utils.geostore.request_to_microservice', side_effect=mocked_request_to_microservice)
    def test_get_geostore(self, mock_config):

        """ Test to make calls to geostore """

        logging.debug('[TEST]: Test to make call to geostore')

        g = get_geostore(geostore_id)
        self.assertEqual(g, geostore)
        self.assertIn(mock.call({'uri': '/geostore/{}?format={}'.format(geostore_id, 'esri'),
                                 'method': 'GET'}),
                      mock_config.call_args_list)

    @mock.patch('area_intersect.utils.geostore.get_geostore', side_effect=mocked_get_geostore)
    def test_get_esrijson_wm(self, mock_geostore_id):

        """ Test to get ESRIJSON from geostore """

        logging.debug('[TEST]: Test get ESRIJSON in WM from geostore')

        ej = get_esrijson_wm(geostore_id)
        self.assertEqual(ej, esrijson_wm)
        self.assertIn(mock.call(geostore_id), mock_geostore_id.call_args_list)

    def test_reproject_esrijson(self):

        """ Test if ESRI Json gets correctly projected into Web Mercator """

        logging.debug('[TEST]: Test reproject ESRIJSON')

        esrijson_proj = reproject_esrijson(esrijson)
        self.assertEqual(esrijson_proj, esrijson_wm)



