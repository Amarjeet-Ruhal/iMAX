import os
import pygame
from gtts import gTTS
from dotenv import load_dotenv
import google.generativeai as genai
import speech_recognition as sr
import pandas as pd
import numpy as np
import re

import dateparser
from datetime import datetime

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
    



# Function to save demo schedule details to a file
def save_demo_schedule(details):
    try:
        file_path = os.path.join(os.getcwd(), "demo_schedule.txt")
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(details + "\n")
        print(f"Demo scheduled and saved to {file_path}")
    except Exception as e:
        print(f"File write error: {e}")

    
def parse_date(input_text):
    parsed = dateparser.parse(input_text)
    if parsed and parsed.date() >= datetime.today().date():
        return parsed.strftime("%d %B %Y")  # e.g., "21 May 2025"
    return None

def parse_time(input_text):
    parsed = dateparser.parse(input_text)
    if parsed:
        return parsed.strftime("%I:%M %p")  # e.g., "03:30 PM"
    return None

def collect_demo_details():
    details = {}

    while True:
        print("AI: What is the title of the demo?")
        speak("What is the title of the demo?")
        user_input = recognize_speech()
        details["title"] = user_input
        print("User:", user_input)
        if user_input != "Sorry, I didn't understand that.":
            break
        else:
            print("AI: I couldn't understand the title. Please try again.")
            speak("I couldn't understand the title. Please try again.")

    # Date collection with validation
    while True:
        print("AI: On which date would you like to schedule the demo?")
        speak("On which date would you like to schedule the demo?")
        date_input = recognize_speech()
        print("User:", date_input)
        parsed_date = parse_date(date_input)
        if parsed_date:
            details["date"] = parsed_date
            break
        else:
            print("AI: I couldn't understand the date. Please try again.")
            speak("I couldn't understand the date. Please try again.")

    # Time collection with validation
    while True:
        print("AI: At what time should the demo be scheduled?")
        speak("At what time should the demo be scheduled?")
        time_input = recognize_speech()
        print("User:", time_input)
        parsed_time = parse_time(time_input)
        if parsed_time:
            details["time"] = parsed_time
            break
        else:
            print("AI: I couldn't understand the time. Please try again.")
            speak("I couldn't understand the time. Please try again.")

    while True:
        print("AI: Who is the participant?")
        speak("Who is the participant?")
        user_input = recognize_speech()
        details["participant"] = user_input
        print("User:", user_input)
        if user_input != "Sorry, I didn't understand that.":
            break
        else:
            print("AI: I couldn't understand the participant's name. Please try again.")
            speak("I couldn't understand the participant's name. Please try again.")

    confirmation_text = f"{details['title']} is scheduled on {details['date']} at {details['time']} with {details['participant']}."
    print("AI: Confirmation:", confirmation_text)
    speak(f"Got it. {confirmation_text}")
    save_demo_schedule(confirmation_text)

    print("AI: Do you want another scheduling? if yes then say yes, I wa")
    speak("Do you want another scheduling?")
    user_input = recognize_speech()
    print("User:", user_input)
    if "yes" in user_input.lower() or "another" in user_input.lower():
        collect_demo_details()




def load_payment_data(file_path="invoice_tracker_example.csv"):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

def search_payment_info(data, query):
    query = query.strip().lower()
    for _, row in data.iterrows():
        customer = str(row.get("Customer Name", "")).lower()
        invoice = str(row.get("Invoice No.", ""))

        pattern = r'\b{}\b'.format(invoice)
        x=False
        if re.search(pattern, query):
            x=True

        # Try matching against customer name or invoice number
        if customer in query or x:
            return {
                "Customer": row.get("Customer Name", "N/A"),
                "Invoice": row.get("Invoice No.", "N/A"),
                "Amount": row.get("Total Amount Due", "N/A"),
                "Status": row.get("Outstanding / Balance Due", "N/A"),
                "Due Date": row.get("Payment Due Date", "N/A")
            }
    return None




def determine_mode(user_input):
    if any(word in user_input.lower() for word in ["demo", "erp", "schedule"]):
        return "demo_scheduling"
    elif any(word in user_input.lower() for word in ["interview", "job", "screening"]):
        return "interview"
    elif any(word in user_input.lower() for word in ["payment", "order", "follow-up"]):
        return "payment_followup"
    return None

def generate_response(user_input, mode, payment_data=None):
    try:
        if mode == "payment_followup" and payment_data is not None:
            speak("Please provide Invoive number or customer name for the payment details you want to check.")
            print("AI: Please provide Invoive number or customer name for the payment details you want to check.")
            user_input = recognize_speech()
            print("User:", user_input)
            if user_input.lower() in ["exit", "stop"]:
                return "exit"
            info = search_payment_info(payment_data, user_input)
            if info:
                return (
                    f"Payment information for {info['Customer']}:\n"
                    f"Invoice No: {info['Invoice']}, Amount: ₹{info['Amount']}, "
                    f"Balance: ₹{info['Status']}, Due Date: {info['Due Date']}."
                )
            else:
                return generate_response(user_input, mode,payment_data)

        # Gemini fallback
        prompts = {
            "interview": "You are an AI recruiter for initial screenings. Keep responses precise and ask only key questions and don't use * while speaking.",
            # "payment_followup": "You are following up on payments/orders. Be direct and confirm details briefly and don't use * while speaking."
        }
        prompt = f"{prompts[mode]} Respond briefly to: {user_input}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI response error: {e}")
        return "I'm sorry, I encountered an issue."





def cold_call():
    payment_data = load_payment_data()

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

        if mode == "demo_scheduling":
            collect_demo_details()
            speak("Do you want to exit? If yes then say exit")
            user_input = recognize_speech()
            if "yes" in user_input.lower() or "exit" in user_input.lower():
                speak("Thank you! Goodbye.")
                break
            else:
                speak("Let's continue. Do you want to change the mode?")
        else:
            ai_response = generate_response(user_input, mode, payment_data)
            if ai_response == "exit":
                speak("Thank you! Goodbye.")
                break
            print("AI:", ai_response)
            speak(ai_response)

        user_input = recognize_speech()



if __name__ == "__main__":
    cold_call()
