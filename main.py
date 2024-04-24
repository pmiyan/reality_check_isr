from brave_search import get_news_documents
from retrieval import retrieve_url_data
from similarity import get_similarity
from score_and_evaluate import evaluate_responses
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
client = OpenAI()


def process_user_query(user_query):
    print("getting news documents...")
    query_docs = get_news_documents(user_query, client)
    doc_urls = [doc["url"] for doc in query_docs]
    responses = {}
    for i, url in enumerate(doc_urls):
        document_text = retrieve_url_data(url)
        content = """
        {url}
        
        {text}
        """.format(url=url, text=document_text)
        print("getting similarity...")
        response = get_similarity(user_query, content, client)
        print(response)
        responses[url] = response

    final_response = evaluate_responses(responses, client)
    # score = final_response[0]
    # score_context = final_response[1]
    # print(final_response)
    return final_response

def main():
    st.title("Fake News Detection")
    user_query = st.text_input("Enter your statement to verify it:")
    if st.button("Verify"):
        with st.spinner('Processing your query...'):
            final_response = process_user_query(user_query)
        st.success('Here is the response:')
        st.write(final_response)

if __name__ == '__main__':
    main()
