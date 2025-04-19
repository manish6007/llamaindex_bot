# Data Insights Chatbot

A full-stack AI-powered chatbot for data insights, featuring a FastAPI backend and a Streamlit frontend. The bot supports SQL/knowledge queries, persistent chat memory, and rich UI chat experience.

## Features
- FastAPI backend for all business logic, data, and model inference
- Streamlit frontend for a ChatGPT-like chat UI
- Per-session conversational memory
- SQL query, data, and explanation shown separately in chat
- AWS S3 integration (optional)

## Prerequisites
- Python 3.10+
- (Recommended) Virtual environment (venv)

## Installation

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd llamaindex_bot
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # Or
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

### 1. Start the FastAPI Backend

```sh
uvicorn backend.main:app --reload
```
- The backend will be available at http://localhost:8000
- You can check http://localhost:8000/docs for API documentation

### 2. Start the Streamlit Frontend

In a new terminal (with the same venv activated):

```sh
streamlit run streamlit_app.py
```
- The frontend will be available at http://localhost:8501

## Usage
- Interact with the chatbot in the Streamlit UI.
- Each message is sent to the FastAPI backend, which maintains per-session memory.
- The bot's response will show the SQL query, data (as a table if possible), and explanation.
- All previous messages are shown in a chat-like format.

## Project Structure
```
llamaindex_bot/
├── agent/                # Agent logic
├── assets/               # Logo and static assets
├── backend/              # FastAPI backend (main.py, routers, models)
├── config/               # Configuration files
├── core/                 # Logging, utilities
├── data/                 # Knowledgebase and data files
├── llamaIndex/           # LlamaIndex logic, memory, embeddings
├── services/             # AWS S3 and other services
├── ui/                   # Streamlit UI components and styles
├── visualization/        # Chart generation
├── streamlit_app.py      # Streamlit frontend entry point
├── requirements.txt      # All dependencies
```

## Customization
- To change the logo, replace `assets/logo.png`.
- To update the knowledgebase, edit `data/knowledgebase.txt`.
- To add new endpoints, edit or add routers in `backend/routers/`.

## Troubleshooting
- If you see errors about missing Python or venv, recreate your virtual environment and reinstall requirements.
- If Streamlit or FastAPI can't connect, ensure both are running and check for port conflicts.
- For Windows, always use `venv\Scripts\activate` to activate your environment.

## License
MIT
