import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Apple Knowledge Assistant", layout="wide")
st.title("Apple Product Q&A Assistant (RAG + Agent)")
with st.expander("How to use"):
    st.markdown("""
You can:
- Ask **general product questions** like `Name all Apple products` or `What are the types of iPads?`
- Ask **for specifications** like `Specs of iPad` or `Specs of all MacBooks`
- Ask **to calculate** (e.g., `Calculate 12 + 5`)
- Ask **for definitions** (e.g., `Define RAM`, `Define MacBook`)
- Ask **comparisons** (e.g., `Compare iPad Air vs iPad Pro`)

> Tip: Start by asking **"Name all apple products"** to see available context from the dataset.""")
query = st.text_input("Ask a question")

if query:
    with st.spinner("Thinking..."):
        result = run_agent(query)

    st.subheader("Decision Route:")
    st.write(result["route"].capitalize())

    st.subheader("Answer:")
    st.markdown(result["result"])

    if result.get("context"):
        st.subheader("Retrieved Context:")
        st.text_area("Context", result["context"], height=200)

    if result.get("context"):
        st.subheader("Retrieved Chunks Preview")
    chunks = result["context"].split("---")
    for i, chunk in enumerate(chunks[:3]):
        with st.expander(f"Chunk {i+1}"):
            st.markdown(chunk)
