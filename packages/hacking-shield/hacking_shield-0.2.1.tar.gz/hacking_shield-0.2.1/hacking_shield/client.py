import requests

class SQLDetectionClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://hacking-shield-api.onrender.com"  # Replace with your actual API URL for testing

    def detect_harmful_sql(self, sql_query):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "query": sql_query
        }

        try:
            # Sending POST request to the API endpoint
            response = requests.post(f"{self.base_url}/detect_sql", headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Assuming the response is in JSON format

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Detailed HTTP error
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")  # Connection-related errors
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")  # Timeout-related errors
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")  # General request errors
            return None
