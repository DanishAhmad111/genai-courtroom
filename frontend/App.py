import streamlit as st
import sys
import os

# Make sure Python can find backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.courtroom_logic import run_courtroom

st.set_page_config(page_title="GenAI Courtroom", layout="wide")
st.title("🧑‍⚖️ GenAI Courtroom – Legal Trial Simulator")

st.markdown("""
Simulate a courtroom trial using generative AI. Enter a case description, and the AI will generate:
- 👨‍💼 Prosecution argument
- 👨‍⚖️ Defense response
- 📜 Judge's verdict
""")
#################################################################
from rag.rag_utils import extract_text_from_pdf, chunk_text, build_faiss_index
import tempfile

uploaded_pdf = st.file_uploader("📄 Upload legal document (PDF) - Optional", type="pdf", help="Upload a PDF to add legal references to the trial. The app works without it too!")

if uploaded_pdf:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.read())
        pdf_path = tmp.name
        text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(text)
        build_faiss_index(chunks)
        st.success("📚 Document processed and indexed.")
################################################################
# Input for case summary
case = st.text_area("📥 Enter a legal dispute or case summary:", height=200)

# Button to trigger trial simulation
if st.button("⚖️ Simulate Trial"):
    if not case.strip():
        st.warning("Please enter a case description.")
    else:
        with st.spinner("Running courtroom simulation..."):
            try:
                prosecution, defense, verdict = run_courtroom(case)
                st.success("✅ Trial completed.")
                
                st.subheader("👨‍💼 Prosecution")
                st.markdown(prosecution)

                st.subheader("👨‍⚖️ Defense")
                st.markdown(defense)

                st.subheader("📜 Judge Verdict")
                st.markdown(verdict)

            except Exception as e:
                st.error(f"An error occurred: {e}")
