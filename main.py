from brave_search import get_news_documents
from retrieval import retrieve_url_data
from similarity import get_similarity
from score_and_evaluate import evaluate_responses
import streamlit as st
from streamviz import gauge
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def process_user_query(user_query):
    print("getting news documents...")
    query_docs = get_news_documents(user_query, client)
    doc_urls = [doc["url"] for doc in query_docs]
    responses = {}
    with st.sidebar:
        for i, url in enumerate(doc_urls):
            document_text = retrieve_url_data(url)
            content = """
            {url}
            
            {text}
            """.format(url=url, text=document_text)
            print("getting similarity...")
            response = get_similarity(user_query, content, client)
            print(response)
            st.write(url)
            for key, value in response.items():
                st.write(key, "=" , value)
            st.markdown("---\n")
            # st.write(response)
            responses[url] = response

    final_response = evaluate_responses(responses, client)
    # score = final_response[0]
    # score_context = final_response[1]
    # print(final_response)
    return final_response


def main():
    def display_box(title, content, color):
        st.markdown(
            f'<div style="border: 2px solid {color}; border-radius: 5px; padding: 10px; margin-bottom: 10px;"><h3 style="color: {color};">{title}</h3><p>{content}</p></div>',
            unsafe_allow_html=True)

    st.title("Fake News Detection")
    user_query = st.text_input("Enter your statement to verify it:")

    if st.button("Verify"):
        with st.spinner('Processing your query...'):
            final_response = process_user_query(user_query)
        st.markdown('<div style= color: #ae7bff; border-radius: 5px;"><p>Here is the response:</p></div>',
                    unsafe_allow_html=True)

        final_score = final_response[0]
        final_verdict = final_response[1]
        final_color = final_response[2]
        final_summary = final_response[3]

        # display_box("Score", final_score, final_color)
        gauge(
            (final_score + 1) / 2,
            gTheme="White", gSize="SML",
            gTitle="Reality score", gcLow="#FF5733", gcMid="#D3D3D3", gcHigh="#006400",
            grLow=0.15, grMid=0.5, sFix="%"
        )
        display_box("Verdict", final_verdict, final_color)
        display_box("Summary", final_summary, final_color)


if __name__ == '__main__':
    main()
