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


    print("Explanation:")

    print(call_model("Please explain "+question+" With 2 example problems+" + "Keep your Explanation 8-10 Bullet Points"))

    response = input("Do you need another explanation(Y/N):")

    while response == "Y":
        print(call_model("Please explain "+question+" With 2 example problems(if applicable) with answers+" + "Keep your Explanation 8-10 Bullet Points"))
        response = input("Do you need another explanation(Y/N):")

    print("Quiz")

    response = input("How many questions do you want the quiz to be:")

    quiz = call_model("Give me a multiple choice(Answer choices are ABCD not 1234) quiz on" + question + "That is " + response + "questions long" + "Don't give me the answer key")

    print(quiz)

    response = input("Please enter your answers(Ex: A,B,C,D):")

    text = (call_model("This is the quiz" + quiz + "Check these answers and give feedback" + response + "At the top of the output return the score in this format: 'Score: (Correct answers)/(Total Questions)' in this exact format down to the spaces" + " Don't put any other text before or on the line of the Score"))

    print(text)

    l1 = text.split()

    full_question = {"topic" : question, "date": str(date.today()), "score": str(l1[1])}

    with open("data.json", "r") as f:
        data = json.load(f)
        
    data["topics"].append(full_question)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    
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
    average = 0

    for i in data["topics"]:
        score = i["score"]

        parts = score.split("/")

        correct = int(parts[0])
        total = int(parts[1])

        average += (correct / total) * 100

    average = average / len(data["topics"])

    print("Last studied topic: " + data["topics"][-1]["topic"])
    print("Last study date: " + data["topics"][-1]["date"])
    print("Total topics studied: " + str(len(data["topics"])))
    print("Total unique topics: " + str(len(set(topic_names))))
    print("Average Accuracy: " + str(round(average, 2)) + "%")

print("AI Study Engine")

print("1. Study")
print("2. View History")
print("3. Cleanup")
print("4. View Stats")

response = int(input("Choose an option:"))

while response not in l1:
    response = int(input("Please enter 1, 2, 3, 4: "))
while response != 4:
    if response == 1:
        study()
    elif response == 2:
        history()
    elif response == 3:
        clean_up()

    print("1. Study")
    print("2. View History")
    print("3. Cleanup")
    print("4. View Stats")

    response = int(input("Choose an option:"))

    while response not in l1:
        response = int(input("Please enter 1, 2, 3, 4: "))
if response == 4:
        check_stats()

