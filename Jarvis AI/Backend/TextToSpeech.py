import pygame # import pygame library for handling audio playback.
import random # import random for generating random choices.
import asyncio # import asyncio for asynchronous operations.
import edge_tts # import edge_tts for text to speech function
import os # import os for file path handling
from dotenv import dotenv_values # import dotenv for reading envionment variables from .env

# Load environment variables from .env files
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")  # Get the assistant voice from the environment variables.

# Asynchronous function to convert text into an audio file.
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3" # Define the path where the speech file will be saved.
    
    if os.path.exists(file_path): # Check if the file already exists.
        os.remove(file_path) # If it exists, remove it avoid overwriting errors
        
    # Create communicate oibject to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%') 
    await communicate.save(r"Data\speech.mp3")  # Save the generated speech as an mp3 file
    
# Function to manage Text to Speech functionality
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(Text))
            
            # Initialize pygame mixer for audio playback
            pygame.mixer.init()
            
            # Load the generated speech file into pygame mixer
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play() # Play the audio
            
            # Loop until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)   # Let the loop to 10 ticks per second
                
            return True # Return True if the audio playerd successfully
        
        except Exception as e:  # Handle any exceptions during the process
            print(f"An error occured in TTS: {e}")     
            
        finally:
            try:
                # Call the provided function with false to signal the end of TTS
                func(False)
                pygame.mixer.music.stop() # Stop the audio playback
                pygame.mixer.quit()
                
            except Exception as e: # Handle any exception during cleanup
                print(f"An error occured in finally block: {e}")
                
# Function to manage Text To Speech with additional responsees for long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".") # Split the text by periods into a list of sentences
    
    # List of predefined responses for cases where the text is too long.
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    
    # If the text is very long (more the 4 sentences and 250 characters ), add a responses message.
    if len(Data) > 4 and len(Text) > 250:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func)
        
    # Otherwise, just play the whole text
    else:
        TTS(Text, func)
        
# Main execution loop
if __name__ == "__main__":
    while True:
        # Propmt user for input and [passes it to Text to Specch function
        TextToSpeech(input("Enter the text: "))     
                            

    
