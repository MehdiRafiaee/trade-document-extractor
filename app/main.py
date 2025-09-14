import streamlit as st
from app.ocr import extract_text_from_pdf
from app.nlp import extract_entities

st.title("Trade Document Information Extractor")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "png", "jpg"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("temp_file", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract text
    text = extract_text_from_pdf("temp_file")
    
    # Display text
    st.subheader("Extracted Text")
    st.text(text)
    
    # Extract entities
    entities = extract_entities(text)
    
    st.subheader("Extracted Entities")
    for entity in entities:
        st.write(f"{entity['text']} ({entity['label']})")
