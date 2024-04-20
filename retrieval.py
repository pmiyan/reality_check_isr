from dotenv import load_dotenv
load_dotenv()

from llama_index.core import VectorStoreIndex, download_loader
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.web import BeautifulSoupWebReader

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embedding = embed_model
Settings.llm = None

loader = BeautifulSoupWebReader()

import requests

def custom_get(url, *args, **kwargs):
    headers = kwargs.get("headers", {})
    headers["User-Agent"] = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/123.0.0.0 Safari/537.36"
    kwargs["headers"] = headers
    return original_get(url, *args, **kwargs)

original_get = requests.get

requests.get = custom_get

url_list = ["https://www.nytimes.com/2024/04/19/style/taylor-swift-lyrics-tortured-poets-department.html", "https://apnews.com/article/gaza-israel-aid-pier-us-military-e988256270fc0067d2f5524fd542a475"]
for url in url_list:
    documents = loader.load_data(urls=[url])
    print(documents[0].text)
