# import requests

# class TextGenerationService:
#     def __init__(self, api_url, api_key):
#         self.api_url = api_url
#         self.api_key = api_key

#     def generate_response(self, query, context):
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json",
#         }
#         payload = {"query": query, "context": context}
#         response = requests.post(f"{self.api_url}/generate", json=payload, headers=headers)
#         if response.status_code == 200:
#             return response.json().get("response")
#         else:
#             raise Exception(f"Error in text generation: {response.text}")
