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


    googles['left'] = "https://github.com/pmiyan/reality_check_isr/blob/c89507c3d1259b8dcf68d3870c7e3104204ec5a6/left.goggles"
    googles['right'] = "https://github.com/pmiyan/reality_check_isr/blob/c89507c3d1259b8dcf68d3870c7e3104204ec5a6/right.goggles"
    googles['unopinionated'] = "https://raw.githubusercontent.com/pmiyan/reality_check_isr/151b63a59c03678a0d6c706477b35a6ae47013db/goggles"
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


