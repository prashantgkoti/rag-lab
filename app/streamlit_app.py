from pathlib import Path
import sys 

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from scripts.query_corpus import search
from src.rag.generation import generate_answer

st.set_page_config(page_title="Sec Lending RAG", page_icon=":robot_face:")
st.title("Sec Lending RAG FAQ")
st.caption("Ask questions about securities lending and get answers based on the SEC Lending FAQ corpus.")

question = st.text_input("Enter your question here: ", placeholder="What margin is required from the borrower?")

if st.button("Ask"):
    if question:
        with st.spinner("Searching for relevant information..."):
            hits = search(question, top_k=5)
            chunks = [{"source": hit.payload["source"], "text": hit.payload["text"]} for hit in hits]
            if not chunks:
                st.warning("No relevant information found in the corpus.")
            else:
                with st.spinner("Generating answer..."):
                    answer = generate_answer(question, chunks)
                    st.subheader("Answer:")
                    st.write(answer)  
                    
        st.markdown("### Sources")
        for i, hit in enumerate(hits, start=1):
            with st.expander(f"[{i}] {hit.payload['source']} — score {hit.score:.3f}"):
                st.write(hit.payload["text"])

