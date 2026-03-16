from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os


def create_vector_database():

    loader = DirectoryLoader(
        "app/rag/documents",
        glob="*.txt"
    )

    documents = loader.load()

    print("Total TXT files detected:", len(documents))   # ⭐ added

    # Add metadata (disease name)
    for doc in documents:
        filename = os.path.basename(doc.metadata["source"])
        disease_name = filename.replace(".txt", "")
        doc.metadata["disease"] = disease_name

    text_splitter = CharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    docs = text_splitter.split_documents(documents)

    print("Total chunks created:", len(docs))   # ⭐ added

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="app/rag/vector_db"
    )

    vectorstore.persist()

    print("Vector database created successfully")


if __name__ == "__main__":
    create_vector_database()