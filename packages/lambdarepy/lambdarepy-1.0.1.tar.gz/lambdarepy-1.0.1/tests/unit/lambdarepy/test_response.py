import unittest

from tests.test_data import *

class TestResponse(unittest.TestCase):
    def test___init__(self):
        expected_result = Mock(
            message=fake_response_message,
            status_code=500,
            error=True,
            data=fake_response_data,
            body_content = fake_error_body_content
        )

        actual_result = error_response
        
        with self.subTest():
            self.assertEqual(expected_result.message, actual_result.message)
            self.assertEqual(expected_result.status_code, actual_result.status_code)
            self.assertTrue(actual_result.error)
            self.assertEqual(expected_result.data, actual_result.data)
            self.assertEqual(expected_result.body_content, actual_result.body_content)

        expected_result = Mock(
            message=fake_response_message,
            status_code=200,
            error=False,
            data=fake_response_data,
            body_content = fake_no_error_body_content
        )

        actual_result = no_error_response
        
        with self.subTest():
            self.assertEqual(expected_result.message, actual_result.message)
            self.assertEqual(expected_result.status_code, actual_result.status_code)
            self.assertFalse(actual_result.error)
            self.assertEqual(expected_result.data, actual_result.data)
            self.assertEqual(expected_result.body_content, actual_result.body_content)

    def test_to_response(self):
        expected_result = {
            'statusCode': 200, 
            'body': 
            {
                'error': False,
                'message': 'This is a fake message',
                'data': fake_response_data
            }
        }
        actual_result = no_error_response.to_response()

        with self.subTest():
            self.assertEqual(expected_result, actual_result)

