from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.vectorstores import FAISS
import os
import glob
import logging

# Enable logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

directories = ["Docs"]
def extract_metadata_from_filename(filename):
    base_name = os.path.basename(filename).lower().replace(".txt", "")
    parts = base_name.split("_")

    metadata = {}

    # Identify known product categories
    known_categories = ["iphone", "ipad", "macbook", "apple", "watch", "homepod", "airpods"]

    for cat in known_categories:
        if cat in parts:
            metadata["category"] = cat.capitalize()
            break

    if "models" in parts:
        metadata["type"] = "models"
    elif "specs" in parts:
        metadata["type"] = "specs"
    elif "products" in parts:
        metadata["type"] = "overview"

    return metadata


def load_documents(directory="Docs", use_cache=True):
    if use_cache and os.path.exists("vector_store/index.faiss"):
        print("Loading cached vector store...")
        return FAISS.load_local("vector_store", HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))

    docs = []
    for path in glob.glob(os.path.join(directory, "*.txt")):
        loader = TextLoader(path)  
        metadata = extract_metadata_from_filename(path)
        for doc in loader.load():
            doc.metadata.update(metadata)
            docs.append(doc)
    logging.info(f"Loaded {len(docs)} documents from {directory}.")
    # Filter out noise before chunking
    docs = [d for d in docs if not any(x in d.page_content.lower() for x in ["regulatory", "safety", "disposal", "accessibility"])]
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    db = FAISS.from_documents(chunks, HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
    db.save_local("vector_store")
    return db