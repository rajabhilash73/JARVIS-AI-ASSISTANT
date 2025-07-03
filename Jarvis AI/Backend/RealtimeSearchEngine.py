from googlesearch import search
from groq import Groq
from dotenv import dotenv_values
from json import load, dump
import datetime

# Load environment variables from the .env files.
env_vars = dotenv_values(".env")

# Retrive environment variables for jusername, assistname and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Goq client using the provided API Key.
client = Groq(api_key=GroqAPIKey)

# Define the system instructions to the chatbots.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to log the chatlog to the json file , and create the empty one if doesn't exist.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLogg.json", "w") as f:
        dump([], f)
        
# Function to perform a Google search and format the results.
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))  
    Answer = f"The search results for {query} are:\n[start]\n"   
    
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
        
    Answer += "[end]"
    print(Answer)
    return Answer
    
# Function to clean up the answer by removing thje empty lines
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation systemj and initiql user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hello, how can I assist you today?"}
]

# Function to get real-time information liike the current date and time.
def Information():
    data = ""
    current_date_time = datetime.datetime.now() 
    day = current_date_time.strftime("%A") 
    date = current_date_time.strftime("%d") 
    month = current_date_time.strftime("%B") 
    year = current_date_time.strftime("%Y") 
    hour = current_date_time.strftime("%H") 
    minute = current_date_time.strftime("%M") 
    second = current_date_time.strftime("%S")
    data += f"Use this Real-Time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data

# Function to handle Real-time search engine and response generation.
def RealTimeSearchEngine(prompt):
    global SystemChatBot, messages
    
    # Load the chatlog from the json file.
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})    
    
    # Add Google search results to the system chat bots message
    SystemChatBot.append({"role": "user", "content": GoogleSearch(prompt)})
    
    # Generate the resiponse using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-70b-8192", 
        messages=SystemChatBot + [{"role": "user", "content": Information()}] + messages, 
        temperature=0.7, 
        max_tokens=2048,
        top_p=1, 
        stream=True, 
        stop=None 
    )
    
    Answer = ""
    
    # Concatenate response chunks from the streaming response.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
            
    # Clean up the response
    Answer = Answer.strip().replace("</s>", "")        
    messages.append({"role": "assistant", "content": Answer})
    
    # Save the updated chatlogt back to the json file.
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
        
    # Remove the most recent user message from the chatlog
    SystemChatBot.pop() 
    return AnswerModifier(Answer)  

# Main entry point of the program for the interactive searches.
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealTimeSearchEngine(prompt)) 
       
       