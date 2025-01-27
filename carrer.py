import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import requests


def fetch_web_results(query, api_key, top_k=10):
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": top_k}
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json()
    web_results = []
    for result in results.get("webPages", {}).get("value", []):
        web_results.append({
            "name": result["name"],
            "url": result["url"],
            "snippet": result["snippet"]
        })
    return web_results

def analyze_career_path(web_results):
    career_steps = []
    for result in web_results:
        snippet = result["snippet"]
        if any(keyword in snippet.lower() for keyword in ["step", "path", "career", "progress", "role"]):
            career_steps.append(snippet)
    return career_steps

def generalize_career_path(career_steps, openai_api_key):
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    prompt = (
        "You are a career expert. Based on the following information about career paths, "
        "provide a generic step-by-step roadmap for someone pursuing a career in this field:\n\n"
        f"Extracted Career Steps:\n{career_steps}\n\n"
        "Generic Career Roadmap:"
    )
    response = llm.predict(prompt)
    return response

def get_conversation_chain(vectorstore, top_k=5):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.error("Please load the preprocessed data first!")
        return

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(f"**User:** {message.content}")
        else:
            st.write(f"**Bot:** {message.content}")

def main():
    st.set_page_config(page_title="Right Fit", page_icon=":books:")

    option = st.sidebar.selectbox(
        "Choose a feature:",
        ["Career Path Discovery", "Skill Analyzer"]
    )

    if option == "Career Path Discovery":
        st.title("Career Path Discovery :chart_with_upwards_trend:")
        bing_api_key = ""  # Replace with your Bing API Key
        openai_api_key = ""  # Replace with your OpenAI API Key

        query = st.text_input("Enter a career or job role (e.g., Data Scientist):")
        if st.button("Generate Career Plan"):
            with st.spinner("Fetching career path information..."):
                try:
                    web_results = fetch_web_results(query, bing_api_key)
                    career_steps = analyze_career_path(web_results)
                    if career_steps:
                        roadmap = generalize_career_path("\n".join(career_steps), openai_api_key)
                        st.write("### Generic Career Roadmap:")
                        st.write(roadmap)
                        st.write("### Top Web Results:")
                        for idx, result in enumerate(web_results):
                            st.markdown(f"**{idx + 1}. [{result['name']}]({result['url']})**")
                            st.write(f"_Snippet_: {result['snippet']}")
                            st.write("---")
                    else:
                        st.warning("No relevant career steps found.")

                except Exception as e:
                    st.error(f"Error: {e}")

    elif option == "Skill Analyzer":
        st.title("Skill Analyzer :briefcase:")

        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

        # Automatically load the preprocessed data
        if st.session_state.conversation is None:
            with st.spinner("Loading preprocessed data..."):
                try:
                    embeddings = OpenAIEmbeddings()
                    faiss_index_path = "C:/Users/lalit_2idtquy/OneDrive/Desktop/Projects/ask-multiple-pdfs-main/faiss_index" 
                    vectorstore = FAISS.load_local(faiss_index_path, embeddings)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("Preprocessed data loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading data: {e}")

        user_question = st.text_input("Ask a question about your documents:")
        if user_question:
            handle_userinput(user_question)

if __name__ == "__main__":
    main()
