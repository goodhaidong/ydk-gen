#  ----------------------------------------------------------------
# Copyright 2016 Cisco Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------

"""test_restconf_provider.py
RestconfServiceProvider test
"""
from __future__ import absolute_import

import os
import unittest

from ydk.providers import RestconfServiceProvider
from ydk.types import EncodingFormat
from ydk.path import Repository
from ydk.path import Codec


class SanityTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Need to keep a local reference for repo to keep it alive
        repo_path = os.path.dirname(__file__)
        repo_path = os.path.join(repo_path, '..', '..', '..', 'cpp', 'core', 'tests', 'models')
        self.repo = Repository(repo_path)
        self.restconf_provider = RestconfServiceProvider(self.repo, 'localhost', 'admin', 'admin', 12306, EncodingFormat.JSON)

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_del_read(self):
        root_schema = self.restconf_provider.get_root_schema()
        runner = root_schema.create_datanode('ydktest-sanity:runner', '')

        delete_rpc = root_schema.create_rpc('ydk:delete')
        codec_service = Codec()

        json = codec_service.encode(runner, EncodingFormat.JSON, False)
        delete_rpc.get_input_node().create_datanode('entity', json)
        delete_rpc(self.restconf_provider)

        runner.create_datanode('ytypes/built-in-t/number8', '3')
        json = codec_service.encode(runner, EncodingFormat.JSON, False)
        self.assertNotEqual(json, '')
        create_rpc = root_schema.create_rpc('ydk:create')
        create_rpc.get_input_node().create_datanode('entity', json)

        read_rpc = root_schema.create_rpc('ydk:read')
        runner_read = root_schema.create_datanode('ydktest-sanity:runner', '')

        json = codec_service.encode(runner_read, EncodingFormat.JSON, False)
        self.assertNotEqual(json, '')
        read_rpc.get_input_node().create_datanode('filter', json)

        read_rpc(self.restconf_provider)

        runner = root_schema.create_datanode('ydktest-sanity:runner', '')
        number8 = runner.create_datanode('ytypes/built-in-t/number8', '5')

        json = codec_service.encode(runner, EncodingFormat.JSON, False)
        self.assertNotEqual(json, '')

        update_rpc = root_schema.create_rpc('ydk:update')
        update_rpc.get_input_node().create_datanode('entity', json)
        update_rpc(self.restconf_provider)


if __name__ == '__main__':
    import sys
    suite = unittest.TestLoader().loadTestsFromTestCase(SanityTest)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
