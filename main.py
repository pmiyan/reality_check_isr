from brave_search import get_news_documents
from retrieval import retrieve_url_data
from similarity import get_similarity
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

def process_user_query(user_query):
    query_docs = get_news_documents(user_query, client)
    doc_urls = [doc["url"] for doc in query_docs]
    for url in doc_urls:
        document_text = retrieve_url_data(url)
        response = get_similarity(user_query, document_text, client)
        print(response)
    return True

if __name__ == '__main__':
    # user_query = input("Enter your statement to verify it:")
    user_query = "Travis Kelce plays for the state of Kansas"
    process_user_query(user_query)
