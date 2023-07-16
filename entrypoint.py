import dotenv
from src.lambda_function import lambda_handler
import json

dotenv.load_dotenv()
if __name__ == "__main__":
    event_json=json.loads('{"symbol":"TWTR","user_id":"3292378430"}')
    lambda_handler(event=event_json, context=None)
