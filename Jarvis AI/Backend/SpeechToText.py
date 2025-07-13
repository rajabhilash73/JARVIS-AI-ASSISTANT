from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environent variables from the .env file
env_vars = dotenv_values(".env")

# Get the input language setting from the environment variables.
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;
        let isRecognizing = false;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || newSpeechRecognition();
            recognition.lang = 'en';
            recognition.continuous = true;
        
            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };
        
            recognition.onend = function() {
                if (isRecognizing) {
                    recognition.start();
                }
            };
            isRecognizing = true;
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                isRecognizing = false;
                recognition.stop();
            }
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environment variables.
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Write the modified Html Code to a file.
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)
    
# Get the current working directory
current_dir = os.getcwd()

# Generate the gfile path for the Html file.
Link = f"{current_dir}/Data/Voice.html"

# Set chrome option for the WebDriver.
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36" 
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument("--headless=new")

# Initialize the chrome WebDriver using the ChromeDriverManager.

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for temporary files.
TempDirPath = rf"{current_dir}/Frontend/Files"

# Functions to set the assistant's status by writing it to a file.
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)
        
# Function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["what", "where", "who", "how", "which", "when", "why", "whose", "whom", "can you", "what's", "where's", "how's", "can you"]      
    
    # Check if the query is a question and add a question marks if necessary.
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"    
    else:
        # Add a period if the query is not a question.
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."    
            
    return new_query.capitalize()   

# Function to translate text into english using thje mtranslate library.
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")    
    return english_translation.capitalize()

# Function to perform speech recognition using the webdriver.
def SpeechRecognition():
    # Open the Html file in the web browser.
    driver.get("file:///" + Link)
    # Start speech recognition by clicking the start button.
    driver.find_element(by=By.ID, value="start").click()
    
    while True:
        try:
            # Get the reocgnized text from the html output element
            Text = driver.find_element(by=By.ID, value="output").text
            
            if Text:
                # Stop recognition by clicking the stop button.
                driver.find_element(by=By.ID, value="end").click()
                
                # If the input language is english, return the modified query.
                if InputLanguage.lower() =="en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    # If the input language is not english, translate the text anjd return it.
                    SetAssistantStatus("Translating ....")
                    return QueryModifier(UniversalTranslator(Text))
                
        except Exception as e:
            pass
        
# Main execution block.
if __name__ == "__main__":
    while True:
        # Continously perform speech recognitoin and print the recognized text.
        Text = SpeechRecognition()
        print(Text)              
 
             
              