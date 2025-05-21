import os
import re
import fitz  # PyMuPDF
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document

class LocalEmbedding(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

def clean_html(raw_html):
    return re.sub(r'<[^>]+>', '', raw_html)

def extract_pdf_text(folder="assets"):
    combined = ""
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            with fitz.open(os.path.join(folder, file)) as doc:
                for page in doc:
                    combined += page.get_text()
    return [combined[i:i+400] for i in range(0, len(combined), 400)]

def prepare_embeddings(json_data, folder="assets", index_path="assets/faiss_index"):
    if os.path.exists(index_path):
        return FAISS.load_local(index_path, LocalEmbedding(), allow_dangerous_deserialization=True)

    # Parse JSON
    chunks = []
    for item in json_data["ResponseObject"]["key_features"]:
        text = f"{item['kf_name']}: {clean_html(item['kf_details'])}"
        chunks.append(text)

    # Parse PDFs
    chunks += extract_pdf_text(folder)

    # Create FAISS vectorstore
    docs = [Document(page_content=chunk) for chunk in chunks]
    embedder = LocalEmbedding()
    vectorstore = FAISS.from_documents(docs, embedder)
    vectorstore.save_local(index_path)
    return vectorstore

def retrieve_context(query, vectorstore, k=4):
    return [doc.page_content for doc in vectorstore.similarity_search(query, k=k)]
