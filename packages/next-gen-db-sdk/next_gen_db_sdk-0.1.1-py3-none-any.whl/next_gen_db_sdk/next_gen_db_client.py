import requests
from .exceptions import NextGenDBError, NotFoundError

class NextGenDBClient:
    def __init__(self, base_url: str):
        """
        Initialize the NextGenDBClient.

        Args:
            base_url (str): The base URL of the next-gen-db server (e.g., 'http://localhost:8047').
        """
        self.base_url = base_url.rstrip("/")

    # --- Document Operations ---

    def create_document(self, key: str, document: dict):
        """Creates a new document in the database."""
        url = f"{self.base_url}/document/{key}"
        response = requests.post(url, json=document)
        self._handle_response(response)
        return response.json()

    def get_document(self, key: str):
        """Retrieves a document from the database."""
        url = f"{self.base_url}/document/{key}"
        response = requests.get(url)
        self._handle_response(response)
        return response.json()

    def update_document(self, key: str, document: dict):
        """Updates an existing document in the database."""
        url = f"{self.base_url}/document/{key}"
        response = requests.put(url, json=document)
        self._handle_response(response)
        return response.json()

    def delete_document(self, key: str):
        """Deletes a document from the database."""
        url = f"{self.base_url}/document/{key}"
        response = requests.delete(url)
        self._handle_response(response)
        return response.json()

    # --- Graph Operations ---

    def add_node(self, node_id: str, properties: dict):
        """Adds a new node to the graph."""
        url = f"{self.base_url}/graph/node/{node_id}"
        response = requests.post(url, json=properties)
        self._handle_response(response)
        return response.json()

    def get_node(self, node_id: str):
        """Retrieves a node from the graph."""
        url = f"{self.base_url}/graph/node/{node_id}"
        response = requests.get(url)
        self._handle_response(response)
        return response.json()

    def add_edge(self, node1: str, node2: str, relation: str):
        """Adds a relationship (edge) between two nodes in the graph."""
        url = f"{self.base_url}/graph/edge"
        response = requests.post(url, json={"node1": node1, "node2": node2, "relation": relation})
        self._handle_response(response)
        return response.json()

    def get_edge(self, node1: str, node2: str):
        """Retrieves a relationship (edge) between two nodes in the graph."""
        url = f"{self.base_url}/graph/edge?node1={node1}&node2={node2}"
        response = requests.get(url)
        self._handle_response(response)
        return response.json()

    # --- Internal Helper Functions ---

    def _handle_response(self, response):
        """Handle response from the server, raising errors if necessary."""
        if response.status_code == 404:
            raise NotFoundError(response.json().get("detail", "Resource not found"))
        elif response.status_code >= 400:
            raise NextGenDBError(response.json().get("detail", "An error occurred"))


