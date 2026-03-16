# from langchain_community.llms import Ollama
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings


# class AgroChatEngine:

#     def __init__(self, predicted_class):

#         # Save disease context
#         self.predicted_class = predicted_class

#         # Load embeddings
#         self.embeddings = HuggingFaceEmbeddings(
#             model_name="all-MiniLM-L6-v2"
#         )

#         # Load vector DB
#         self.vectorstore = Chroma(
#             persist_directory="app/rag/vector_db",
#             embedding_function=self.embeddings
#         )

#         # Load LLM (Ollama)
#         self.llm = Ollama(model="llama3")

#         # Create memory
#         self.memory = ConversationBufferMemory(
#             memory_key="chat_history",
#             return_messages=True
#         )

#         # Create Conversational RAG chain
#         self.chain = ConversationalRetrievalChain.from_llm(
#             llm=self.llm,
#             retriever=self.vectorstore.as_retriever(),
#             memory=self.memory
#         )

#     def ask(self, user_question):

#         # Inject disease context automatically
#         enhanced_question = f"""
#         The detected disease is {self.predicted_class}.
#         Farmer question: {user_question}
#         """

#         response = self.chain.invoke({
#             "question": enhanced_question
#         })

#         return response["answer"]



import os
from app.utils.knowledge_parser import parse_document
from app.utils.question_mapper import map_question_to_section


class AgroChatEngine:

    def __init__(self, predicted_class):

        self.predicted_class = predicted_class

        disease_file = predicted_class.replace("___", "_") + ".txt"

        self.file_path = os.path.join(
            "app/rag/documents",
            disease_file
        )

        self.sections = parse_document(self.file_path)

    def ask(self, question):

        section = map_question_to_section(question)

        if section in self.sections:

            return f"{section}:\n\n{self.sections[section]}"

        return "Information not available."