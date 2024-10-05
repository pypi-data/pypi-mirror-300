import requests
import time
import logging

# Custom Exceptions
class CirclemindError(Exception):
    """Base class for exceptions in the Circlemind API."""
    pass

# Circlemind API Client
class Circlemind:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {'apiKey': self.api_key}
        logging.basicConfig(level=logging.INFO)

    def add_memory(self, memory: str, memory_id: str = None):
        """Add a new memory."""
        url = f"{self.base_url}/memory"
        payload = self._create_memory_payload(memory, memory_id)
        
        response = self._send_post_request(url, payload)
        return response

    def get_memories(self, query: str, max_items: int = 25):
        """Retrieve a list of memories based on a query."""
        url = f"{self.base_url}/reasoning"
        payload = self._create_query_payload(query)
        
        response = self._send_post_request(url, payload)
        memories = self._wait_for_response(response)
        
        return memories[:max_items]

    def _create_memory_payload(self, memory: str, memory_id: str):
        """Create payload for adding memory."""
        return {"memory": memory, "memoryId": memory_id}

    def _create_query_payload(self, query: str):
        """Create payload for querying memories."""
        return {"query": query}

    def _send_post_request(self, url: str, payload: dict):
        """Send a POST request to the given URL with the provided payload."""
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.HTTPError as e:
            logging.error(f"Failed to send POST request: {e}")
            raise CirclemindError(f"Error adding memory: {str(e)}")

    def _wait_for_response(self, initial_response):
        """Poll the API until the memory processing is done."""
        status = "CREATED"
        request_id = initial_response.get("requestId")
        request_time = initial_response.get("requestTime")

        while status not in ["DONE", "FAILED"]:
            logging.info("Waiting for response...")
            time.sleep(1)
            response = self._send_get_request(request_id, request_time)
            status = response.get("status", "")
        
        if status == "FAILED":
            raise CirclemindError("Fetching memories failed.")

        return response.get("memories", [])

    def _send_get_request(self, request_id: str, request_time: str):
        """Send a GET request to check the status of the processing."""
        url = f"{self.base_url}/reasoning"
        params = {"requestId": request_id, "requestTime": request_time}
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            logging.error(f"Failed to send GET request: {e}")
            raise CirclemindError(f"Error fetching memories: {str(e)}")


if __name__ == '__main__':
    cm = Circlemind("YOUR_API_KEY", "http://ec2-3-81-205-157.compute-1.amazonaws.com")

    cm.get_memories("What animals do I like?")

