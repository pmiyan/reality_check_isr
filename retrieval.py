# from llama_index.core import Settings
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import re
from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": ("Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; "
                   "+http://www.google.com/bot.html) Chrome/123.0.0.0 Safari/537.36")
}


def clean_text(text):
    # Replace multiple newlines with one newline
    cleaned_text = re.sub(r'\n+', '\n', text)
    # Replace multiple spaces with one space
    cleaned_text = re.sub(r' +', ' ', cleaned_text)
    # Replace multiple tabs with one tab
    cleaned_text = re.sub(r'\t+', '\t', cleaned_text)
    return cleaned_text.strip()


def retrieve_url_data(url):
    print("retrieving url data...:", url)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.title.string
    main_tag = soup.find('main')
    if main_tag:
        data = clean_text(main_tag.getText())
    else:
        data = clean_text(soup.getText())
    return title, data
