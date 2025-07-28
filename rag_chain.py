import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

# Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Vector DB
vectorstore = Chroma(
    collection_name="changi_airport_collection",
    persist_directory="./chroma_db",
    embedding_function=embedding_model,
)

# LLM

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3,
    convert_system_message_to_human=True
)


# RAG Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=False
)

while True:
    user_input = input("Ask something about Changi Airport: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = qa_chain.run(user_input)
    print("Bot:", response)
