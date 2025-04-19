import streamlit as st
import requests
import pandas as pd
import io
from datetime import datetime
from ui.helpers import generate_unique_id
from ui.styles import Styles
from ui.components import ChatUI
from visualization.charts import ChartGenerator

# Backend API base URL
API_BASE_URL = "http://localhost:8000"

class StreamlitApp:
    """Main Streamlit application class (refactored for FastAPI backend)."""

    def __init__(self):
        self.logo_path = "assets/logo.png"
        self.styles = Styles()
        self.chat_components = ChatUI()
        self.chart_generator = ChartGenerator(None)

        # Generate a unique session ID
        if "session_id" not in st.session_state:
            self.session_id = generate_unique_id()
            st.session_state.session_id = self.session_id
        else:
            self.session_id = st.session_state.session_id

        # Initialize message ratings if not in session state
        if "message_ratings" not in st.session_state:
            st.session_state.message_ratings = {}
        if "is_thinking" not in st.session_state:
            st.session_state.is_thinking = False

    def setup_ui(self):
        try:
            st.set_page_config(page_title="Data Insights Chatbot", page_icon="🤖", layout="wide")
            self.styles.apply_all_styles(st)
            self.setup_sidebar()
            self.setup_main_content()
        except Exception as e:
            st.error(f"An error occurred while setting up the UI: {str(e)}")

    def setup_sidebar(self):
        try:
            with st.sidebar:
                st.image(self.logo_path, width=200)
                st.write("Welcome to the Data Insights Chatbot!")
                st.write("Ask me about data insights or SQL queries.")
                st.write(f"Session ID: {st.session_state.session_id}")
                st.write(f"Current Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown("---")
                self.chat_components.setup_feedback()
        except Exception as e:
            st.sidebar.error(f"An error occurred while setting up the sidebar: {str(e)}")

    def query_agent(self, query):
        url = f"{API_BASE_URL}/agent/query"
        response = requests.post(url, json={"query": query, "session_id": self.session_id})
        if response.ok:
            return response.json()
        else:
            return {"success": False, "response": f"Error: {response.text}"}

    def send_feedback(self, response_id, feedback, rating):
        url = f"{API_BASE_URL}/agent/feedback"
        response = requests.post(url, json={"response_id": response_id, "feedback": feedback, "rating": rating, "session_id": self.session_id})
        return response.ok

    def search_knowledgebase(self, query):
        url = f"{API_BASE_URL}/knowledgebase/search"
        response = requests.get(url, params={"query": query, "session_id": self.session_id})
        if response.ok:
            return response.json().get("results", [])
        return []

    def get_inventory(self):
        url = f"{API_BASE_URL}/inventory/"
        response = requests.get(url, params={"session_id": self.session_id})
        if response.ok:
            return response.json().get("data", [])
        return []

    def get_chart_data(self):
        url = f"{API_BASE_URL}/chart/data"
        response = requests.get(url, params={"session_id": self.session_id})
        if response.ok:
            return response.json().get("summary", {})
        return {}

    def download_s3_file(self, s3_path):
        url = f"{API_BASE_URL}/s3/download"
        response = requests.get(url, params={"s3_path": s3_path, "session_id": self.session_id})
        if response.ok:
            return response.content
        return None

    def display_chart_for_result(self, s3_path=None, sample_rows=None, chart_type=None, x_column=None, y_column=None):
        try:
            data = None
            if s3_path:
                st.info(f"Loading data from S3: [{s3_path}]")
                content = self.download_s3_file(s3_path)
                if content:
                    data = pd.read_csv(io.BytesIO(content))
                    st.success(f"Successfully loaded {len(data)} records from S3")
                else:
                    st.error("Failed to load data from S3.")
                    return
            elif sample_rows:
                data = pd.DataFrame(sample_rows)
                st.warning("Using sample data due to S3 loading error")
            else:
                st.error("No data available for visualization")
                return

            df = pd.DataFrame(data)
            columns = list(df.columns)

            if not x_column:
                x_column = st.selectbox("Select X axis column:", columns)
            if not y_column:
                numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
                if not numeric_columns:
                    st.warning("No numeric columns available for Y-axis")
                    return
                y_column = st.selectbox("Select Y-axis column:", numeric_columns)

            if not chart_type:
                chart_type = st.selectbox(
                    "Select chart type:",
                    ["bar", "line", "pie", "scatter", "histogram", "heatmap"],
                    index=0
                )

            color_column = None
            if len(columns) > 2 and chart_type.lower() != "pie":
                use_color = st.checkbox("Use color differentiation")
                if use_color:
                    color_column = st.selectbox("Select column for color:", columns)

            fig = self.chart_generator.generate_chart(
                data=df,
                chart_type=chart_type,
                x_column=x_column,
                y_column=y_column,
                title=f"{y_column} by {x_column}",
                color_column=color_column
            )
            self.chart_generator.display_chart_in_streamlit(fig)

        except Exception as e:
            st.error(f"An error occurred while generating the chart: {str(e)}")

    def setup_main_content(self):
        st.title("Data Insights Chatbot 🤖")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "input_key" not in st.session_state:
            st.session_state.input_key = str(datetime.now().timestamp())
        # Place chat history above input, like ChatGPT
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"<div style='text-align: left; color: #1a73e8; background-color: #e8f0fe; padding: 8px; border-radius: 8px; margin: 8px 0;'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
            else:
                content = msg["content"]
                if isinstance(content, dict):
                    sql_query = content.get("sql_query", "")
                    data = content.get("data", "")
                    explanation = content.get("explanation", "")
                    if sql_query:
                        st.markdown(f"**SQL Query:**\n```sql\n{sql_query}\n```")
                    if isinstance(data, list) and data and isinstance(data[0], dict):
                        st.markdown("**Data:**")
                        st.dataframe(pd.DataFrame(data))
                    elif data:
                        st.markdown(f"**Data:**\n```\n{data}\n```")
                    if explanation:
                        st.markdown(f"**Explanation:**\n{explanation}")
                elif isinstance(content, str):
                    st.markdown(f"<div style='text-align: left; color: #222; background-color: #f1f3f4; padding: 8px; border-radius: 8px; margin: 8px 0;'>{content}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(str(content))
        # Chat input at the bottom, always cleared after sending
        user_query = st.text_input(
            "Type your message and press Enter...",
            placeholder="Type your message and press Enter..."
        )
        if user_query:
            if ("last_user_query" not in st.session_state) or (user_query != st.session_state.get("last_user_query")):
                st.session_state.is_thinking = True
                with st.spinner("Thinking..."):
                    result = self.query_agent(user_query)
                    st.session_state.is_thinking = False
                    response = result.get("response", "No response.")
                    # Save user and bot messages to chat history
                    st.session_state.chat_history.append({"role": "user", "content": user_query})
                    st.session_state.chat_history.append({"role": "bot", "content": response})
                    st.session_state.last_user_query = user_query
                # Clear the input box after sending by changing the key
                st.session_state.input_key = str(datetime.now().timestamp())
                st.rerun()

if __name__ == "__main__":
    app = StreamlitApp()
    app.setup_ui()
