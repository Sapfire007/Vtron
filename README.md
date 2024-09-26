# Vtron Personal Digital Assistant

Vtron is a Python-based personal digital assistant that integrates various functionalities including voice recognition, text-to-speech, web searches, and more. It provides a GUI interface and can perform tasks such as sending emails, fetching news, and providing weather updates.

## Features

- **Voice Recognition**: Uses speech recognition to understand and execute voice commands.
- **Text-to-Speech**: Converts text responses to speech using the `pyttsx3` library.
- **OpenAI Integration**: Interacts with OpenAI's API to provide responses based on user queries.
- **Web Functionalities**: Includes capabilities to search Wikipedia, Google, play YouTube videos, and more.
- **GUI Interface**: A Tkinter-based GUI with an image and terminal display.
- **And many more...!**


# Author
- **Saptarshi Bose**


## Installation

### Prerequisites

Ensure you have Python 3.8 or higher installed. You can download Python from [python.org](https://www.python.org/downloads/).

### Setting Up the Virtual Environment

1. **Create a Virtual Environment :**
   ```sh
   E:\Vtron\v\Scripts\python.exe -m venv vtron-env
   ```

2. **Activate the Virtual Environment :**
   - **On Windows :**
     ```sh
     vtron-env\Scripts\activate
     ```

   - **On macOS/Linux :**
     ```sh
     source vtron-env/bin/activate
     ```


### Installing Dependencies

1. **Clone the Repository :**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Required Packages :**
   ```sh
   # Vtron Project Packages
   
   1. requests - For making HTTP requests to external APIs.
   2. wikipedia - To fetch information from Wikipedia.
   3. pywhatkit - For interacting with WhatsApp, YouTube, and Google searches.
   4. webbrowser - To open URLs in the default web browser.
   5. email.message (EmailMessage) - For creating email messages.
   6. smtplib - For sending emails via the SMTP protocol.
   7. decouple - For managing environment variables from a `.env` file.
   8. speech_recognition - For converting spoken words into text.
   9. pyttsx3 - For text-to-speech conversion.
   10. keyboard - For detecting keyboard hotkeys.
   11. os - For interacting with the operating system.
   12. tkinter - For building the graphical user interface (GUI).
   13. threading - For handling concurrent tasks.
   14. time - For managing time-related tasks.
   15. datetime - For date and time manipulation.
   16. pyjokes - For generating random jokes.

   ```


### Environment Variables

   Create a `.env` file in the root directory of your project with the following variables:
   
   ```makefile
   USER=YourUsername
   BOT=Vtron
   OPENAI_API_KEY=your_openai_api_key
   WOLFRAM_ALPHA_APP_ID=your_wolfram_alpha_app_id
   EMAIL=your_email@example.com
   PASSWORD=your_email_password
   NEWSAPI_KEY=your_newsapi_key
   OPENWEATHER_API_KEY=your_openweather_api_key
   ```


### Usage

1. **Run the Application :**
   
   ```sh
   python main.py
   ```

2. **Voice Commands :**
   - **Activate Listening**: Press Ctrl+Alt+K
   - **Pause Listening**: Press Ctrl+Alt+P
   - **Start OpenAI**: Say "activate open ai" or "start open ai"
   - **Stop OpenAI**: Say "deactivate open ai"


## Project Structure

- **main.py**: Contains the main application logic and GUI setup.
- **online.py**: Contains functions for online interactions (e.g., web searches, sending emails).
- **convo.py**: Contains response data and random text used in interactions.

## Troubleshooting

- **Voice Inputs Not Working**: Ensure your microphone is correctly set up and permissions are granted.
- **API Errors**: Check your API keys and ensure they are correctly set in the .env file.


## Additional Information

### GUI Layout
- **Image Display**: The right half of the Tkinter GUI displays a GIF or picture of AI.
- **Terminal**: The left half of the Tkinter GUI acts as a chat terminal.

### Voice Command Handling
- Commands for starting and stopping OpenAI interactions are implemented in the `process_input()` function.

### Development Notes
- Ensure `window` is used instead of `root` for Tkinter window naming.
- The `test_chat` function and test button have been removed from the Tkinter GUI as per the project requirements.
- The `listening = False` state is used initially, with functions `start_listening()` and `pause_listening()` triggered by keyboard hotkeys (Ctrl+Alt+K to start listening, and Ctrl+Alt+P to pause listening).
- The Vtron thread logic is kept inside its own function and not mixed with specific command handling logic.
<hr>
