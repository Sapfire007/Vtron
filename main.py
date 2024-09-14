import io
import sys
import threading
import pyttsx3    # This module will be used to convert text to speech
import speech_recognition as sr
import keyboard
import os
import subprocess as sp          # The Python subprocess module empowers the creation and interaction with child processes, which enables the execution of external programs or commands.
import imdb
import wolframalpha
import openai
import tkinter as tk     #here
from tkinter import Label, Text, Scrollbar, scrolledtext
from PIL import Image, ImageTk              #till this
from decouple import config
from datetime import datetime
from random import choice
from convo import random_text, repeat_cmd, vtron_health, vtron_identity, vtron_thank_you_responses
from online import find_my_IP, search_on_wikipedia, search_on_google, youtube, schedule_whatsapp_msg, open_hyperlink, send_email, get_news, weather_report


engine = pyttsx3.init('sapi5')   # sapi5 is a microsoft speech api for speech recognition
engine.setProperty('volume',1.5)
engine.setProperty('rate',200)
voices = engine.getProperty('voices')        # importing voices module through variable
engine.setProperty('voice',voices[1].id)     # 0 for a male voice

USER = config('USER')
HOSTNAME = config('BOT')
# A .env file is a text file containing key value pairs of all the environment variables required by your application. This file is included with your project locally but not saved to source control so that you aren't putting potentially sensitive information at risk.


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour
    if (hour>=5) and (hour<12):
        speak(f"Good morning! {USER}")
    elif (hour>=12) and (hour<16):
        speak(f"Good afternoon! {USER}")
    elif (hour>=16) and (hour<20):
        speak(f"Good evening! {USER}")
    else:
        speak(f"Hello there! {USER}")
    speak(f"I am {HOSTNAME}, your Personal Digital Assistant. How may I assist you?") 


listening = False
listening_lock = threading.Lock()

def start_listening():
    with listening_lock:
        global listening
        listening = True
    print("Vtron is now listening...")

def pause_listening():
    with listening_lock:
        global listening
        listening = False
    print("Vtron has stopped listening.")

keyboard.add_hotkey('ctrl+alt+k',start_listening)
keyboard.add_hotkey('ctrl+alt+p',pause_listening)


def take_command():

    # Check if Vtron is listening before proceeding
    if not listening:
        return 'None'  # Return 'None' if Vtron is paused
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1    # This means the recognizer will wait for 1 second of silence before considering the input as complete.
        audio = r.listen(source)

    try:
        print("Recognizing...")
        queri = r.recognize_google(audio,language='en-in')
        print(f"{USER}'s statement : {queri}")
        if 'stop' not in queri and 'exit' not in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 or hour < 6:
                speak(f"Good night! {USER}, take care.")
                print(f"Good night! {USER}, take care.")
            else:
                speak(f"Have a great day ahead! {USER}.")
                print(f"Have a great day ahead! {USER}.")
            exit()

    except Exception:
        speak(choice(repeat_cmd))
        queri = 'None'

    return queri


# Function to generate OpenAI response
OPENAI_API_KEY = config('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
def get_openai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Or whichever engine you're using
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except openai.error.AuthenticationError as e:
        print("Authentication error:", e)
        speak("There was an issue with the API key. Please check your credentials.")
    except openai.error.RateLimitError as e:
        print("Rate limit exceeded:", e)
        speak("I have exceeded my usage limit. Please try again later.")
    except openai.error.OpenAIError as e:
        print("An error occurred:", e)
        speak("An error occurred with OpenAI. Please try again.")
    except Exception as e:
        print("An unexpected error occurred:", e)
        speak("An unexpected error occurred. Please try again.")

# Function to handle OpenAI activation and interaction
def activate_openai():
    speak("Note that, this is a free tier plan and the api might encounter errors")
    speak("OpenAI activated. How can I assist you?")
    while True:
        query = take_command().lower()
        
        if "deactivate open ai" in query:
            speak("Deactivating OpenAI. Let me know if you need anything else.")
            break
        
        # Send the user's command as the prompt to OpenAI
        openai_response = get_openai_response(query)
        
        # Speak the OpenAI response
        if openai_response:
            speak(openai_response)


# Main GUI and Vtron logic integration
def run_vtron_with_gui():
    
    # Initialize the main window
    window = tk.Tk()
    window.title("Vtron Assistant")
    
    # Load and display the image
    img = Image.open("E:\\Vtron\\ai_image.png")  # Replace with your image path
    img = img.resize((400, 300), Image.LANCZOS)  # Adjust size as needed
    img = ImageTk.PhotoImage(img)

    img_label = tk.Label(window, image=img)
    img_label.grid(row=0, column=0, padx=10, pady=10)  # Place the image on the left

    # Create a scrolled text widget for terminal/log display
    terminal_display = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=20, width=60)
    terminal_display.grid(row=0, column=1, padx=10, pady=10)  # Place the terminal on the right    


    # Create an in-memory file object to capture stdout
    log_capture = io.StringIO()

    # Redirect stdout to the in-memory file object
    sys.stdout = log_capture


    def update_terminal():
        # Get the current contents of the log_capture
        log_contents = log_capture.getvalue()
        # Update the ScrolledText widget with the captured output
        terminal_display.delete(1.0, tk.END)
        terminal_display.insert(tk.END, log_contents)
        terminal_display.yview(tk.END)  # Scroll to the end
        # Schedule the function to run again after 1000 ms (1 second)
        window.after(1000, update_terminal)

    # Start updating the terminal display
    # update_terminal()

    def vtron_thread():
        # speak("Hello there!")
        # print("Hello there!")
        greet_me()   
        while True:
            if listening:

                query = take_command().lower()

                if "how are you" in query:
                    speak(choice(vtron_health))

                elif query in vtron_identity:
                    speak("I am Vtron, a personal digital assistant developed by Saptarshi on Python.")
                    print("I am Vtron, a personal digital assistant developed by Saptarshi on Python.")

                elif "thanks" in query or "thankyou" in query or "thank" in query:
                    speak(choice(vtron_thank_you_responses))
                
                elif "time is it" in query or "what is the time" in query or "time now" in query:
                    currentHours = datetime.now().hour
                    currentMinutes = datetime.now().minute
                    if currentHours < 12:
                        speak(f"{currentHours}:{currentMinutes} AM")
                        print(f"Current time is : {currentHours}:{currentMinutes} AM")
                        
                    else:
                        twlHrsFormat = currentHours - 12 if currentHours > 12 else 12
                        speak(f"{twlHrsFormat}:{currentMinutes} PM")
                        print(f"Current time is : {currentHours}:{currentMinutes} PM")

                elif "open command prompt" in query:
                    speak("Opening command prompt.")
                    os.system('start cmd')
                
                elif "open camera" in query:
                    speak("Opening camera.")
                    sp.run('start microsoft.windows.camera:',shell=True)
                
                elif "open notepad" in query:
                    speak("Opening notepad.")
                    notepadNewFile_path = "C:\\Users\\sapfi\\AppData\\Local\\Microsoft\\WindowsApps\\notepad.exe"
                    os.startfile(notepadNewFile_path)
                
                elif "ip address" in query or "what is my ip" in query:
                    ip_address = find_my_IP()
                    speak(f"Your IP address is {ip_address}")
                    print(f"Your IP address is : {ip_address}")

                elif "open youtube" in query:
                    speak("What do you want to play on YouTube?")
                    video = take_command().lower()
                    youtube(video)
                
                elif "open google" in query:
                    speak("What do you want to google ?")
                    search = take_command().lower()
                    search_on_google(search)

                elif "open wikipedia" in query:
                    speak("What do you want to search on Wikipedia?")
                    search = take_command().lower()
                    wikiresults = search_on_wikipedia(search)
                    speak(f"According to wikipedia, {wikiresults}")
                    speak("I am printing it on terminal.")
                    print(wikiresults)

                elif "schedule whatsapp message" in query:
                    speak("Please enter the receiver's number starting with +")
                    receiver_number = take_command()
                    speak("Now, please enter your message")
                    message_to_receiver = take_command().lower()
                    speak("Please enter schedule hour in 24 hours format")
                    schedule_hour = take_command()
                    speak("Please enter the minute of the scheduled hour")
                    schedule_minute = take_command()

                    if not receiver_number.startswith("+"):
                        raise ValueError("Phone number must include the country code, e.g., +1234567890")
                    
                    try:
                        whatsapp_send = schedule_whatsapp_msg(receiver_number, message_to_receiver, schedule_hour, schedule_minute)
                        print(f"Message scheduled to {receiver_number} at {schedule_hour}:{schedule_minute}")

                    except Exception as e:
                        print(f"An error occurred: {e}")

                elif "induction class" in query:
                    speak("Redirecting you to VIT live induction Bridge classes on YouTube LIVE")
                    url = "https://www.youtube.com/@FreshersInduction2024"
                    open_hyperlink(url)

                elif "vtop" in query or "v-top" in query:
                    speak("Redirecting you to the VTOP landing page")
                    url = "https://vtop.vitap.ac.in/vtop/open/page"
                    open_hyperlink(url)
                
                elif "linkedin" in query:
                    speak("Redirecting to your LinkedIn profile")
                    url = "https://www.linkedin.com/in/saptarshi-bose-a09436313/"
                    open_hyperlink(url)
                
                elif "github" in query:
                    speak("Redirecting to your GitHub profile")
                    url = "https://github.com/Sapfire007"
                    open_hyperlink(url)
                
                elif "whatsapp web" in query:
                    speak("Redirecting you to WhatsApp Web")
                    url = "https://web.whatsapp.com/"
                    open_hyperlink(url)
                
                elif "spotify" in query:
                    speak("Redirecting you to Spotify")
                    url = "https://open.spotify.com/"
                    open_hyperlink(url)

                elif "send an email" in query:
                    speak("Please enter the receiver's email address")
                    receiver_add = take_command().capitalize()
                    speak("What should be the subject of your email ?")
                    # subject = input("Enter your email's subject : ")
                    subject = take_command().capitalize()
                    print("Your email subject : ",subject)
                    speak("What should be the message of your email ?")
                    message = take_command().capitalize()
                    print("Your email message : ",message)
                    if send_email(receiver_add,subject,message):
                        speak(f"{USER}, your email has been sent.")
                        print(f"{HOSTNAME} says : {USER}, your email has been sent.")
                    else:
                        speak("Something went wrong, please check the error log.")

                elif "news" in query:
                    speak(f"I am reading out today's latest news headlines")
                    speak(get_news())
                    speak("I am printing the news said, on the screen")
                    print("==============================================================")
                    print(*get_news(), sep='\n')
                    print("==============================================================")

                elif "weather" in query:
                    speak("Please tell the name of the city whose weather forecast is to be shown")
                    city_name = take_command().capitalize()
                    speak(f"Getting latest weather updates for {city_name}")
                    weather, temp, feels_Like = weather_report(city_name)
                    speak(f"The current temperature at {city_name} is : {temp}, but it feels like {feels_Like}")
                    speak(f"Also the weather report talks about {weather}")
                    speak(f"Im printing the above mentioned weather report on the screen")
                    print(f"Description : {weather} \nTemperature : {temp} \nFeels like : {feels_Like}")

                
                elif "movie" in query:
                    movies_db = imdb.IMDb()
                    speak("Please tell me the movie name")
                    movieInput = take_command()
                    movies = movies_db.search_movie(movieInput)
                    speak(f"Searching for {movieInput}")
                    speak("I found these")
                    for movie in movies:
                        title = movie["title"]
                        year = movie["year"]
                        speak(f"{title}-{year}")
                        info = movie.getID()
                        movie_info = movies_db.get_movie(info)
                        rating = movie_info["rating"]
                        cast = movie_info["cast"]
                        actor = cast[0:6]
                        plot = movie_info.get('plot outline','plot summary not available')
                        speak(f"{title} was released in {year} has imdb rating of {rating} . It has a cast of {actor}. The plot summary of the movie is {plot}.")
                        print(f"Vtron says : \"{title}\" was released in {year} has imdb rating of : {rating}. \nIt has a cast of : {actor}. \nThe plot summary of the movie is : {plot}.")
                        break      # used break statement here cuz to execute the top search result rather than all the input matches

                elif "calculate" in query:
                    WOLFRAM_ALPHA_APP_ID = config('WOLFRAM_ALPHA_APP_ID')
                    client = wolframalpha.Client(WOLFRAM_ALPHA_APP_ID)
                    ind = query.lower().split().index("calculate")
                    text = query.split()[ind + 1:]
                    result = client.query(" ".join(text))

                    try:
                        result = client.query(" ".join(text))
                        ans = next(result.results).text            # essentially gets the first textual answer from the response.
                        speak(f"The answer is {ans}")
                        print(f"Vtron says :  The answer is : {ans}")

                    except StopIteration:                        # In this case, if Wolfram Alpha doesn’t return any results, the StopIteration exception tells the program that no more answers are available, and you handle that by informing the user.
                        speak("I couldn't find that, please try again.")

                    except Exception as e:
                        speak("An unexpected error occurred while calculating. Please try again.")
                        print(f"Error: {e}")
                
                elif "what is" in query or "who is" in query or "who was" in query or "which is" in query:
                    WOLFRAM_ALPHA_APP_ID = config('WOLFRAM_ALPHA_APP_ID')
                    client = wolframalpha.Client(WOLFRAM_ALPHA_APP_ID)

                    try:
                        ind = query.lower().index("what is") if "what is" in query.lower() else \
                        query.lower().index("who is") if "who is" in query.lower() else \
                        query.lower().index("who was") if "who was" in query.lower() else \
                        query.lower().index("which is") if "which is" in query.lower() else None

                        if ind is not None:
                            text = query.split()[ind + 2:]
                            result = client.query(" ".join(text))
                            ans = next(result.results).text            # essentially gets the first textual answer from the response.
                            speak(f"The answer is {ans}")
                            print(f"Vtron says :  The answer is : {ans}")

                        else:
                            speak("I could not find that")

                    except StopIteration:                        # In this case, if Wolfram Alpha doesn’t return any results, the StopIteration exception tells the program that no more answers are available, and you handle that by informing the user.
                        speak("I couldn't find that, please try again.")

                    except Exception as e:
                        speak("An unexpected error occurred while fetching the answer, try googling your query or please try again later.")
                        print("Error: An unexpected error occurred while fetching the answer, try googling your query or please try again later.")

                elif "activate open ai" in query or "start open ai" in query:
                    activate_openai()

            else:
                continue


    update_terminal()
    # Start the Vtron assistant thread
    threading.Thread(target=vtron_thread, daemon=True).start()

    window.mainloop()

if __name__ == '__main__':
    run_vtron_with_gui()