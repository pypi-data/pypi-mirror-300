import requests
from typing import List, Dict, Union, Optional
from .exceptions import SyzgyException
from .models import Document, SearchResult, Collection

class SyzgyClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, **kwargs)
        if response.status_code >= 400:
            error_message = f"HTTP {response.status_code}: {response.reason}"
            try:
                error_body = response.json()
                error_message += f"\nResponse body: {error_body}"
            except ValueError:
                error_message += f"\nResponse body: {response.text}"
            raise SyzgyException(error_message)
        try:
            return response.json()
        except ValueError:
            raise SyzgyException(f"Invalid JSON response: {response.text}")

    def create_collection(self, name: str, vector_size: int, quantization: int, distance_function: str) -> Collection:
        data = {
            "name": name,
            "vector_size": vector_size,
            "quantization": quantization,
            "distance_function": distance_function
        }
        result = self._request("POST", "/api/v1/collections", json=data)
        # Use the parameters passed in to construct the Collection object
        return Collection(self, name, 0, vector_size, quantization, distance_function)

    def get_collections(self) -> List[Collection]:
        result = self._request("GET", "/api/v1/collections")
        return [Collection(self, c["collection_name"], c["document_count"], c["dimension_count"], c["quantization"], c["distance_function"]) for c in result]

    def get_collection(self, name: str) -> Collection:
        result = self._request("GET", f"/api/v1/collections/{name}")
        return Collection(self, name, result["document_count"], result["dimension_count"], result["quantization"], result["distance_function"])

    def delete_collection(self, collection_name: str) -> Dict:
        return self._request("DELETE", f"/api/v1/collections/{collection_name}")

class Collection:
    def __init__(self, client: SyzgyClient, collection_name: str, document_count: int, dimension_count: int, quantization: int, distance_function: str):
        self.client = client
        self.collection_name = collection_name
        self.document_count = document_count
        self.dimension_count = dimension_count
        self.quantization = quantization
        self.distance_function = distance_function

    def insert_documents(self, documents: List[Document]) -> Dict:
        data = [doc.to_dict() for doc in documents]
        return self.client._request("POST", f"/api/v1/collections/{self.collection_name}/records", json=data)

    def update_document_metadata(self, document_id: int, metadata: Dict) -> Dict:
        data = {"metadata": metadata}
        return self.client._request("PUT", f"/api/v1/collections/{self.collection_name}/records/{document_id}/metadata", json=data)

    def delete_document(self, document_id: int) -> Dict:
        return self.client._request("DELETE", f"/api/v1/collections/{self.collection_name}/records/{document_id}")

    def search(self, vector: Optional[List[float]] = None, text: Optional[str] = None,
               k: Optional[int] = None, radius: Optional[float] = None, limit: Optional[int] = None,
               offset: Optional[int] = None, precision: Optional[str] = None,
               filter: Optional[str] = None) -> List[SearchResult]:
        data = {
            "vector": vector,
            "text": text,
            "k": k,
            "radius": radius,
            "limit": limit,
            "offset": offset,
            "precision": precision,
            "filter": filter
        }
        data = {k: v for k, v in data.items() if v is not None}
        result = self.client._request("POST", f"/api/v1/collections/{self.collection_name}/search", json=data)
        return [SearchResult(**item) for item in result["results"]]

    def get_document_ids(self) -> List[int]:
        result = self.client._request("GET", f"/api/v1/collections/{self.collection_name}/ids")
        return result
