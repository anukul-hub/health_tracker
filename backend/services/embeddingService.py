# import requests

# class EmbeddingService:
#     def __init__(self, api_url, api_key):
#         self.api_url = api_url
#         self.api_key = api_key

#     def generate_embedding(self, text):
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json",
#         }
#         payload = {"text": text}
#         response = requests.post(f"{self.api_url}/embed", json=payload, headers=headers)
#         if response.status_code == 200:
#             return response.json().get("embedding")
#         else:
#             raise Exception(f"Error in embedding generation: {response.text}")
