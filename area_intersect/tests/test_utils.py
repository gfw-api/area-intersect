import unittest
from area_intersect.utils import getlist
from werkzeug.datastructures import MultiDict


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

        no_ws = MultiDict([('xy', 'value 1')])
        one_ws = MultiDict([('xy', 'value 1'), ('ws', 'value 2')])
        two_ws = MultiDict([('xy', 'value 1'), ('ws', 'value 2'), ('ws', 'value 3')])

        result = getlist('ws', no_ws)
        self.assertEqual(result, list())

        result = getlist('ws', one_ws)
        self.assertEqual(result, ['value 2'])

        result = getlist('ws', two_ws)
        self.assertEqual(result, ['value 2', 'value 3'])
