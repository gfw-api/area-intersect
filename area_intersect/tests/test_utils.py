import unittest
from unittest import mock
from area_intersect import app
from area_intersect.utils import getlist
from area_intersect.utils.geostore import get_geostore
from werkzeug.datastructures import ImmutableMultiDict
import logging
import json

with open('area_intersect/tests/fixtures/geostore.json') as src:
    geostore = json.load(src)

geostore_id = "204c6ff1dae38a10953b19d452921283"

def mocked_request_to_microservice(*args, **kwargs):

    """ mock geostore response """

    logging.debug('[MOCK]: args: {}'.format(args))

    if args[0]['uri'] == '/geostore/{}?format={}'.format(geostore_id, 'esri') and \
            args[0]['method'] == 'GET':
        return geostore
    else:
        return None

class UtilsTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass


    def test_getlist(self):

        #  test if getlist extracts values correctly from MultiDict

        no_ws = ImmutableMultiDict([('xy', 'value 1')])
        one_ws = ImmutableMultiDict([('xy', 'value 1'), ('ws', 'value 2')])
        two_ws = ImmutableMultiDict([('xy', 'value 1'), ('ws[0]', 'value 2'), ('ws[1]', 'value 3')])

        result = getlist('ws', no_ws)
        self.assertEqual(result, list())

        result = getlist('ws', one_ws)
        self.assertEqual(result, ['value 2'])

        result = getlist('ws', two_ws)
        self.assertEqual(result, ['value 2', 'value 3'])


    @mock.patch('area_intersect.utils.geostore.request_to_microservice', side_effect=mocked_request_to_microservice)
    def test_get_geostore(self, mock_config):

        """ Test to make calls to geostore """

        logging.debug('[TEST]: Test to make call to geostore')

        g = get_geostore(geostore_id)
        self.assertEqual(g, geostore)
        self.assertIn(mock.call({'uri': '/geostore/{}?format={}'.format(geostore_id, 'esri'),
                                 'method': 'GET'}),
                      mock_config.call_args_list)
