class Response():
    def __init__(self, message, status_code=200, error=False, data=None):
        self.message = message
        self.status_code = status_code
        self.error = error
        self.data=data
        
        if self.status_code != 200:
            self.error = True
            self.data = self.data

        self.body_content = {
            "error": self.error,
            "message": message,
            "data": self.data
        }

    def to_response(self):
        self.response = {
            "statusCode": self.status_code,
            "body": self.body_content
        }
        
        print(f"Formed response {self.response}")

        return self.response