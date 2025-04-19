import os
import streamlit as st
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage
)
from llama_index.core.settings import Settings
from llama_index.llms.bedrock import Bedrock
from llama_index.embeddings.bedrock import BedrockEmbedding, Models

from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas import evaluate
from datasets import Dataset

# ------------------------------------------------------------------------
# LlamaIndex - Amazon Bedrock

llm = Bedrock(model="anthropic.claude-v2")
embed_model = BedrockEmbedding(model="amazon.titan-embed-text-v1")

Settings.llm = llm
Settings.embed_model = embed_model

# ------------------------------------------------------------------------
# Streamlit

st.set_page_config(page_title='LlamaIndex Q&A over your data 📂')

# Clear Chat History function
def clear_screen():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

with st.sidebar:
    st.title('LlamaIndex 🦙')
    st.subheader('Q&A over your data 📂')
    st.markdown('[Amazon Bedrock](https://aws.amazon.com/bedrock/) - The easiest way to build and scale generative AI applications with foundation models')
    st.divider()
    streaming_on = st.toggle('Streaming')
    st.button('Clear Screen', on_click=clear_screen)

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing your data. This may take a while..."):
        PERSIST_DIR = "storage"
        if not os.path.exists(PERSIST_DIR):
            documents = SimpleDirectoryReader(input_dir="data", recursive=True).load_data()
            index = VectorStoreIndex.from_documents(documents)
            index.storage_context.persist(persist_dir=PERSIST_DIR)
        else:
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            index = load_index_from_storage(storage_context)
        return index

index = load_data()

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    if streaming_on:
        # Streaming query path
        query_engine = index.as_query_engine(streaming=True)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ''
            streaming_response = query_engine.query(prompt)
            for chunk in streaming_response.response_gen:
                full_response += chunk
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        # Non-streaming query path with Ragas evaluation
        query_engine = index.as_query_engine(similarity_top_k=3, response_mode="compact")
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = query_engine.query(prompt)
                answer = response.response
                context = [node.text for node in response.source_nodes]

                # Display response
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # Ragas Evaluation
                try:
                    sample = {
                        "question": prompt,
                        "answer": answer,
                        "contexts": context,
                    }
                    ragas_dataset = Dataset.from_list([sample])
                    results = evaluate(ragas_dataset, metrics=[
                        faithfulness,
                        answer_relevancy,
                        context_precision,
                    ])

                    st.markdown("### Ragas Evaluation")
                    st.dataframe(results.to_pandas())
                except Exception as e:
                    st.error(f"Ragas evaluation failed: {str(e)}")
