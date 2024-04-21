from dotenv import load_dotenv
load_dotenv()

from llama_index.core import VectorStoreIndex, download_loader
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.web import BeautifulSoupWebReader
from openai import OpenAI
client = OpenAI()

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

url_list = ["https://www.cnn.com/2023/09/26/politics/trump-organization-business-fraud/index.html"]#, "https://apnews.com/article/gaza-israel-aid-pier-us-military-e988256270fc0067d2f5524fd542a475"]
for url in url_list:
    documents = loader.load_data(urls=[url])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
             "content":
                 """
                 You are a fact checking AI designed to output JSON.
                 Given a statement and some context, state if it is true or false.
                 State the reasoning for your answer, and also the confidence level.
                 Keys in JSON object:
                 - "answer": "true" or "false"
                 - "reasoning": "Your reasoning here."
                 - "confidence": Low, Medium, High
                 - "context": "The context of the statement in document."
                 """},
            {"role": "user",
             "content":
                 f"""
                 Context:
                 {documents[0].text}
                 Statement: 'Donald Trump got convicted of fraud'.
                 """},
        ]
    )
    print(response.choices[0].message.content)
    print("Hello")

