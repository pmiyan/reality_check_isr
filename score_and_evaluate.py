'''Generates a score based on the cumulative responses'''

import json

def generate_score(responses):
    total_score = 0
    total_weight = 0

    for response in responses:
        answer = response['answer'].upper()

        if answer == 'NULL':
            continue
        elif answer == 'TRUE':
            score = 1
        elif answer == 'FALSE':
            score = -1
        else:
            score = 0

        confidence = response['confidence'].upper()

        # Assigning weights based on confidence levels
        if confidence == 'HIGH':
            weight = 2
        elif confidence == 'MEDIUM':
            weight = 1.5
        elif confidence == 'LOW':
            weight = 1
        else:
            weight = 0

        total_score += score * weight
        total_weight += weight

    if total_weight == 0:
        return 0  # Avoid division by zero

    overall_score = total_score / total_weight

    return overall_score


def determine_fake_news(score):
    categories = {
        (-1, -0.71): ("High Confidence False", "#FF5733"),  # Red
        (-0.71, -0.36): ("Medium Confidence False", "#FFA833"),  # Orange
        (-0.36, -0.21): ("Low-Medium Confidence False", "#FFD133"),  # Yellow
        (-0.21, 0.21): ("Uncertain", "#D3D3D3"),  # Gray
        (0.21, 0.36): ("Low-Medium Confidence True", "#FFD133"),  # Yellow
        (0.36, 0.71): ("Medium Confidence True", "#3CB371"),  # Green
        (0.71, 1): ("High Confidence True", "#006400")  # Dark Green
    }

    for range_, (label, color) in categories.items():
        if range_[0] <= score <= range_[1]:
            return label, color


def generate_text_response(responses, fake_o_meter, score, client):
    # Based on the meter value, generate a response by passing all the context
    # from the responses to GPT-3.5 and summarize the responses
    if score >= 0.21:
        # Get all the true responses and summarize the content
        context = [response['context'] for response in responses.values() if response['answer'].upper() == 'TRUE']
    elif score <= -0.21:
        # Get all the false responses and summarize the content
        context = [response['context'] for response in responses.values() if response['answer'].upper() == 'FALSE']
    else:
        # Get all the uncertain responses and summarize the content
        context = [response['context'] for response in responses.values()]

    context_str = "\n".join(context)
    # Generate a response based on the context
    res = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content":
                 """
                 You are a summarizer. Given all the context from various sources,
                 summarize the content and provide a conclusion.
                 """},
            {"role": "user",
             "content":
                 f"""
                    Decision: {fake_o_meter}
                    
                    Context: {context_str}
                """},
        ]
    )
    response_context = res.choices[0].message.content
    print(response_context)
    return response_context

'''Returns text response based on the cumulative responses'''
def evaluate_responses(responses, client):
    score = generate_score(responses.values())
    fake_o_meter, fake_o_color = determine_fake_news(score)
    print(f"Score: {score}")
    print(f"Fake-o-Meter: {fake_o_meter}")
    print(f"Fake-o-Color: {fake_o_color}")
    score_context = generate_text_response(responses, fake_o_meter, score, client)
    return (score, fake_o_meter, score_context)