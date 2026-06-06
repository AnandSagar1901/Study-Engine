import os
from google import genai
import json

client = genai.Client(api_key= os.getenv("API_KEY"))
def call_model(content):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=content+"Don't put any markdown as this currently being used in terminal",
    )

    return response.text

if not os.path.exists("data.json"):
    with open("data.json", "w") as f:
        json.dump({"topics": []}, f, indent=4)

def study():
    question = input("Please enter your question or topic you want to be explained:")

    with open("data.json", "r") as f:
        data = json.load(f)
        
    data["topics"].append(question)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

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

def history():
    with open("data.json", "r") as f:
        data = json.load(f)

    print("\nTopics studied:")
    for topic in data["topics"]:
        print("-", topic)

def clean_up():
    with open("data.json", "r") as f:
        data = json.load(f)
        print(data)
    call_model("Please delete any duplicates in this data and return only in JSON nothing else: " + data )

print("AI Study Engine")

print("1. Study")
print("2. View History")
print("3. Cleanup")

response = int(input("Choose an option: "))

while response != 1 or 2 or 3:
    response = int(input("Please enter 1, 2, or 3: "))

if response == 1:
    study()
elif response == 2:
    history()
elif response == 3:
    clean_up

