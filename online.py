import requests
import wikipedia
import pywhatkit as kit     # This module will be used to access our online functions like Google and YouTube and it has many pre-defined libraries in it.
import webbrowser
from email.message import EmailMessage
import smtplib                           # The smtplib module defines an SMTP client session object that can be used to send mail to any internet machine with an SMTP or ESMTP listener daemon. (smtp - send mail transfer protocol)
from decouple import config


EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')


NEWSAPI_KEY = config('NEWSAPI_KEY')
OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY')


def find_my_IP():
    ipaddress = requests.get('https://api.ipify.org?format=json').json()
    return ipaddress["ip"]


def search_on_wikipedia(query):
    wikiresults = wikipedia.summary(query,sentences=2)
    return wikiresults


def search_on_google(query):
    kit.search(query)


def youtube(video):
    kit.playonyt(video)


def schedule_whatsapp_msg(number,message,hrs,mins):
    kit.sendwhatmsg(number,message,hrs,mins)             # Uses Whatsapp Web in the default browser


def open_hyperlink(url):
    webbrowser.open(url)  # Opens the given URL in the default browser


def send_email(receivers_address,subject,message):
    try:
        email = EmailMessage()
        email['To'] = receivers_address
        email['Subject'] = subject
        email['From'] = EMAIL
        
        email.set_content(message)

        s = smtplib.SMTP("smtp.gmail.com",587)          # Port 587 was established as a modern secure SMTP port for message delivery. It supports TLS natively and STARTTLS as well, allowing for the secure submission of mail over SMTP.
        s.starttls()                            # The .starttls() method tells the email server that an email client, like Gmail or Outlook, wants to upgrade the current insecure connection to a secure, encrypted one using TLS. This ensures that the rest of the communication between the client and the server is safe and protected.
        s.login(EMAIL,PASSWORD)
        s.send_message(email)
        s.close()

        return True
    
    except Exception as e:
        print(e)
        return False
    

def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey"
                          f"={NEWSAPI_KEY}").json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]


def weather_report(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}"
    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        # Parse the JSON response
        result = response.json()
        
        # Print the full response for debugging
        # print(f"API Full Response: {result}")
        
        # Extract weather details safely
        weather = result.get("weather", [{}])[0].get("main", "No weather info")
        temp = result.get("main", {}).get("temp", 0)
        feels_like = result.get("main", {}).get("feels_like", 0)
        
        # Convert temperatures from Kelvin to Celsius
        temp_celsius = round(temp - 273.15, 2)
        feels_like_celsius = round(feels_like - 273.15, 2)
        
        return weather, f"{temp_celsius}°C", f"{feels_like_celsius}°C"
    
    except requests.exceptions.RequestException as e:
        # Handle network or HTTP errors
        print(f"An error occurred: Couldn't fetch data / {e}")
        return f"{None}, Couldn't fetch data", "Error", "Error"