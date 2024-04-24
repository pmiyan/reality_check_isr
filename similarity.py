import json

def get_similarity(statement, context, client):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      response_format={ "type": "json_object" },
      messages=[
        {"role": "system",
         "content":
    """
    You are a fact checking AI designed to output JSON.
    Given a statement and context document sources where 
    each document starts as Source i, state if the statement 
    is true or false according to each source.
    State the reasoning for your answer, and also the confidence level.
    If the context is not enough to make a decision, state answer as "NULL"
    Keys in JSON object:
    - "answer": "TRUE" or "FALSE" or "NULL" (all uppercase)
    - "reasoning": "Your reasoning here."
    - "confidence": LOW, MEDIUM, HIGH (all uppercase)
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
    similarity_response = response.choices[0].message.content
    return json.loads(similarity_response)