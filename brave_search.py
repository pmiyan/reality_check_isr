from brave import Brave

def get_news_documents(user_query, client, num_results, inclination):

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
    googles = {}

  #  googles['left'] = "https://raw.githubusercontent.com/allsides-news/brave-goggles/main/left.goggles"
    googles['left'] = "https://gist.githubusercontent.com/pmiyan/30faf37d38f86d031cccddbda15c58ef/raw/647c44f1918f1e993e006c9c3bde498aedad0127/left.goggles"
    googles['right'] = "https://raw.githubusercontent.com/allsides-news/brave-goggles/main/right.goggles"
    googles['unopinionated'] = "https://raw.githubusercontet.com/allsides-news/brave-goggles/main/right.goggles"
    googles['default'] = "https://gist.githubusercontent.com/pmiyan/30faf37d38f86d031cccddbda15c58ef/raw/647c44f1918f1e993e006c9c3bde498aedad0127/left.goggles"
    #create custom goggles - unbiased
    selected_google = googles[inclination]

    search_results = brave.search(q=query, count=num_results,
                                  # result_filter='news',
                                  freshness='py',
                                  spellcheck=True,
                                  goggles_id=selected_google,
                                  raw=True) #

    news_results = search_results["web"]["results"]

    # pprint(news_results)

    return news_results


