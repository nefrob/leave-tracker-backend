'''
Tests for the leave backend restful api.
'''

import unittest
import requests

HEADERS = {'Content-Type': 'application/json'}

LEAVE_LIST_URL = 'http://localhost:5000/leave/list'


'''
Helpers
'''
def clear_leaves():
    '''
    Clear all leaves
    '''
    return requests.delete(LEAVE_LIST_URL)


class LeaveListTests(unittest.TestCase):
    '''
    Leave list unit tests
    '''
    def test_leave_list_get_empty(self):
        '''
        Get empty leave list
        '''
        response = requests.get(LEAVE_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    
    def test_leave_list_get(self):
        '''
        Get all leaves
        '''
        pass


    def test_leave_list_delete(self):
        '''
        Delete all leaves
        '''
        response = requests.delete(LEAVE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], '0 leave(s) deleted')


if __name__ == '__main__':
    unittest.main()