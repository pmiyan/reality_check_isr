from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

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
"""},
    {"role": "user",
     "content":
"""
Context:
Taylor Alison Swift (born December 13, 1989) is an American singer-songwriter. Her reinventive artistry, distinctive songwriting and entrepreneurship have been widely publicized and influential.

Swift began professional songwriting at age 14. She signed with Big Machine Records in 2005 and achieved prominence as a country pop singer with the albums Taylor Swift (2006) and Fearless (2008).
Their singles "Teardrops on My Guitar", "Love Story", and "You Belong with Me" were crossover successes on country and pop radio formats and brought Swift mainstream fame.
She experimented with rock and electronic styles on her next albums, Speak Now (2010) and Red (2012), respectively, with the latter featuring her first Billboard Hot 100
number-one single, "We Are Never Ever Getting Back Together". Swift recalibrated her image from country to pop with 1989 (2014), a synth-pop album containing the chart-topping
songs "Shake It Off", "Blank Space", and "Bad Blood". Media scrutiny inspired the hip-hop-influenced Reputation (2017) and its number-one single "Look What You Made Me Do".

Statement: Taylor Swift is a rap artist.
"""},
  ]
)
print(response.choices[0].message.content)