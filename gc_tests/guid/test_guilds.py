# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-2-22
#

import unittest
from gc_tests import BasicTestCase
from guildconnections.common.tools.env import ResourceLoader
import StringIO

class TestGuide(BasicTestCase):
    """ """


    formdata = dict(
        name='Guide',
        url='http://www.google.com',
        description='This is a test guide',
        founded_on='2013-06-06 00:00:00',
        min_age_required=18,
        gender_required='M',
        play_time_required='8',
        play_type='type 1',
        weekly_play_time='20',
        timezone='8',
        prime_time_from='12',
        prime_time_to='16',
        previous_games='',
        voice='1',
    )

    def post(self, logo=None):
        to_post = self.formdata.copy()
        if logo:
            to_post['logo'] = logo
            return self.client.post(self.bp_guide_path, data=to_post)
        return self.request('post', self.bp_guide_path, data=to_post)


    def test_post(self):
        resoure = ResourceLoader.get().get_resoure('upload.jpg')
        with open(resoure.path, 'rb') as f:
            response = self.post(logo=(StringIO.StringIO(f.read()), 'logo.jpg'))
            guide = self.get_result(response)
            self.assertEqual(guide['url'], self.formdata['url'])
            self.assertEqual(guide['description'], self.formdata['description'])
            self.assertEqual(guide['founded_on'], self.formdata['founded_on'])


    def test_put(self):
        # post a guide first
        guide = self.post()

        guide['name'] = 'Changed name'
        guide['timezone'] = '2'

        modified = self.request('put', self.bp_guide_path + guide['_id'], data=guide)
        self.assertEqual(modified['_id'], guide['_id'])
        self.assertEqual(modified['name'], 'Changed name')
        self.assertEqual(modified['timezone'], 2)



    def test_delete(self):
        response = self.request('delete', self.bp_guide_path, return_response=True)
        self.assert405(response)

        guide = self.post()
        self.request('delete', self.bp_guide_path + guide['_id'])

        # then we try to get the guide
        response = self.request('get', self.bp_guide_path + guide['_id'], return_response=True)
        self.assert404(response)
        self.assert_failed_result(response, 404)


    def test_get_list(self):
        # post two questions
        self.post()
        guide = self.post()
        where = {
            'id': guide['_id'],
        }
        self.get_list(self.bp_guide_path, where=where, expect_size=1)
        paper_list = self.get_list(self.bp_guide_path,)

        # we delete one
        self.request('delete', self.bp_guide_path + guide['_id'])
        self.get_list(self.bp_guide_path, where=where, expect_size=0)
        # left one
        self.get_list(self.bp_guide_path, expect_size=len(paper_list) - 1)



    def test_get(self):
        guide = self.post()
        result = self.request('get', self.bp_guide_path + guide['_id'])
        assert isinstance(result, dict)
        self.assertEqual(result['_id'], guide['_id'])


if __name__ == "__main__":
    unittest.main()
