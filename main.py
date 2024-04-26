from brave_search import get_news_documents
from retrieval import retrieve_url_data
from similarity import get_similarity
from score_and_evaluate import evaluate_responses
import streamlit as st
from gauge import gauge
from dotenv import load_dotenv
import threading
from openai import OpenAI
from urllib.parse import urlparse


load_dotenv()
client = OpenAI()


def open_ai_query(url, user_query, llm, responses):
    document_title, document_text = retrieve_url_data(url)
    content = """
    {url}

    {text}
    """.format(url=url, text=document_text)
    print("getting similarity...")
    response = get_similarity(user_query, content, llm)
    response["title"] = document_title
    responses[url] = response


def process_user_query(user_query, num_results):
    print("getting news documents...")
    query_docs = get_news_documents(user_query, client, num_results)
    doc_urls = [doc["url"] for doc in query_docs]
    single_responses = {}
    threads = []
    for i, url in enumerate(doc_urls):
        execThread = threading.Thread(target=open_ai_query, args=(url, user_query, client, single_responses,))
        threads.append(execThread)
        execThread.start()

    for exec_thread in threads:
        exec_thread.join()

    final_response = evaluate_responses(single_responses, client)
    return final_response, single_responses


EmojiDict = {
    "TRUE": "✅ True",
    "FALSE": "❌ False",
    "NULL": "❓ Uncertain"
}


def main():
    num_results = 10

    def display_box(title, content, color):
        st.markdown(
            f'<div style="border: 2px solid {color}; border-radius: 5px; padding: 10px; margin-bottom: 10px;"><h3 style="color: {color};">{title}</h3><p>{content}</p></div>',
            unsafe_allow_html=True)

    st.title("Fake News Detection")
    user_query = st.text_input("Enter your statement to verify it:")

    if st.button("Verify"):
        with st.spinner('Processing your query...'):
            final_response, single_responses = process_user_query(user_query, num_results)
        st.markdown('<div style= color: #ae7bff; border-radius: 5px;"><p>Here is the response:</p></div>',
                    unsafe_allow_html=True)

        final_score = final_response[0]
        final_verdict = final_response[1]
        final_color = final_response[2]
        final_summary = final_response[3]

        with st.expander("See sources"):
            tabs = st.tabs(["Source {}".format(x) for x in range(1, len(single_responses) + 1)])

            for (url, response), tab in zip(single_responses.items(), tabs):
                base_url = urlparse(url).netloc
                with tab:
                    header = f"[{response['title']}]({url})"
                    st.header(header)
                    st.markdown(f"""
                        > From {base_url}
                        
                        ---
                        
                        Rating: {EmojiDict[response["answer"]]}
                            
                        Confidence: {response["confidence"]}
                        
                        ---
                        Reasoning: {response["reasoning"]}
                        
                        ---
                        Context: {response["context"]}
                    """)

        gauge(
            (final_score + 1) / 2,
            gTheme="White", gSize="FULL",
            gTitle="Reality score", gcLow="#FF5733", gcMid="#D3D3D3", gcHigh="#006400",
            grLow=0.15, grMid=0.5, sFix="%"
        )
        display_box("Verdict", final_verdict, final_color)
        display_box("Summary", final_summary, final_color)

    return True


if __name__ == '__main__':
    main()
