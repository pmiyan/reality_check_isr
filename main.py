from time import time

import_time_start = time()
from brave_search import get_news_documents
print("import time:", time() - import_time_start)

retrieval_time_start = time()
from retrieval import retrieve_url_data
print("retrieval time:", time() - retrieval_time_start)

similarity_time_start = time()
from similarity import get_similarity
print("similarity time:", time() - similarity_time_start)

from score_and_evaluate import evaluate_responses
from dotenv import load_dotenv
load_dotenv()
import threading

print("import time:", time() - import_time_start)

openai_time_start = time()
from openai import OpenAI
client = OpenAI()
print("openai time:", time() - openai_time_start)


def process_user_query(user_query):
    print("getting news documents...")
    query_docs = get_news_documents(user_query, client)
    doc_urls = [doc["url"] for doc in query_docs]
    responses = {}

    threads = []
    def open_ai_query(url, user_query, client):
        document_text = retrieve_url_data(url)
        content = """
        {url}
        
        {text}
        """.format(url=url, text=document_text)
        print("getting similarity...")
        response = get_similarity(user_query, content, client)
        print(response)
        responses[url] = response

    

    for i, url in enumerate(doc_urls):
        execThread = threading.Thread(target=open_ai_query, args = (url,user_query,client, responses,))
        threads.append(execThread)
        execThread.start()

    for exec_thread in threads:
        exec_thread.join()
        
    final_response = evaluate_responses(responses, client)
    # score = final_response[0]
    # score_context = final_response[1]
    print(final_response)

    return True


if __name__ == '__main__':
    # user_query = input("Enter your statement to verify it:")
    # user_query = "Donald Trump is being supported by the Republican party to provide funding to Ukraine."
    user_query = "Mike Jonsen is being suppported by the Democratic party to provide funding to Ukraine."
    process_user_query(user_query)
