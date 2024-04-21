def get_similarity(statement, context, client):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      response_format={ "type": "json_object" },
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
                Context: {context}
                Statement: {statement}
            """},
      ]
    )
    similaity_response = response.choices[0].message.content
    return similaity_response