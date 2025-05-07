import os
import re
import sqlite3
import subprocess
import time
import webbrowser
import speech_recognition as sr
from urllib.parse import quote
import pyautogui
from playsound import playsound
import eel
import pywhatkit as kit
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words
import random
import pygetwindow as gw
from plyer import notification
from engine.api import GEMINI_API_KEY
import google.generativeai as genai


# Configure the Gemini API with the API key
genai.configure(api_key=GEMINI_API_KEY)
# Connect to SQLite database for persistent reminders

# Connect to SQLite database
conn = sqlite3.connect("friday.db")
cursor = conn.cursor()
import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Define the speak function
def speak(text):
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def clean_query(query):
    # Remove filler phrases for more natural language understanding
    filler_phrases = [
        r"can you",
        r"could you",
        r"would you",
        r"please",
        r"do me a favor",
        r"hey",
        r"for me",
        r"just",
        r"kindly",
        r"open up",
        r"launch"
    ]

    query = query.lower()
    for phrase in filler_phrases:
        query = re.sub(phrase, "", query)

    return query.strip()

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = clean_query(query)

    # Extract the target app/site
    open_match = re.search(r"open (.+)", query)
    if open_match:
        query = open_match.group(1).strip()

    # List of natural responses
    opening_responses = [
        "Sure, opening {} now.",
        "Alright, let me open {} for you.",
        "Hold up, launching {}.",
        "Here you go, {} is opening.",
        "Opening {} as requested."
    ]

    if query:
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (query,))
            results = cursor.fetchall()

            if results:
                response = random.choice(opening_responses).format(query)
                speak(response)
                eel.receiverText(response)  # Add to chat history
                eel.DisplayMessage(response)  # Send response to UI
                os.startfile(results[0][0])
            else:
                cursor.execute('SELECT path FROM web_command WHERE name IN (?)', (query,))
                results = cursor.fetchall()

                if results:
                    response = random.choice(opening_responses).format(query)
                    speak(response)
                    eel.receiverText(response)  # Add to chat history
                    eel.DisplayMessage(response)  # Send response to UI
                    webbrowser.open(results[0][0])
                else:
                    response = f"Sorry, I couldn't find {query}."
                    speak(response)
                    eel.receiverText(response)  # Add to chat history
                    eel.DisplayMessage(response)  # Send response to UI
                    try:
                        os.system('start ' + query)
                    except:
                        response = "I wasn't able to open it."
                        speak(response)
                        eel.receiverText(response)  # Add to chat history
                        eel.DisplayMessage(response)  # Send response to UI
        except:
            response = "Something went wrong while trying to open the application."
            speak(response)
            eel.receiverText(response)  # Add to chat history
            eel.DisplayMessage(response)  # Send response to UI

def PlayYoutube(query):
    search_term = extract_yt_term(query)

    playing_responses = [
        "Got it! Playing {} on YouTube.",
        "Here you go, enjoy {}.",
        "Let me pull up {} on YouTube.",
        "Alright, starting {} now."
    ]

    speak(random.choice(playing_responses).format(search_term))
    kit.playonyt(search_term)
    
# import subprocess
# import time
# import pyautogui
# import pygetwindow as gw

def drawSquareInPaint():
    speak("Opening Paint and drawing a square.")
    
    # Open Paint without blocking execution
    subprocess.Popen("mspaint")  
    time.sleep(2)  # Wait for Paint to open

    # Bring Paint window to the front (ensure it's focused)
    paint_window = None
    for window in gw.getWindowsWithTitle("Paint"):  
        paint_window = window
        break

    if paint_window:
        paint_window.activate()  # Focus the Paint window
        time.sleep(1)  # Wait for focus to take effect
    else:
        speak("Unable to find Paint window.")
        return

    # Ensure Paint is in Brush or Pencil mode
    pyautogui.press('p')  # Select Pencil tool
    time.sleep(1)

    # Define the starting position and side length
    start_x, start_y = 500, 400  # Starting position
    side_length = 200  # Length of each side of the square

    # Click inside Paint to activate the drawing area
    pyautogui.click(start_x, start_y)  # Click at the starting position
    time.sleep(0.5)

    # Start drawing the square
    pyautogui.mouseDown()  # Press mouse down

    # Draw the four sides of the square
    pyautogui.dragTo(start_x + side_length, start_y, duration=0.5)  # Right
    pyautogui.dragTo(start_x + side_length, start_y + side_length, duration=0.5)  # Down
    pyautogui.dragTo(start_x, start_y + side_length, duration=0.5)  # Left
    pyautogui.dragTo(start_x, start_y, duration=0.5)  # Up (back to start)

    pyautogui.mouseUp()  # Release mouse

    speak("Square drawing completed.")
            
def hotword():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Handle background noise

        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=2)  # Capture audio
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")  # Debug print

                # Detect the word "friday" as standalone
                if re.search(r'\bfriday\b', command):
                    print("Wake word detected")
                    speak("Hello, how can I help you today?")  # Speak the text

                    # Simulate pressing Win + J
                    pyautogui.keyDown("win")
                    pyautogui.press("j")
                    time.sleep(2)
                    pyautogui.keyUp("win")
                    
            except sr.UnknownValueError:
                print("Could not understand audio")  # Feedback on failed recognition
            except sr.RequestError as e:
                print(f"Error: Unable to access speech recognition service; {e}")

def control_window(query):
    query = clean_query(query)  # Use your existing clean_query function
    
    # Extract the window title and action from the query
    if "google chrome" in query.lower():
        window_title = "Google Chrome"
    elif "notepad" in query.lower():
        window_title = "Notepad"
    elif "firefox" in query.lower():
        window_title = "Mozilla Firefox"
    else:
        speak("Sorry, I don't support controlling that window.")
        return
    
    # Handle window actions
    if "minimize" in query:
        try:
            target_window = gw.getWindowsWithTitle(window_title)[0]
            target_window.minimize()
            speak(f"{window_title} minimized.")
        except IndexError:
            speak(f"{window_title} window not found.")
    elif "maximize" in query:
        try:
            target_window = gw.getWindowsWithTitle(window_title)[0]
            target_window.maximize()
            speak(f"{window_title} maximized.")
        except IndexError:
            speak(f"{window_title} window not found.")
    elif "restore" in query:
        try:
            target_window = gw.getWindowsWithTitle(window_title)[0]
            target_window.restore()
            speak(f"{window_title} restored.")
        except IndexError:
            speak(f"{window_title} window not found.")
    else:
        speak("Sorry, I didn't understand that window control command.")

@eel.expose
def get_chat_response(query):
    response = chatBot(query)  # Call the chatBot function
    return response  # Return the AI-generated response

def chatBot(query):
    user_input = query.lower()
    
    # Add a prompt for short answers
    prompt = f"Give a short and precise answer as human: {user_input}"
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    # Generate a response
    response = model.generate_content(prompt)
    response_text = response.text.strip()  # Remove extra spaces
    
    if response_text:
        eel.DisplayMessage(response_text)  # Send response to frontend
        return response_text  # Return response but DO NOT speak it here

    return "Sorry, I couldn't generate a response."

task_list = []

def add_task(task_name):
    """
    Add a task to the task list.
    """
    task_list.append(task_name)

def remove_task(task_name):
    """
    Remove a task from the task list.
    """
    if task_name in task_list:
        task_list.remove(task_name)
    else:
        raise ValueError(f"Task '{task_name}' not found.")

def get_task_list():
    """
    Retrieve the list of tasks.
    """
    return task_list

def list_tasks():
    """
    Retrieve and display/speak the list of tasks.
    """
    if not task_list:
        return "You have no tasks."
    elif len(task_list) == 1:
        return f"You have 1 task: {task_list[0]}"
    else:
        return "Your tasks are: " + ", ".join(task_list)