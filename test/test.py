'''
Tests for the backend restful api.
'''

import unittest
import requests


HEADERS = {'Content-Type': 'application/json'}
ALL_URL = 'http://localhost:5000/all'


'''
Unit tests
'''
class ApiTests(unittest.TestCase):
    def test_empty_db(self):
        '''
        Assert database is empty
        '''
        response = requests.get(ALL_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

if __name__ == '__main__':
    unittest.main()
