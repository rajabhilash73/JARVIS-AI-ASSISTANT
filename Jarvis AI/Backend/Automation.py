from AppOpener import close, open as appopen # import function to open and close apps.
from webbrowser import open as webopen # import web browser function
from pywhatkit import search, playonyt # import functions for goole and youtube search
from dotenv import dotenv_values # import dotenv to manage environment variables
from bs4 import BeautifulSoup # import beautifulsoup for html content
from rich import print # for styled console output
from groq import Groq # for AI chat functioanlity
import webbrowser # import webbrowser for opening url's
import subprocess # import subprocess for the interacting with the system
import requests #import requests for making https requests
import keyboard # for keyboard related actions 
import asyncio # import asyncio for asynchronous programming
import os # import os for operating system functionalities

# Load environment variables from .env files
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")   # Retrive the groq API key

# Define CSS classes for parsing specific elements in html content
classes = ["zCubwf", "hgKElc", "LTKOO", "sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", 
               "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table",
               "dDoNo ikb4Bb gsrt", "sXLaOe", "LWKfKe", "VQF4g", "qv3Wpe", "Kno-rdeSc", "SPZz6b"]

# Define a user-agent for making web-requests
useragent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

# Initialize the Groq client with API key
client = Groq(api_key= GroqAPIKey)

# Predefined responses for user interactions.
responses = [
    "Your Satisfaction is my top priority; feel free to reach out if there's anything else I can help you with."
    "I am at your service for any additional questions or support you may need. Don't hesitate ask whenever you want."
]

# List to store chatbot messages
messages = []

# System message to provide context to the chatbot

SystemChatBot = SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You are an intelligent assistant that generates content based on the user's request. Respond appropriately based on the topic—code, letters, articles, etc.  " }]


# FUnctions to perform a google search
def GoogleSearch(Topic):
    search(Topic)  # Use pywhatkit search function to perform google search
    return True    # Indicate sucess

#GoogleSearch("Mahendra Singh Dhoni")
# Functions to generate content using AI and save it to a file.
def Content(Topic):
    # Nested function to open a file in a notepad
    def OpenNotepad(File):
        default_text_editor = "notepad.exe"   # Default text editor
        subprocess.Popen([default_text_editor, File])  # Open the file in notepad

    # Nested function to generate content using AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's prompt to the messages.

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )


        Answer = ""  # Initialize an empty string for the response

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True

# Content("application for a bank statement.")

# Function to search for a topic on youtube
def YouTubeSearch(Topic):
    Url4search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the youtube search url.
    webbrowser.open(Url4search) # Open the search url in web browser
    return True # Sign of Success

# FUnction tp play a video on youtube.
def PlayYouTube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video
    return True
# PlayYouTube("Ind Vs Pak 2023 Highlights")

# PlayYouTube("Hind ke Sitara")
# Function to open an application or a relevant webpage
def OpenApp(app, sess=requests.session()):
    
    try:
        appopen(app, match_closest = True, output = True, throw_error = True) # Attempt to open the app
        return True
    except:
        # Nested function to extract linkis from the HTML content
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser') # Prase the html content
            links = soup.find_all('a', {'jsname': 'UWckNb'}) # Find the relevant links
            return [link.get('href') for link in links]  # Return the links
        
        # Nested function to perform google search and retrive HTML.
        def search_google(query):
            url = f"https://www.google.com/search?q={query}" # construct the google search url
            headers = {"User-Agent": useragent} # Use the predefined user-agent.
            response = sess.get(url, headers=headers) # Perform the GET requests.
            
            if response.status_code == 200:
                return responses.text # Return the HTML content
            else:
                print("Failed to retrive such results.") # Print an error message
                return None
            
        html = search_google(app)   # Perform the google search
        
        if html:
            link = extract_links(html)[0] # Extract the first links from the search results
            webopen(link) # Open the link in web browser
            
        return True # Indicate success

# OpenApp("Prime Video")  
# Function to close an application
def CloseApp(app):
    
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True) # Attempt to close an app
            return True
        except:
            return False # Indicate error
# CloseApp("Prime Video")        
# Function to execute system- level command
def System(command):
    
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute") # mute key press    
        
    # Nested function to unmute the system volume. 
    def unmute():
        keyboard.press_and_release("volume unmute") # unmute key press    
        
    # Nested function to increase system volume
    def volume_up():
        keyboard.press_and_release("volume up")  # Volume up     
        
    # Nested function to decrease system volume.
    def volume_down():
        keyboard.press_and_release("volume down")  # Volume down
        
    # Execute the appropriate command
    if command == "mute":
        mute()    
    elif command == "unmute":
        unmute()
    elif command == "volume up" :
        volume_up()
    elif command == "volume down":
        volume_down()     
        
    return True # Indicate success   

# asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):
    
    funcs = [] # List to store asynchronous tasks
    
    for command in commands:
        
        if command.startswith("open "): # Handle open commands
            
            if "open it" in commands: # Ignore open it commands
                pass
            
            if "open file" == command: # Ignore open file command
                pass
            
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # Schedule app opening
                funcs.append(fun)
            
        elif command.startswith("general "): # placeholder for general ciommands    
            pass
        
        elif command.startswith("realtime "): # For realtime commands
            pass
        
        elif command.startswith("close "): # Close commands
            fun = asyncio.to_thread(OpenApp, command.removeprefix("close")) # App closing
            funcs.append(fun)
            
        elif command.startswith("play "): # Handle play commands
            fun = asyncio.to_thread(OpenApp, command.removeprefix("play")) 
            funcs.append(fun)
            
        elif command.startswith("content "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("content"))
            funcs.append(fun)    
            
        elif command.startswith("google search ")  :
            fun = asyncio.to_thread(OpenApp, command.removeprefix("google search")) 
            funcs.append(fun)   
            
        elif command.startswith("youtube search ")  :
            fun = asyncio.to_thread(OpenApp, command.removeprefix("youtube search")) 
            funcs.append(fun) 
            
        elif command.startswith("system ")  :
            fun = asyncio.to_thread(OpenApp, command.removeprefix("system")) 
            funcs.append(fun)             
            
        else:
            print(f"No Function Found. For {command}") # Print and error for unrecognized commands
            
    results = await asyncio.gather(*funcs)     # Execute all tasks concurrently
    
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result
            
# Asynchronous function to automate command execution
async def Automation(commands: list[str]):
    
    async for result in TranslateAndExecute(commands): # Translate and execute commands.
        pass
    
    return True # Indicate success.

# if __name__ == "__main__":
#     asyncio.run(Automation([]))
                      
            
                
           
                    
                
            
        
        
            
        
            
                
                
                
             
        


