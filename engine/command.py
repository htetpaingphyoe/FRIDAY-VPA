import pyttsx3
import speech_recognition as sr
import eel
import time
import sys
import sqlite3
from engine.task_manager import add_task, remove_task, list_tasks
from engine.api import GEMINI_API_KEY
import google.generativeai as genai

# Configure the Gemini API with the API key
genai.configure(api_key=GEMINI_API_KEY)

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voices', voices[0].id)
    engine.setProperty('rate', 150)
    eel.DisplayMessage(text)
    # print(voices)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()
    
@eel.expose
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)
    try:
        print('recognizing')
        eel.DisplayMessage('recognizing...')
        query = r.recognize_google(audio, language='en')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        # speak(query)
    except Exception as e:
        return ""
    return query.lower()

@eel.expose
def allCommands(message=1):
    try:
        if message == 1:
            query = takecommand()  # Capture voice input
            print(query)
            # eel.senderText(query)
        else:
            query = message  # Use the provided text input
        print(f"User said: {query}")
        eel.senderText(query)  # Send user input to the frontend

        # Retry up to 3 times if the query is empty
        retry_count = 0
        while not query and retry_count < 3:
            speak("I didn't catch that. Could you repeat?")
            retry_count += 1
            query = takecommand()

        if not query:
            speak("Sorry, I'm still not hearing anything. Let's try later.")
            return

        # Handle different commands
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif any(keyword in query for keyword in ["minimize", "maximize", "restore"]):
            from engine.features import control_window
            control_window(query)
        elif "draw a square" in query:
            from engine.features import drawSquareInPaint
            drawSquareInPaint()
        elif "stop" in query or "thank you" in query:  # New condition for "stop" or "thank you"
            speak("Goodbye sir, have a good day.")
            time.sleep(1)
            eel.closeWindow()
            time.sleep(1)
            sys.exit()
        elif "add" in query or "make schedule for" in query:
            handle_add_task(query)
        elif "list tasks" in query or "list of the task" in query:
            tasks_message = list_tasks()
            speak(tasks_message)
            eel.DisplayMessage(tasks_message)  # Send task list to the frontend
        elif "remove task" in query or "remove" in query:
            handle_remove_task(query)
        else:
            handle_chatbot(query)

    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred while processing your request.")

    eel.ShowHood()  # Update the UI

def handle_add_task(query):
    """
    Extract the task name from the query and add it to the task list.
    """
    try:
        # Extract the task name from the query
        task_name = query.replace("add task", "").strip()
        task_name = query.replace("make schedule for", "").strip()
        
        # Check if the task name is empty
        if not task_name:
            speak("Please specify a task name.")
            return

        # Add the task using the simplified task management system
        add_task(task_name)  # Add the task without time
        speak(f"Task '{task_name}' added successfully.")

    except Exception as e:
        print(f"Error in handle_add_task: {e}")
        speak("An error occurred while adding the task.")
        
@eel.expose
def save_command(sys_name, sys_path, web_name, web_url):
    try:
        conn = sqlite3.connect("friday.db")  # Connect to SQLite database
        cursor = conn.cursor()

        if sys_name and sys_path:
            print(f"Inserting System Command: {sys_name} - {sys_path}")
            cursor.execute("INSERT INTO sys_command (name, path) VALUES (?, ?)", (sys_name, sys_path))

        if web_name and web_url:
            print(f"Inserting Web Command: {web_name} - {web_url}")
            cursor.execute("INSERT INTO web_command (name, path) VALUES (?, ?)", (web_name, web_url))

        conn.commit()  # Save changes
        conn.close()   # Close connection

        print("Command saved successfully!")
        return "Command saved successfully!"  # Send message back to UI

    except Exception as e:
        print("Error saving command:", str(e))  # Print exact error
        return f"Error saving command: {str(e)}"  # Send error message to UI
    
def handle_remove_task(query):
    """
    Extract the task name from the query and remove it from the task list.
    """
    try:
        # Extract the task name from the query
        task_name = query.replace("remove task", "").strip()
        task_name = query.replace("remove", "").strip()
        if not task_name:
            speak("Please specify a task name.")
            return

        # Remove the task using the simplified task management system
        remove_task(task_name)
        speak(f"Task '{task_name}' removed successfully.")

    except Exception as e:
        print(f"Error in handle_remove_task: {e}")
        speak("An error occurred while removing the task.")

def handle_chatbot(query):
    """Handles chatbot queries (Gemini API)."""
    from engine.features import chatBot  # Import inside function to avoid circular import
    
    response = chatBot(query)  # Get response from Gemini API
    
    if response:
        speak(response)  # Speak only once