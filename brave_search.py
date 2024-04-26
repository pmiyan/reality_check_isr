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
    googles['left'] = "https://raw.githubusercontent.com/pmiyan/reality_check_isr/5993f835cb12e59efa2a7273adf17c7a088d088e/goggles"
    googles['right'] = "https://raw.githubusercontent.com/allsides-news/brave-goggles/main/right.goggles"
    googles['neutral'] = "https://raw.githubusercontent.com/allsides-news/brave-goggles/main/right.goggles"
    googles['default'] = "https://raw.githubusercontent.com/pmiyan/reality_check_isr/5993f835cb12e59efa2a7273adf17c7a088d088e/goggles"
    #create custom goggles - unbiased
    selected_google = None
    if inclination:
        selected_google = googles[inclination]
    else:
        selected_google = googles['default']

    search_results = brave.search(q=query, count=num_results,
                                  # result_filter='news',
                                  freshness='py',
                                  spellcheck=True,
                                  goggles_id=selected_google,
                                  raw=True) #

    news_results = search_results["web"]["results"]

    # pprint(news_results)

    return news_results


