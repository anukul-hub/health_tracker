# class RAGService:
#     def __init__(self, embedding_service, vector_store_service, text_generation_service):
#         self.embedding_service = embedding_service
#         self.vector_store_service = vector_store_service
#         self.text_generation_service = text_generation_service

#     def process_query(self, query):
#         # Step 1: Generate embedding for query
#         query_embedding = self.embedding_service.generate_embedding(query)

#         # Step 2: Retrieve relevant documents
#         retrieved_docs = self.vector_store_service.search_similar(query_embedding)

#         # Step 3: Combine context
#         context = " ".join([doc["text"] for doc in retrieved_docs["data"]["Get"]["Document"]])

#         # Step 4: Generate response
#         return self.text_generation_service.generate_response(query, context)
