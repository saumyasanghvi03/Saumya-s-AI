# AI-Powered Financial Literacy Chat Widget

This project aims to create an embeddable chat widget that provides financial literacy information using AI. It features a Flask backend with a RAG (Retrieval Augmented Generation) pipeline using LangChain, OpenAI, and Pinecone, and a (placeholder) React frontend.

**Current Status:**
*   **Backend:** Developed and functional up to the point of requiring real API keys and network access to external services (OpenAI, Pinecone).
*   **Frontend:** **Placeholder code only.** The React frontend could not be built or tested due to a non-functional `npm` environment in the development sandbox. The provided React code offers a structural starting point.

## Project Structure

```
.
├── backend/            # Flask backend application
│   ├── app.py          # Main Flask app with /chat API
│   ├── populate_pinecone.py # Script to load data into Pinecone
│   ├── requirements.txt# Python dependencies
│   ├── .env            # For API keys (gitignored, use .env.template)
│   └── ...
├── data/               # Sample financial literacy documents
│   ├── savings_faq.txt
│   └── investing_basics.txt
├── frontend/           # React frontend application (Placeholder)
│   └── chat-widget/
│       ├── src/
│       │   ├── components/ # React components (ChatPopup, ChatWidget, etc.)
│       │   │   ├── ChatPopup.jsx
│       │   │   ├── ChatWidget.jsx
│       │   │   ├── MessageInput.jsx
│       │   │   └── MessageList.jsx
│       │   ├── App.jsx     # Main App component
│       │   ├── main.jsx    # Vite entry point
│       │   └── App.css     # Basic styles
│       ├── package.json    # Frontend dependencies (Vite setup)
│       └── ...
└── README.md           # This file
```

## 1. Backend Setup

The backend is a Flask application that serves a `/chat` API endpoint.

### Prerequisites
*   Python 3.8+
*   Access to an OpenAI API key
*   Access to a Pinecone API key and environment details

### Installation & Setup
1.  **Clone the repository (if you haven't already).**
2.  **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```
3.  **Create a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configure API Keys:**
    *   Make a copy of `.env.template` (if provided, otherwise create `.env` directly).
        *   *Developer Note: I will create a `.env.template` in the next step.*
    *   Edit the `.env` file in the `backend` directory and add your actual API keys:
        ```env
        # Pinecone API Key
        PINECONE_API_KEY="YOUR_PINECONE_API_KEY"
        PINECONE_ENVIRONMENT="YOUR_PINECONE_ENVIRONMENT" # e.g., "us-west1-gcp"

        # OpenAI API Key
        OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
        ```

### Populating the Vector Database
Before running the main application, you need to populate your Pinecone index with the financial literacy data.
1.  **Ensure your `.env` file is correctly configured with your API keys.**
2.  **Run the `populate_pinecone.py` script from the `backend` directory:**
    ```bash
    python populate_pinecone.py
    ```
    This script will:
    *   Load documents from the `../data/` directory.
    *   Chunk the documents.
    *   Generate embeddings using OpenAI.
    *   Create a Pinecone index (default: `financial-literacy-widget`) if it doesn't exist.
    *   Store the documents and their embeddings in the index.

### Running the Flask Backend
1.  **Ensure your `.env` file is configured and you have populated the Pinecone index.**
2.  **Run the Flask application from the `backend` directory:**
    ```bash
    python app.py
    ```
    The application will start (by default on `http://localhost:5001`). You should see output indicating it's running.

### API Endpoint
*   **`POST /chat`**:
    *   Accepts a JSON payload: `{"message": "Your financial question here"}`
    *   Returns a JSON response:
        ```json
        {
          "answer": "The AI-generated answer...",
          "source_documents": [
            {
              "content": "Relevant snippet from a source document...",
              "metadata": { "source": "filename.txt", ... }
            }
          ]
        }
        ```

## 2. Frontend Setup (Placeholder Only)

**IMPORTANT LIMITATION:** The React frontend could not be fully developed, built, or tested due to a non-functional `npm` (Node Package Manager) in the development sandbox environment. `npm` commands consistently failed (e.g., "uv_cwd" errors, inability to find installed binaries like `vite` or `react-scripts`).

The code in the `frontend/chat-widget` directory represents a Vite-based React application structure with placeholder components. To make this frontend functional, you would need to:
1.  Have a working Node.js and npm environment.
2.  Navigate to `frontend/chat-widget`.
3.  Run `npm install` to install dependencies (this step was failing in the sandbox).
4.  Run `npm run dev` to start the Vite development server (also failing).

### Placeholder Component Structure
*   `src/components/ChatPopup.jsx`: Manages the visibility of the chat button and widget.
*   `src/components/ChatWidget.jsx`: Core chat interface, handles message state and API calls to `http://localhost:5001/chat`.
*   `src/components/MessageList.jsx`: Displays the list of messages.
*   `src/components/MessageInput.jsx`: Provides the text input and send button.
*   `src/App.jsx`: Renders `ChatPopup`.
*   `src/main.jsx`: Vite entry point.

## 3. Conceptual Embed Logic

If the React frontend *could* be built, it would produce a JavaScript bundle (e.g., `widget.js`) and a CSS file (e.g., `widget.css`). To embed the chat widget on a website, a user would typically:

1.  **Host the `widget.js` and `widget.css` files** (e.g., on a CDN or their own server).
2.  **Add the following snippet to their HTML page:**

    ```html
    <!-- Link to the widget's CSS -->
    <link rel="stylesheet" href="PATH_TO_YOUR_HOSTED/widget.css">

    <!-- Script tag to load the widget's JavaScript bundle -->
    <!-- The script itself should handle creating its own root DOM element if needed -->
    <script src="PATH_TO_YOUR_HOSTED/widget.js" defer></script>
    ```
    The `ChatPopup.jsx` component is designed to be fixed-position and manage its own appearance once the script is loaded.

## Contributing
(Standard contribution guidelines would go here if this were an open project - e.g., fork, branch, PR)

## Disclaimer
This is a software component generated by an AI assistant. Thorough testing, security hardening, and review are required before use in production environments. Ensure compliance with API terms of service for OpenAI, Pinecone, etc.
