from lambdarepy.event import EventFactory

escaped_body = "{\"attr1\": \"value1\"}"
unescaped_body = {"attr1": "value1"}
fake_api_gw_event = {"body": f"{escaped_body}"}
fake_sqs_event = {"Records": [{"body": f"{escaped_body}"}]}
fake_invalid_event = {}
fake_ef_api_gw = EventFactory(fake_api_gw_event)
fake_ef_sqs = EventFactory(fake_sqs_event)
fake_ef_invalid = EventFactory(fake_invalid_event)
fake_exception_message = f"""An invalid event was provided {fake_invalid_event}\n
Valid input must follow one of these schemas:"""

from lambdarepy.response import Response
from unittest.mock import Mock

fake_response_message = "This is a fake message"
fake_response_data = Mock()

fake_error_body_content = {
    "error": True,
    "message": fake_response_message,
    "data": fake_response_data
}

fake_no_error_body_content = {
    "error": False,
    "message": fake_response_message,
    "data": fake_response_data
}

error_response = Response(
    message=fake_response_message,
    status_code=500,
    data=fake_response_data
)

no_error_response = Response(
    message=fake_response_message,
    data=fake_response_data
)

fake_response = {
    "statusCode": 200,
    "body": fake_no_error_body_content
}