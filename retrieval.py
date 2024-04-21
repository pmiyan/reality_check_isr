from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.web import BeautifulSoupWebReader
import requests

def retrieve_url_data(url):
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.embedding = embed_model
    Settings.llm = None
    loader = BeautifulSoupWebReader()

    def custom_get(url, *args, **kwargs):
        headers = kwargs.get("headers", {})
        headers["User-Agent"] = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/123.0.0.0 Safari/537.36"
        kwargs["headers"] = headers
        return original_get(url, *args, **kwargs)

    original_get = requests.get

    requests.get = custom_get

    documents = loader.load_data(urls=[url])
    url_text = documents[0].text
    return url_text
