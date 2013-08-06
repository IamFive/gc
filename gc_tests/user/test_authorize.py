# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-15
#
from gc_tests import BasicTestCase
from guildconnections import error_code
from guildconnections.common import clear_db, init_db
import unittest


class TestAuth(BasicTestCase):

    get_me_path = BasicTestCase.bp_profile_path + 'me'

    def setUp(self):
        clear_db()
        init_db()

    def test_signup(self):
        """ testcase for signup """
        # test for wrong parameter
        response = self.request('post', self.bp_authorize_path + 'signup',
                                return_response=True)
        self.assert_error_code(response, error_code.ENP_REQUIRED)

        formdata = dict(email='simple@abc.com')
        response = self.request('post', self.bp_authorize_path + 'signup',
                                data=formdata, return_response=True)
        self.assert_error_code(response, error_code.ENP_REQUIRED)

        formdata = dict(email='simple@abc.com', password='passwd',
                        name='simple')
        result = self.request('post', self.bp_authorize_path + 'signup',
                              data=formdata)
        self.assertEqual(result.get('email'), formdata.get('email'))

    def test_login(self):
        """ """
        def assert_fail_login(data):
            response = self.request('post',
                                    self.bp_authorize_path + 'login',
                                    data=data,
                                    return_response=True)
            self.assert_error_code(response, error_code.LOGIN_FAILED)

        # request some private resource before login
        # it should return 401
        response = self.request('get', self.get_me_path, return_response=True)
        self.assert401(response)

        # then we login with no email and passwd
        assert_fail_login({})

        # then we login with correct email but no passwd
        data = dict(email=self.DFT_USER_EMAIL,)
        assert_fail_login(data)

        # then we login with correct email but wrong passwd
        data = dict(email=self.DFT_USER_EMAIL, password='wrongpass')
        assert_fail_login(data)

        # then we login with no email
        data = dict(password=self.DFL_USER_PASSWD)
        assert_fail_login(data)

        # then we signup one user and login
        data = dict(email='login@abc.com', password='passwd', name='login')
        self.request('post', self.bp_authorize_path + 'signup', data=data)
        result = self.request('post', self.bp_authorize_path + 'login', data)
        self.assertTrue(result)

        # after login, we visit some private resources
        result = self.request('get', self.get_me_path)
        self.assertEqual('login@abc.com', result.get('email'))

    def test_logout(self):

        # login first
        data = dict(email='login@abc.com', password='passwd', name='login')
        self.request('post', self.bp_authorize_path + 'signup', data=data)
        result = self.request('post', self.bp_authorize_path + 'login', data)
        self.assertTrue(result)

        # after login, we visit some private resources
        result = self.request('get', self.get_me_path)
        self.assertEqual('login@abc.com', result.get('email'))

        # then we logout
        result = self.request('get', self.bp_authorize_path + 'logout')
        self.assertTrue(result)

        # then get some private resource, should return 401
        response = self.request('get', self.get_me_path, return_response=True)
        self.assert401(response)


if __name__ == "__main__":
    unittest.main()
