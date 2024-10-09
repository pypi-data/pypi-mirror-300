import requests

class SQLDetectionClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://hacking-shield-api.onrender.com"  # Your actual API URL

    def detect_harmful_sql(self, sql_query):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Include the API key in the data payload
        data = {
            "query": sql_query,
            "api_key": self.api_key  # Include the API key in the payload
        }

        try:
            # Send the request
            response = requests.post(f"{self.base_url}/detect_sql", headers=headers, json=data)

            # Print the request details
            print(f"Request URL: {response.url}")
            print(f"Request Data: {data}")
            print(f"Response Status Code: {response.status_code}")

            # Check for HTTP errors
            response.raise_for_status()  # Raise an error for bad responses

            # Parse and return the JSON response
            return response.json()  # Assuming the response is in JSON format

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Detailed HTTP error
            if response.content:
                print("Response Content:", response.content.decode())  # Print response content for further insight
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