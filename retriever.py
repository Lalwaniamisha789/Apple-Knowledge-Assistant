import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Import the function from doc_loader
from doc_loader import load_documents

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if not os.path.exists("vector_store/index.faiss"):
        print("Vector store not found. Creating it...")
        db = load_documents()
    else:
        db = FAISS.load_local("vector_store", embeddings, allow_dangerous_deserialization=True)
        print("Vector store loaded from 'vector_store/'")

    return db.as_retriever(search_type="similarity", search_kwargs={"k": 6})

