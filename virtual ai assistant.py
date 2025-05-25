import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import socket
import random
import subprocess
import platform
import ctypes

# Initialize speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use voices[0] for male voice

def remove_emojis(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def talk(text):
    print("Friday:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"Recognized command: {command}")
    except Exception as e:
        print("Could not understand audio:", e)
        exit
    return command

def run_friday():
    command = take_command()
    if not command:
        talk("I didn't hear anything. Please try again.")
        return

    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
        
    elif 'date' in command:
        today = datetime.datetime.now().strftime('%A, %B %d, %Y')
        talk(f"Today's date is {today}")

    elif 'hello' in command:
        talk('Hello sir, how can I help you?')

    elif 'what is your name' in command:
        talk('I am your virtual assistant, Friday.')

    elif 'what is my name' in command:
        talk('Your name is Rounak Kumar Mishra.')

    elif 'how are you' in command:
        talk('I am fine, what about you?')

    elif 'i am also fine' in command:
        talk('Okay, good.')

    elif 'tell me something about my project' in command:
        talk('You have made a virtual assistant in your Prayogam project exhibition. It responds to voice commands. '
             'The team leader is Rounak Kumar Mishra')

    elif 'search for' in command:
        topic = command.replace('search for', '').strip()
        talk(f"Searching for {topic}")
        try:
            summary = wikipedia.summary(topic, sentences=2)
            talk(summary)
        except:
            talk("Sorry, I couldn't find anything.")
            
    elif 'system information' in command:
        system = platform.system()
        version = platform.version()
        processor = platform.processor()
        talk(f"This system is running {system}, version {version}, with a {processor} processor.")
    
    elif 'open' in command:
        site = command.replace('open', '').strip()
        talk(f'Searching for {site}')
        pywhatkit.search(site)
        
    elif 'calculate bmi' in command:
        try:
            talk("Please tell me your weight in kilograms.")
            weight = float(take_command())
            talk("Please tell me your height in meters.")
            height = float(take_command())
            bmi = weight / (height ** 2)
            talk(f"Your BMI is {bmi:.2f}")
        except Exception as e:
            talk("Sorry, I couldn't calculate BMI.")
            print("BMI error:", e)
            
    elif 'calculator' in command:
        talk("Opening calculator.")
        subprocess.Popen('calc.exe')
    
    elif 'notepad' in command:
        talk("Opening notepad.")
        subprocess.Popen('notepad.exe')
        
    elif 'my ip' in command:
        ip = socket.gethostbyname(socket.gethostname())
        talk(f"Your IP address is {ip}")
    
    elif 'run' in command:
        pywhatkit.search("www.chatgpt.openai.com")
        
    elif 'toss a coin' in command:
        result = random.choice(['Heads', 'Tails'])
        talk(f"The coin landed on {result}")
        
    elif 'roll a dice' in command:
        result = random.randint(1, 6)
        talk(f"You rolled a {result}")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
        
    elif 'where am i' in command or 'my location' in command:
        try:
            res = requests.get('https://ipinfo.io/json')
            data = res.json()
            city = data.get('city', '')
            region = data.get('region', '')
            country = data.get('country', '')
            talk(f"You are in {city}, {region}, {country}")
        except Exception as e:
            talk("Sorry, I couldn't get your location.")
            print("Location error:", e)
            
    elif 'remember that' in command:
        talk("What should I remember?")
        data = take_command()
        with open("memory.txt", "w") as file:
            file.write(data)
            talk("I will remember that.")
            
    elif 'what do you remember' in command:
        try:
            with open("memory.txt", "r") as file:
                memory = file.read()
                talk("You asked me to remember: " + memory)
        except FileNotFoundError:
            talk("I don't have anything in memory.")

    elif 'directions to' in command:
        destination = command.replace('directions to', '').strip()
        talk(f"Showing directions to {destination}")
        pywhatkit.search(f"directions to {destination} in Google Maps")
        
    elif 'lock screen' in command:
        talk("Locking the screen now.")
        ctypes.windll.user32.LockWorkStation()

    elif 'stop' in command or 'exit' in command or 'bye' in command:
        talk('Okay, shutting down. Goodbye!')
        exit()

    else:
        talk('Please say the command again.')

while True:
    run_friday()
