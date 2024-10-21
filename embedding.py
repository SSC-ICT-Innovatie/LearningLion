from langchain_huggingface import HuggingFaceEmbeddings
import torch

class Embedding:
  embeddings = None
  def __init__(self):
      print("Embedding class initialized")

  def get_embeddings(self):
      return self.embeddings
    
  def setup_embeddings(self):
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    model_name = "textgain/allnli-GroNLP-bert-base-dutch-cased"
    if torch.backends.mps.is_available():
        model_kwargs = {'device': 'mps'}
    elif torch.cuda.is_available():
        model_kwargs = {'device': 'cuda'}
    else:
        model_kwargs = {'device': 'cpu'}
    model_kwargs["trust_remote_code"] = True
    encode_kwargs = {'normalize_embeddings': False}
    self.embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
