from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import speech_recognition as sr
import time
import pyttsx3

CHROMEDRIVER_PATH = 'C:\\Users\\riyesh\\OneDrive\\Desktop\\gaze_controlled_keyboard_p10\\chromedriver.exe'
WELCOME_MESSAGE = "Hello! I'm your personal assistant. How can I help you?"
UNKNOWN_COMMAND_MESSAGE = "Sorry, I didn't understand that. Please try again."
ERROR_MESSAGE = "Sorry, I couldn't understand your speech. Please try again."
GOODBYE_MESSAGE = "Goodbye! Have a great day."



brave_path = 'C:\\Users\\riyesh\\OneDrive\\Desktop\\gaze_controlled_keyboard_p10\\chromedriver.exe' # replace with the actual path to the driver executable
options = webdriver.ChromeOptions()
options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe' # replace with the actual path to the Brave browser binary file
driver = webdriver.Chrome(executable_path=brave_path, options=options)

engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def speak(query):
    engine.say(query)
    engine.runAndWait()

def recognize_speech():
    with microphone as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
    
    try:
        response = recognizer.recognize_google(audio)
        return response.lower()
    except:
        return None

speak(WELCOME_MESSAGE)
while True:
    voice = recognize_speech()
    if voice is None:
        
        continue
    print(voice)
    if 'open google' in voice:
        speak('Opening google..')
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('https://google.com')
    
        speak('What do you want to search?')
        query = recognize_speech()
        if query is None:
            
            continue
        driver.get('https://google.com')
        element = driver.find_element("xpath","//input[@title='Search']")
        
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
    elif 'open youtube' in voice:
        speak('Opening youtube..')
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('https://youtube.com')
    
        speak('What do you want to search?')
        query = recognize_speech()
        if query is None:
           
            continue
        element = driver.find_element("xpath","//input[@title='Search']")
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
    elif 'switch tab' in voice:
        num_tabs = len(driver.window_handles)
        cur_tab = driver.window_handles.index(driver.current_window_handle)
        next_tab = (cur_tab + 1) % num_tabs
        driver.switch_to.window(driver.window_handles[next_tab])
    elif 'close tab' in voice:
        speak('Closing Tab..')
        driver.close()
    elif 'go back' in voice:
        driver.back()
    elif 'go forward' in voice:
        driver.forward()
    elif 'exit' in voice:
        speak(GOODBYE_MESSAGE)
        driver.quit()
        break
    else:
        speak(UNKNOWN_COMMAND_MESSAGE)
  
