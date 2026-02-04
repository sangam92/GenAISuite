import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load vector store
vector_store = FAISS.load_local(
    "sop_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# SOP-only prompt
prompt = ChatPromptTemplate.from_template("""
You are an SOP assistant.
Answer ONLY using the SOP content below.
If the answer is not found, say:
"I could not find this information in the SOP."

SOP Content:
{context}

Question:
{question}
""")

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.8
)

# RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Ask loop
while True:
    q = input("\nAsk SOP question (or 'exit'): ")
    if q.lower() == "exit":
        break

    answer = rag_chain.invoke(q)
    print("\nAnswer:", answer)
