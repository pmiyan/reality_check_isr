from brave import Brave

def get_news_documents(user_query, client, num_results):

    brave = Brave()

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      temperature=0.3,
      messages=[
        {"role": "system", "content": ("As a fact-checking assistant, help me convert the following user input into a prompt"
                                       " for google search. Only reply with the best converted prompt."
                                       "Do not add quotes around the generated prompt."
                                       "Your input will be directly sent to google search.")},
        {"role": "user", "content": user_query}
      ]
    )

    query = completion.choices[0].message.content
    left_goggles = "https://raw.githubusercontent.com/allsides-news/brave-goggles/main/left.goggles"
    right_goggles = "https://raw.githubusercontent.com/allsides-news/brave-goggles/main/right.goggles"
    #create custom goggles - unbiased

    search_results = brave.search(q=query, count=num_results,
                                  # result_filter='news',
                                  freshness='py',
                                  spellcheck=True,
                                  goggles_id="https://gist.githubusercontent.com/pmiyan/30faf37d38f86d031cccddbda15c58ef/raw/647c44f1918f1e993e006c9c3bde498aedad0127/left.goggles",
                                  raw=True) #

    news_results = search_results["web"]["results"]

    # pprint(news_results)

    return news_results


