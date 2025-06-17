import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore # Updated import
import pinecone

def main():
    load_dotenv()

    # --- Load Environment Variables ---
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_environment = os.getenv("PINECONE_ENVIRONMENT") # Ensure this is set in .env
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not all([pinecone_api_key, pinecone_environment, openai_api_key]):
        print("Error: Missing one or more environment variables (PINECONE_API_KEY, PINECONE_ENVIRONMENT, OPENAI_API_KEY).")
        print("Please ensure they are set in your .env file.")
        return

    # --- Initialize Pinecone ---
    # The old way: pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
    # New way for pinecone-client v3.x.x
    pc = pinecone.Pinecone(api_key=pinecone_api_key) # environment is often not needed here or handled differently

    # --- Define Pinecone Index ---
    index_name = "financial-literacy-widget" # Choose a name for your index

    # Check if the index exists, create if not
    if index_name not in pc.list_indexes().names:
        print(f"Creating index: {index_name}")
        try:
            pc.create_index(
                name=index_name,
                dimension=1536,  # Dimension for OpenAI's text-embedding-ada-002
                metric='cosine',
                spec=pinecone.PodSpec(environment=pinecone_environment) # Specify environment here
            )
            print(f"Index {index_name} created successfully.")
        except Exception as e:
            print(f"Error creating index {index_name}: {e}")
            return
    else:
        print(f"Index {index_name} already exists.")

    # --- Load Documents from the `data` directory (relative to project root) ---
    # Assuming this script is in 'backend/' and data is in '../data/'
    data_dir_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    print(f"Looking for documents in: {os.path.abspath(data_dir_path)}")

    try:
        loader = DirectoryLoader(
            data_dir_path,
            glob="*.txt", # Load .txt files
            loader_cls=TextLoader,
            show_progress=True,
            use_multithreading=True
        )
        documents = loader.load()
        if not documents:
            print(f"No documents found in {data_dir_path}. Please add some .txt files.")
            return
        print(f"Loaded {len(documents)} documents.")
    except Exception as e:
        print(f"Error loading documents: {e}")
        return

    # --- Split Documents into Chunks ---
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs_chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(docs_chunks)} chunks.")

    # --- Initialize OpenAI Embeddings ---
    embeddings = OpenAIEmbeddings(api_key=openai_api_key) # Pass API key directly

    # --- Populate Pinecone Index ---
    print("Populating Pinecone index...")
    try:
        PineconeVectorStore.from_documents( # Use the updated class
            docs_chunks,
            embeddings,
            index_name=index_name
            # namespace= can be added if needed
        )
        print("Pinecone index populated successfully!")
    except Exception as e:
        print(f"Error populating Pinecone index: {e}")

if __name__ == "__main__":
    main()
