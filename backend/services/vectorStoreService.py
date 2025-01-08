# import weaviate

# class VectorStoreService:
#     def __init__(self, url):
#         self.client = weaviate.Client(url)

#     def add_document(self, text, embedding):
#         self.client.data_object.create(
#             {
#                 "text": text,
#                 "embedding": embedding,
#             },
#             class_name="Document",
#         )

#     def search_similar(self, embedding, top_k=5):
#         return self.client.query.get(
#             "Document", ["text"]
#         ).with_near_vector({"vector": embedding}).with_limit(top_k).do()
