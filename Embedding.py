# import os
# from PyPDF2 import PdfReader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS

# def preprocess_pdfs(pdf_folder, faiss_index_path):
#     text = ""
#     for pdf_file in os.listdir(pdf_folder):
#         if pdf_file.endswith(".pdf"):
#             pdf_path = os.path.join(pdf_folder, pdf_file)
#             pdf_reader = PdfReader(pdf_path)
#             for page in pdf_reader.pages:
#                 text += page.extract_text()

#     text_splitter = CharacterTextSplitter(
#         separator="\n",
#         chunk_size=1000,
#         chunk_overlap=200,
#         length_function=len
#     )
#     text_chunks = text_splitter.split_text(text)

#     embeddings = OpenAIEmbeddings()
#     vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

#     # Save the vectorstore to disk
#     vectorstore.save_local(faiss_index_path)
#     print(f"Vectorstore saved to {faiss_index_path}")

# # Example usage
# if __name__ == "__main__":
#     pdf_folder = "C:/Users/lalit_2idtquy/OneDrive/Desktop/Projects/ask-multiple-pdfs-main/pdfs"  # Folder containing PDFs
#     faiss_index_path = "C:/Users/lalit_2idtquy/OneDrive/Desktop/Projects/ask-multiple-pdfs-main" # Save location for FAISS index
#     preprocess_pdfs(pdf_folder, faiss_index_path)


import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def preprocess_csv_to_embeddings(csv_file_path, faiss_index_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path, header=None)  # No header in the file
    df.columns = ["text"]  # Assign a column name for clarity

    # Extract text data
    texts = df["text"].dropna().tolist()  # Drop any empty rows and convert to a list

    # Create embeddings for each row
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=texts, embedding=embeddings)

    # Save the vectorstore to disk
    vectorstore.save_local(faiss_index_path)
    print(f"Vectorstore saved to {faiss_index_path}")

# Example usage
if __name__ == "__main__":
    csv_file_path = "C:/Users/lalit_2idtquy/OneDrive/Desktop/Projects/ask-multiple-pdfs-main/job_listings.csv"  # Path to your CSV file
    faiss_index_path = "C:/Users/lalit_2idtquy/OneDrive/Desktop/Projects/ask-multiple-pdfs-main/faiss_index"    # Save location for FAISS index
    preprocess_csv_to_embeddings(csv_file_path, faiss_index_path)
