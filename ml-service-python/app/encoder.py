# # ml-service-python/app/encoder.py
# from sentence_transformers import SentenceTransformer
# import os

# # model selection - swap with clinical model when available
# MODEL_NAME = os.environ.get("SBERT_MODEL", "all-mpnet-base-v2")
# print("Loading encoder model:", MODEL_NAME)
# _model = SentenceTransformer(MODEL_NAME)

# def encode(texts, batch_size=32):
#     """
#     texts: list[str] -> numpy array embeddings
#     """
#     return _model.encode(texts, batch_size=batch_size, show_progress_bar=False, normalize_embeddings=True)

# # from sentence_transformers import SentenceTransformer
# # import numpy as np

# # model = SentenceTransformer('all-MiniLM-L6-v2')

# # def encode(texts, batch_size=32):
# #     embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
# #     return embeddings