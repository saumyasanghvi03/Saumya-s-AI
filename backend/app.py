import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore # Updated import
from langchain.chains import RetrievalQA
import pinecone

# Load environment variables
load_dotenv()

# --- Initialize Flask App ---
app = Flask(__name__)

# --- Initialize Pinecone ---
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not all([pinecone_api_key, pinecone_environment, openai_api_key]):
    raise ValueError("Missing one or more environment variables (PINECONE_API_KEY, PINECONE_ENVIRONMENT, OPENAI_API_KEY). Please ensure they are set in your .env file.")

# Initialize Pinecone client (v3.x.x)
pc = pinecone.Pinecone(api_key=pinecone_api_key)

index_name = "financial-literacy-widget" # Same index name as in populate_pinecone.py

# --- Initialize Langchain Components ---
# Embeddings model
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# Check if index exists before trying to use it as a vector store
if index_name not in pc.list_indexes().names:
    # This is a runtime check. The index should ideally be created by populate_pinecone.py
    # You might want to handle this more gracefully, e.g., by returning an error to the client
    # or by attempting to run the population script if feasible and safe.
    raise ValueError(f"Pinecone index '{index_name}' does not exist. Please run populate_pinecone.py first.")

# Pinecone as Vector Store
vectorstore = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)

# Language Model (LLM)
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name='gpt-3.5-turbo', # Or your preferred model
    temperature=0.7 # Adjust for creativity vs. factuality
)

# RetrievalQA Chain
# This chain will retrieve relevant documents from Pinecone and use them to answer questions
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", # "stuff" is a simple method; others include "map_reduce", "refine"
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}), # Retrieve top 3 relevant chunks
    return_source_documents=True # Optionally return source documents
)

# --- API Endpoints ---
@app.route('/')
def hello():
    return "Hello from Flask Backend! The Financial Literacy Chat API is running."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Get response from the QA chain
        result = qa_chain({"query": user_message})

        response_data = {
            "answer": result.get("result"),
            "source_documents": [
                {"content": doc.page_content, "metadata": doc.metadata}
                for doc in result.get("source_documents", [])
            ]
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        # It's good practice to log the error to a file or monitoring service
        return jsonify({"error": "An error occurred processing your request."}), 500

if __name__ == '__main__':
    # Ensure the app runs on a port that's accessible, e.g., 5000 or 5001
    # For development, debug=True is fine. For production, use a proper WSGI server.
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5001)), debug=True)
