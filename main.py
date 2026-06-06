import os
from google import genai
import json
from datetime import datetime, date

client = genai.Client(api_key= os.getenv("API_KEY"))
l1 = [1, 2, 3, 4]
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
    full_question = {"topic" : question, "date": str(date.today())}

    with open("data.json", "r") as f:
        data = json.load(f)
        
    data["topics"].append(full_question)

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
        topic = str(topic)
        topic = topic.replace("{","")
        topic = topic.replace("}","")
        topic = topic.replace("'","")
        print("-", topic)

def clean_up():
    with open("data.json", "r") as f:
        data = json.load(f)

    cleaned_json = call_model( "Remove duplicate topics from this JSON and return ONLY valid JSON:\n" + json.dumps(data) )
    cleaned_data = json.loads(cleaned_json) 
    with open("data.json", "w") as f: json.dump(cleaned_data, f, indent=4) 
    print("Cleanup complete!")

def check_stats():
    with open("data.json", "r") as f:
        data = json.load(f)

    if len(data["topics"]) == 0:
        print("No topics studied yet.")
        return

    topic_names = []

    for topic in data["topics"]:
        topic_names.append(topic["topic"])

    print("Last studied topic: " + data["topics"][-1]["topic"])
    print("Last study date: " + data["topics"][-1]["date"])
    print("Total topics studied: " + str(len(data["topics"])))
    print("Total unique topics: " + str(len(set(topic_names))))

print("AI Study Engine")

print("1. Study")
print("2. View History")
print("3. Cleanup")
print("4. View Stats")

response = int(input("Choose an option:"))

while response not in l1:
    response = int(input("Please enter 1, 2, 3, 4: "))

if response == 1:
    study()
elif response == 2:
    history()
elif response == 3:
    clean_up()
elif response == 4:
    check_stats()

