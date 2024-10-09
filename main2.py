import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer

# Load the pre-trained question answering model
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

def main():
    st.title("Document Question Answering")

    # Upload document
    uploaded_file = st.file_uploader("Upload a document", type=['txt', 'pdf'])

    # Display document content
    if uploaded_file is not None:
        document_text = read_uploaded_file(uploaded_file)
        st.subheader("Document Content")
        st.write(document_text)

        # Ask a question
        question = st.text_input("Ask a question:")
        if st.button("Get Answer"):
            if question.strip() == "":
                st.error("Please enter a question.")
            else:
                answer = get_answer(document_text, question)
                st.subheader("Answer")
                st.write(answer)

def read_uploaded_file(uploaded_file):
    if uploaded_file.type == 'text/plain':
        return uploaded_file.getvalue().decode("utf-8")
    elif uploaded_file.type == 'application/pdf':
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        st.error("Unsupported file format")

def get_answer(document_text, question):
    # Tokenize input
    inputs = tokenizer.encode("question: " + question + " context: " + document_text, return_tensors="pt", max_length=512, truncation=True)

    # Generate answer
    outputs = model.generate(inputs)

    # Decode and return the answer
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

if __name__ == "__main__":
    main()
