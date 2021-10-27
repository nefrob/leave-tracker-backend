'''
Tests for the user backend restful api.
'''

import unittest
import requests


HEADERS = {'Content-Type': 'application/json'}

USER_URL = 'http://localhost:5000/user'
USER_LIST_URL = 'http://localhost:5000/user/list'


'''
Helpers
'''
def clear_users():
    '''
    Clear all users
    '''
    return requests.delete(USER_LIST_URL)


def add_user(user_id):
    '''
    Add new user
    '''
    return requests.put(USER_URL + '/' + str(user_id))


class UserTests(unittest.TestCase):
    '''
    User unit tests
    '''

    def test_user_add(self):
        '''
        Add a user
        '''
        clear_users()

        response = add_user(1)
        self.assertEqual(response.status_code, 201)


    def test_user_update(self):
        '''
        Update a user
        '''
        clear_users()

        add_user(1)
        response = add_user(1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'User already exists'})


    def test_user_get(self):
        '''
        Get a user
        '''
        clear_users()

        add_user(1)
        response = requests.get(USER_URL + '/1')
        self.assertEqual(response.status_code, 200)

    
    def test_user_get_nonexistant(self):
        '''
        Get non-existant user
        '''
        clear_users()

        response = requests.get(USER_URL + '/1')
        self.assertEqual(response.status_code, 404)

    
    def test_user_delete(self):
        '''
        Delete a user
        '''
        clear_users()

        add_user(1)
        response = requests.delete(USER_URL + '/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'User deleted'})

    
    def test_user_delete_nonexistant(self):
        '''
        Delete non-existant user
        '''
        clear_users()

        response = requests.delete(USER_URL + '/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'User not found'})


class UserListTests(unittest.TestCase):
    '''
    User list unit tests
    '''
    def test_user_list_get_empty(self):
        '''
        Get empty user list
        '''
        clear_users()

        response = requests.get(USER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


    def test_user_list_get(self):
        '''
        Get all users
        '''
        clear_users()

        add_user(1)
        response = requests.get(USER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)


    def test_user_list_delete(self):
        '''
        Delete all users
        '''
        clear_users()

        add_user(1)
        response = requests.delete(USER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': '1 user(s) deleted'})


if __name__ == '__main__':
    unittest.main()
