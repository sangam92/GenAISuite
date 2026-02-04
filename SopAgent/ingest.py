import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

from langchain_community.embeddings import HuggingFaceEmbeddings


load_dotenv()





# Load PDF
loader = PyPDFLoader("data/bookML.pdf")
documents = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)
chunks = splitter.split_documents(documents)

# Gemini embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Store vectors
vector_store = FAISS.from_documents(chunks, embeddings)
vector_store.save_local("sop_index")

print("✅ Gemini-based SOP ingestion done")
