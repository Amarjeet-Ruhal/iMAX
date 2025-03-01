import os
import pygame
from gtts import gTTS
from dotenv import load_dotenv
import google.generativeai as genai
import speech_recognition as sr

# Load API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize Speech Recognition
recognizer = sr.Recognizer()
pygame.mixer.init()

def speak(text):
    try:
        pygame.mixer.music.unload()
        tts = gTTS(text=text, lang='hi')
        temp_file = "temp_audio.mp3"
        tts.save(temp_file)
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        os.remove(temp_file)
    except Exception as e:
        print(f"Speech synthesis error: {e}")

def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't understand that."
    except Exception as e:
        print(f"Speech recognition error: {e}")
        return "Error recognizing speech."

def determine_mode(user_input):
    if any(word in user_input.lower() for word in ["demo", "erp", "schedule"]):
        return "demo_scheduling"
    elif any(word in user_input.lower() for word in ["interview", "job", "screening"]):
        return "interview"
    elif any(word in user_input.lower() for word in ["payment", "order", "follow-up"]):
        return "payment_followup"
    return None

def generate_response(user_input, mode):
    try:
        prompts = {
            "demo_scheduling": "You are scheduling ERP demos. Keep responses short and confirm appointments quickly.",
            "interview": "You are an AI recruiter for initial screenings. Keep responses precise and ask only key questions.",
            "payment_followup": "You are following up on payments/orders. Be direct and confirm details briefly."
        }
        
        prompt = f"{prompts[mode]} Respond briefly to: {user_input}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI response error: {e}")
        return "I'm sorry, I encountered an issue."

def save_demo_schedule(details):
    try:
        with open("demo_schedule.txt", "a") as file:
            file.write(details + "\n")
        print("Demo scheduled and saved.")
    except Exception as e:
        print(f"File write error: {e}")

def cold_call():
    speak("Hello! How can I assist you today? Are you looking to schedule a demo, attend an interview, or follow up on a payment or order?")
    user_input = recognize_speech()
    mode = determine_mode(user_input)
    
    if not mode:
        speak("I'm sorry, I couldn't determine the task. Please mention demo scheduling, interview, or payment follow-up.")
        return
    
    while True:
        print("User:", user_input)
        
        if "exit" in user_input.lower() or "stop" in user_input.lower():
            speak("Thank you! Goodbye.")
            break
        
        new_mode = determine_mode(user_input)
        if new_mode and new_mode != mode:
            mode = new_mode
            speak(f"Switching to {mode.replace('_', ' ')} mode.")
            continue
        
        ai_response = generate_response(user_input, mode)
        print("AI:", ai_response)
        speak(ai_response)
        
        if mode == "demo_scheduling" and "confirm" in ai_response.lower():
            save_demo_schedule(f"Scheduled demo: {user_input}")
        
        user_input = recognize_speech()

if __name__ == "__main__":
    cold_call()
