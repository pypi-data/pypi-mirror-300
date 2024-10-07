import json

class EventFactory():
    def __init__(self, event):
        self.event = event

    def get_event_parser(self):
        if self.is_api_gw():
            return ParseApiGatewayEvent(self.event)
        
        elif self.is_sqs():
            return ParseSqsMessage(self.event)
        
        else:
            raise InvalidEventException(self.event)
            
    def is_api_gw(self):
        try:
            json.loads(self.event["body"])
            print("API Gateway event identified")

            return True
        except (TypeError, KeyError):
            return False

    def is_sqs(self):
        try:
            json.loads(self.event["Records"][0]['body'])
            print("SQS message identified")

            return True
        except (TypeError, KeyError):
            return False

class ParseApiGatewayEvent():
    def __init__(self, event):
        self.event = json.loads(event["body"])
        print(f"Parsed API Gateway event {self.event}")
    
class ParseSqsMessage():
    def __init__(self, event):
        self.event = json.loads(event["Records"][0]['body'])
        print(f"Parsed SQS message {self.event}")

class InvalidEventException(Exception):
    def __init__(self, event):
        self.valid_api_gw_schema = {
            "properties": {
                "body": {
                    "type": "string"
                }
            }
        }
        self.valid_sqs_schema = {"properties": 
            {
                "Records": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "body": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }

        self.message = f"""An invalid event was provided {event}           
        \nValid input must follow one of these schemas:       
        \n{self.valid_api_gw_schema}
        \n{self.valid_sqs_schema}"""