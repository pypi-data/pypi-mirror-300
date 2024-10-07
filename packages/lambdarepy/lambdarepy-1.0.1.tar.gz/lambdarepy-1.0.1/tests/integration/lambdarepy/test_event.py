import unittest

from lambdarepy.event import EventFactory, InvalidEventException

from tests.test_data import *

class TestEvent(unittest.TestCase):
    def test_EventFactory_valid(self):
        expected_result = unescaped_body
        actual_result = EventFactory(fake_api_gw_event).get_event_parser()
        
        with self.subTest():
            self.assertEqual(expected_result, actual_result.event)

    def test_EventFactory_invalid(self):
        with self.subTest():
            with self.assertRaises(InvalidEventException):
                EventFactory(fake_invalid_event).get_event_parser()
