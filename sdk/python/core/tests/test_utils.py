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

"""test_utils.py

Utility function for test cases.
"""
import re
import unittest
from argparse import ArgumentParser

import sys
if sys.version_info > (3,):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


def assert_with_error(pattern, ErrorClass):
    def assert_with_pattern(func):
        def helper(self, *args, **kwargs):
            try:
                func(self)
            except ErrorClass as error:
                res = re.match(pattern, error.message.strip())
                self.assertEqual(res is not None, True)
        return helper
    return assert_with_pattern


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest'):
        super(ParametrizedTestCase, self).__init__(methodName)

    @staticmethod
    def parametrize(testcase_klass, device, non_demand, common_cache):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testcase_klass.hostname = device.hostname
        testcase_klass.username = device.username
        testcase_klass.password = device.password
        testcase_klass.port = device.port
        testcase_klass.protocol = device.scheme
        testcase_klass.non_demand = non_demand
        testcase_klass.common_cache = common_cache
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name))
        return suite


def get_device_info():
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("--non-demand", help="disable on demand model downloading",
                        dest="non_demand", action="store_true")
    parser.add_argument("--common-cache", help="use common cache directory",
                        dest="common_cache", action="store_true")
    parser.add_argument("device", nargs='?',
                        help="NETCONF device (ssh://user:password@host:port)")

    args = parser.parse_args()
    if not args.device:
        args.device = "ssh://admin:admin@127.0.0.1:12022"
    device = urlparse(args.device)
    return device, args.non_demand, args.common_cache
