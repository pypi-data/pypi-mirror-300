import unittest
from unittest.mock import patch, Mock

from lambdarepy.event import EventFactory, ParseApiGatewayEvent, ParseSqsMessage, InvalidEventException

from tests.test_data import *

class TestEvent(unittest.TestCase):
    def test___init__(self):
        expected_result = Mock(event = fake_api_gw_event)
        actual_result = fake_ef_api_gw
        
        with self.subTest():
            self.assertEqual(expected_result.event, actual_result.event)

    @patch.object(EventFactory, 'is_sqs')
    @patch.object(EventFactory, 'is_api_gw')
    def test_get_event_parser(self, mock_is_api_gw, mock_is_sqs):
        mock_is_api_gw.return_value = True
        actual_result = fake_ef_api_gw.get_event_parser()
        
        with self.subTest():
            self.assertIsInstance(actual_result, ParseApiGatewayEvent)

        mock_is_api_gw.return_value = False
        mock_is_sqs.return_value = True
        actual_result = fake_ef_sqs.get_event_parser()
        
        with self.subTest():
            self.assertIsInstance(actual_result, ParseSqsMessage)

        mock_is_sqs.return_value = False

        expected_result = f"An invalid event was provided {fake_invalid_event}"
        
        with self.subTest():
            with self.assertRaises(InvalidEventException) as actual_result:
                fake_ef_invalid.get_event_parser()
            self.assertIn(expected_result, actual_result.exception.message)

    @patch('lambdarepy.event.json.loads')
    def test_is_api_gw(self, mock_loads):
        mock_loads.side_effect = KeyError("body")
        actual_result = fake_ef_invalid.is_api_gw()
        
        with self.subTest():
            self.assertFalse(actual_result)
    
        mock_loads.side_effect = None
        actual_result = fake_ef_api_gw.is_api_gw()
        
        with self.subTest():
            self.assertTrue(actual_result)

    @patch('lambdarepy.event.json.loads')
    def test_is_sqs(self, mock_loads):
        mock_loads.side_effect = KeyError("Records")
        actual_result = fake_ef_invalid.is_sqs()
        
        with self.subTest():
            self.assertFalse(actual_result)
    
        mock_loads.side_effect = None
        actual_result = fake_ef_sqs.is_sqs()
        
        with self.subTest():
            self.assertTrue(actual_result)

class TestParseApiGatewayEvent(unittest.TestCase):
    def test___init__(self):
        expected_result = Mock(event = unescaped_body)
        actual_result = ParseApiGatewayEvent(fake_api_gw_event)
        
        with self.subTest():
            self.assertEqual(expected_result.event, actual_result.event)

class TestParseSqsMessage(unittest.TestCase):
    def test___init__(self):
        expected_result = Mock(event = unescaped_body)
        actual_result = ParseSqsMessage(fake_sqs_event)
        
        with self.subTest():
            self.assertEqual(expected_result.event, actual_result.event)

class TestInvalidEventException(unittest.TestCase):
    def test___init__(self):
        expected_result = f"""An invalid event was provided {fake_invalid_event}"""         

        actual_result = InvalidEventException(fake_invalid_event)
        
        with self.subTest():
            self.assertIn(expected_result, actual_result.message)