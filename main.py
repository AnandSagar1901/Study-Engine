import os
from google import genai

client = genai.Client(api_key= os.getenv("API_KEY"))
def call_model(content):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=content+"Don't put any markdown as this currently being used in terminal",
    )

    return response.text


print("AI Study Engine")

response = ""

question = input("Please enter your question or topic you want to be explained:")

print("Explanation:")

print(call_model("Please explain "+question+" With 2 example problems+" + "Keep your Explanation 8-10 Bullet Points"))

response = input("Do you need another explanation(Y/N):")

while response == "Y":
    print(call_model("Please explain "+question+" With 2 example problems(if applicable)+" + "Keep your Explanation 8-10 Bullet Points"))
    response = input("Do you need another explanation(Y/N):")

print("Quiz")

response = input("How many questions do you want the quiz to be:")

quiz = call_model("Give me a multiple choice(Answer choices are ABCD not 1234) quiz on" + question + "That is " + response + "questions long" + "Don't give me the answer key")

print(quiz)

response = input("Please enter your answers(Ex: A,B,C,D):")

print(call_model("This is the quiz" + quiz + "Check these answers and give feedback" + response))
