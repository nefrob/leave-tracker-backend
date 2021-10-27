'''
Tests for the leave backend restful api.
'''

import unittest
import requests

from backend.models.leave import MAX_LEAVE


HEADERS = {'Content-Type': 'application/json'}

LEAVE_URL = 'http://localhost:5000/leave'
LEAVE_CREATE_URL = 'http://localhost:5000/leave/create'
LEAVE_REMAINING_URL = 'http://localhost:5000/leave/remaining'
LEAVE_LIST_URL = 'http://localhost:5000/leave/list'

USER_ID = '1'
LEAVE1 = ('2021-01-01T00:00:00', '2021-01-31T00:00:00')
LEAVE2 = ('2021-02-01T00:00:00', '2021-02-28T00:00:00')
LEAVE_LONG = ('2021-01-01T00:00:00', '2021-12-31T00:00:00')

'''
Helpers
'''
def clear_leaves():
    '''
    Clear all leaves
    '''
    return requests.delete(LEAVE_LIST_URL)


def add_leave(start_date, end_date):
    '''
    Add new leave
    '''
    response = requests.post(LEAVE_CREATE_URL,
        json={
            'start_date': start_date,
            'end_date': end_date,
            'user_id': USER_ID},
        headers=HEADERS)

    return response.json()['id']


class LeaveTests(unittest.TestCase):
    '''
    Leave unit tests
    '''
    def test_leave_get(self):
        '''
        Get a leave
        '''
        clear_leaves()

        id = add_leave(*LEAVE1)
        response = requests.get(LEAVE_URL + '/' + str(id))
        self.assertEqual(response.status_code, 200)


    def test_leave_get_nonexistant(self):
        '''
        Get a non-existant leave
        '''
        clear_leaves()

        response = requests.get(LEAVE_URL + '/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'Leave not found'})


    def test_leave_update(self):
        '''
        Update a leave
        '''
        clear_leaves()

        id = add_leave(*LEAVE1)
        response = requests.put(LEAVE_URL + '/' + str(id),
            json={
                'start_date': LEAVE2[0],
                'end_date': LEAVE2[1],
                'user_id': USER_ID},
            headers=HEADERS)

        self.assertEqual(response.status_code, 200)


    def test_leave_update_no_info(self):
        '''
        Update a leave with no info
        '''
        clear_leaves()

        id = add_leave(*LEAVE1)
        response = requests.put(LEAVE_URL + '/' + str(id),
            headers=HEADERS)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'No leave data provided'})
    
    
    def test_leave_update_nonexistant(self):
        '''
        Update a non-existant leave
        '''
        clear_leaves()

        response = requests.put(LEAVE_URL + '/1',
            json={
                'start_date': LEAVE2[0],
                'end_date': LEAVE2[1],
                'user_id': USER_ID},
            headers=HEADERS)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'Leave not found'})


    def test_leave_update_invalid_dates(self):
        '''
        Update a leave with invalid dates
        '''
        clear_leaves()

        id = add_leave(*LEAVE1)
        response = requests.put(LEAVE_URL + '/' + str(id),
            json={
                'start_date': LEAVE1[1],
                'end_date': LEAVE1[0],
                'user_id': USER_ID},
            headers=HEADERS)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Invalid leave range'})


    def test_leave_update_too_long(self):
        '''
        Update a leave with a too long range
        '''
        clear_leaves()

        id = add_leave(*LEAVE1)
        response = requests.put(LEAVE_URL + '/' + str(id),
            json={
                'start_date': LEAVE_LONG[0],
                'end_date': LEAVE_LONG[1],
                'user_id': USER_ID},
            headers=HEADERS)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Not enough leave days'})


    def test_leave_delete(self):
        '''
        Delete a leave
        '''
        clear_leaves()

        id = add_leave(*LEAVE1)
        response = requests.delete(LEAVE_URL + '/' + str(id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Leave deleted'})


    def test_leave_delete_nonexistant(self):
        '''
        Delete a non-existant leave
        '''
        clear_leaves()

        response = requests.delete(LEAVE_URL + '/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'Leave not found'})


class LeaveCreateTests(unittest.TestCase):
    '''
    Leave create unit tests
    '''
    def test_leave_create(self):
        '''
        Create a new leave
        '''
        clear_leaves()

        response = requests.post(LEAVE_CREATE_URL,
        json={
            'start_date': LEAVE1[0],
            'end_date': LEAVE1[1],
            'user_id': USER_ID},
            headers=HEADERS)

        self.assertEqual(response.status_code, 201)


    def test_leave_create_no_info(self):
        '''
        Create a leave without provided data
        '''
        clear_leaves()

        response = requests.post(LEAVE_CREATE_URL,
            headers=HEADERS)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'No leave data provided'})

        response = requests.post(LEAVE_CREATE_URL,
            json={
                'user_id': USER_ID},
            headers=HEADERS)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Missing leave data'})


    def test_leave_create_invalid_dates(self):
        '''
        Create a leave with invalid dates
        '''
        clear_leaves()

        response = requests.post(LEAVE_CREATE_URL,
            json={
                'start_date': LEAVE1[1],
                'end_date': LEAVE1[0],
                'user_id': USER_ID},
            headers=HEADERS)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Invalid leave range'})


    def test_leave_create_too_long(self):
        '''
        Create a leave with a too long range
        '''
        clear_leaves()

        response = requests.post(LEAVE_CREATE_URL,
            json={
                'start_date': LEAVE_LONG[0],
                'end_date': LEAVE_LONG[1],
                'user_id': USER_ID},
            headers=HEADERS)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Not enough leave days'})


class LeaveRemainingTests(unittest.TestCase):
    '''
    Leave remaining unit tests
    '''
    def test_leave_remaining(self):
        '''
        Get remaining leave for a user
        '''
        clear_leaves()

        add_leave(*LEAVE1)
        response = requests.get(
            LEAVE_REMAINING_URL + '/' + USER_ID + '/' + LEAVE2[0],
            headers=HEADERS)

        self.assertEqual(response.status_code, 200)

        # 84 max leave days - 31 days used = 53 remaining
        self.assertEqual(response.json(), {'remaining': 53})

    
    def test_leave_remaining_nonexistant(self):
        '''
        Get remaining leave for a user that doesn't exist
        '''
        clear_leaves()

        response = requests.get(
            LEAVE_REMAINING_URL + '/' + USER_ID + '/' + LEAVE1[0],
            headers=HEADERS)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'remaining': MAX_LEAVE.days})


class LeaveListTests(unittest.TestCase):
    '''
    Leave list unit tests
    '''
    def test_leave_list_get_empty(self):
        '''
        Get empty leave list
        '''
        clear_leaves()

        response = requests.get(LEAVE_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    
    def test_leave_list_get(self):
        '''
        Get all leaves
        '''
        clear_leaves()

        add_leave(*LEAVE1)
        add_leave(*LEAVE2)

        response = requests.get(LEAVE_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


    def test_leave_list_delete(self):
        '''
        Delete all leaves
        '''
        clear_leaves()

        add_leave(*LEAVE1)
        response = requests.delete(LEAVE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': '1 leave(s) deleted'})


if __name__ == '__main__':
    unittest.main()