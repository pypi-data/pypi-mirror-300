import unittest

from lambdarepy.response import Response

from tests.test_data import *

class TestEvent(unittest.TestCase):
    def test_Response_valid(self):
        expected_result = fake_response

        actual_result = Response(message=fake_response_message, data=fake_response_data).to_response()
        
        with self.subTest():
            self.assertEqual(expected_result, actual_result)

