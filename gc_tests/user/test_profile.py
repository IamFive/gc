# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-5-15
#
import StringIO
from gc_tests import BasicTestCase
import unittest
from guildconnections.common.tools.env import ResourceLoader


class TestAuth(BasicTestCase):

    get_me_path = BasicTestCase.bp_profile_path + 'me'


    def test_me(self):

        self.logout()

        # get before login
        response = self.request('get', self.get_me_path, return_response=True)
        self.assert401(response)

        # login
        self.default_login()

        result = self.request('get', self.get_me_path)
        self.assertEqual(self.DFT_USER_EMAIL, result.get('email'))
        self.assertNotIn('password', result, 'should not return password')
        self.assertNotIn('verify_code', result, 'should not return verify_code')


    def test_post_gamer(self):
        """ test gamer profile post """

        resoure = ResourceLoader.get().get_resoure('upload.jpg')
        with open(resoure.path, 'rb') as f:
            formdata = dict(dob='1900-01-01 00:00:00',
                            gender='M',
                            bio='bio',
                            avg_play_time='6',
                            timezone='8',
                            forum_signature="this is a tail :)",
                            games=["5191a37aafc35816ac6196d1",
                                   "5191a37aafc35816ac6196d2"],
                            find_guide='1',
                            find_for_type='51a0290bafc3581ff8c59f9b',
                            find_for_game='5191a37aafc35816ac6196d1',
                            current_realm='healer',
                            transfer_realm='0',
                            preffered_role='MT',
                            avatar=(StringIO.StringIO(f.read()), 'avatar.jpg'),
                            )

            response = self.client.post(self.bp_profile_path + 'gamer', data=formdata)
            result = self.get_result(response)

            gamer = result.get('gamer')
            self.assertIn('gamer', result)
            self.assertEqual(formdata.get('bio'), gamer.get('bio'))
            self.assertEqual(formdata.get('bio'), gamer.get('bio'))


        # missing games here. find out why.

if __name__ == "__main__":
    unittest.main()
