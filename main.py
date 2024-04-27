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


def process_user_query(user_query, num_results, inclination):
    print("getting news documents...")
    single_responses = {}
    try:

        query_docs = get_news_documents(user_query, client, num_results, inclination)
        doc_urls = [doc["url"] for doc in query_docs]

        threads = []
        for i, url in enumerate(doc_urls):
            execThread = threading.Thread(target=open_ai_query, args=(url, user_query, client, single_responses,))
            threads.append(execThread)
            execThread.start()

        for exec_thread in threads:
            exec_thread.join()
    except Exception as error:
        print(f'Error Occurred while fetching the query : {str(error)}')
        return (0.0,
                'Sorry, we\'re unable to process your request at this point in time!!, Sometimes we can continue to live on with fake news in our lives... Cheerios!!',
                '#D3D3D3', ''), single_responses

    final_response = evaluate_responses(single_responses, client)
    return final_response, single_responses


EmojiDict = {
    "TRUE": "✅ True",
    "FALSE": "❌ False",
    "NULL": "❓ Uncertain"
}

ImportanceDict = {
    "HIGH": 1,
    "MEDIUM": 0,
    "LOW": -1
}


def main():
    num_results = 10

    def display_box(title, content, color):
        st.markdown(
            f'<div style="border: 2px solid {color}; border-radius: 5px; padding: 10px; margin-bottom: 10px;"><h3 style="color: {color};">{title}</h3><p>{content}</p></div>',
            unsafe_allow_html=True)

    google_list = ["unopinionated", "left", "right"]
    st.title("Fake News Detection")
    user_query = st.text_input("Enter your statement to verify it:")
    inclination = st.selectbox(label="Select Political Inclination", options=google_list)
    print(f'inclination selected :  {inclination}')

    if st.button("Verify") and user_query:
        print(f'query : {user_query}')
        with st.spinner('Processing your query...'):
            final_response, single_responses = process_user_query(user_query, num_results, inclination)

        st.markdown('<div style= color: #ae7bff; border-radius: 5px;"><p>Here is the response:</p></div>',
                    unsafe_allow_html=True)

        final_score = final_response[0]
        final_verdict = final_response[1]
        final_color = final_response[2]
        final_summary = final_response[3]
        if len(single_responses) > 0:
            with st.expander("See sources"):
                tabs = st.tabs(["Source {}".format(x) for x in range(1, len(single_responses) + 1)])
                counter = 1
                sorted_responses = dict(sorted(single_responses.items(), key=lambda item: -ImportanceDict[item[1]['confidence']]))
                print(sorted_responses)
                for (url, response), tab in zip(sorted_responses.items(), tabs):
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
                        # st.markdown("""
                        # <style>
                        # .thumbsup {
                        # font-size: 30px;
                        # cursor: pointer;
                        # }
                        # .thumbsdown {
                        # font-size: 30px;
                        # cursor: pointer;
                        # }
                        # </style>
                        # """, unsafe_allow_html=True)

                        # col1, col2 = st.columns(2)
                        #
                        # with col1:
                        #     counter += 1
                        #     if st.button("👍", key=str(counter)):
                        #         st.write("Liked!")
                        #
                        #
                        # with col2:
                        #     counter += 1
                        #     if st.button("👎", key=str(counter)):
                        #         st.write("Disliked!")

            gauge(
                (final_score + 1) / 2,
                gTheme="White", gSize="FULL",
                gTitle="Reality score", gcLow="#FF5733", gcMid="#D3D3D3", gcHigh="#006400",
                grLow=0.15, grMid=0.5, sFix="%"
            )
            display_box("Verdict", final_verdict, final_color)
            display_box("Summary", final_summary, final_color)
        else:
            display_box("", final_verdict, final_color)

    return True


if __name__ == '__main__':
    main()
