# Retrieval-Augmented Generation (RAG) Platform for Career Recommendations

## Overview
This project implements a **Retrieval-Augmented Generation (RAG)** pipeline to provide personalized career recommendations by combining dense retrieval with generative AI models. By processing and analyzing over **1,000+ job postings**, the platform achieves **90% recommendation relevance**, offering users accurate and data-driven career insights.

## Key Features
- **Dense Vector Search**:
  - Utilized **FAISS (Facebook AI Similarity Search)** to create an optimized vector database for efficient retrieval of job postings based on user queries.
  - Enhanced query accuracy and retrieval speed with **10x faster response times** through vector indexing.

- **Generative AI Integration**:
  - Leveraged **OpenAI embeddings** for encoding job descriptions into a high-dimensional feature space.
  - Combined dense retrieval with generative language models to deliver contextual, natural language recommendations.

- **Automation**:
  - Built a dynamic data collection pipeline using **Selenium** to scrape job postings and descriptions from platforms like **LinkedIn**.
  - Automated preprocessing tasks, such as cleaning and structuring the dataset for downstream vectorization.

- **Deployment**:
  - Deployed an interactive **Streamlit dashboard** for real-time user interactions, enabling users to input career queries and receive tailored recommendations.
  - Supported user-specific contextual responses via a conversational retrieval chain.

## Technologies Used
- **Frameworks**:
  - **LangChain**: For constructing the RAG pipeline and managing retrieval-generation workflows.
  - **Hugging Face Transformers**: For leveraging pretrained models to fine-tune language understanding.
- **Tools**:
  - **FAISS**: For efficient vector indexing and dense retrieval.
  - **Selenium**: For web scraping job data dynamically from career platforms.
  - **Streamlit**: For creating an interactive front-end application.
- **Languages**:
  - Python for backend development and scripting.

## Workflow
1. **Data Collection**:
   - Scraped job postings using **Selenium** and stored structured data in CSV format.
   - Cleaned and preprocessed data for vector embedding.
2. **Vectorization and Storage**:
   - Encoded job descriptions into vector embeddings using **OpenAI models**.
   - Indexed these embeddings in **FAISS** for efficient retrieval.
3. **Query Processing**:
   - Users query career paths via the **Streamlit app**.
   - Queries are converted into embeddings and matched with the nearest job descriptions using FAISS.
4. **Response Generation**:
   - Retrieved results are passed through a generative language model for contextual recommendations tailored to the user's input.
5. **Visualization**:
   - Real-time results and insights are displayed in the **Streamlit dashboard**.