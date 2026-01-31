import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import datetime
from googletrans import Translator

# Initialize the recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()

# --- Voice Setup ---
voices = engine.getProperty('voices')
hindi_voice_id = None
english_voice_id = None

# Attempt to find Hindi and English voices
for voice in voices:
    if "hindi" in voice.name.lower() or "india" in voice.name.lower():
        hindi_voice_id = voice.id
    if "english" in voice.name.lower() and "us" in voice.name.lower():
        english_voice_id = voice.id
    
if not english_voice_id and voices:
    english_voice_id = voices[0].id

# Set default to English
engine.setProperty('voice', english_voice_id)
# Adjust speaking rate
engine.setProperty('rate', 170)

def talk(text):
    """
    Speaks the text in English.
    Tries to translate to Hindi and speak that too if a Hindi voice is found.
    """
    # 1. Speak English
    print(f"Jaddu (EN): {text}")
    engine.setProperty('voice', english_voice_id)
    engine.say(text)
    
    # 2. Try Hindi
    try:
        translated = translator.translate(text, dest='hi').text
        print(f"Jaddu (HI): {translated}")
        
        if hindi_voice_id:
            engine.setProperty('voice', hindi_voice_id)
            engine.say(translated)
            # Switch back to English for next time just in case
            engine.setProperty('voice', english_voice_id) 
    except Exception as e:
        print(f"Translation/Voice Error: {e}")

    engine.runAndWait()

def take_command():
    """
    Listens to the microphone and returns the text command.
    """
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening for 'Jaddu'...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            
    except sr.UnknownValueError:
        pass # Don't print anything if nothing recognized to avoid clutter
    except sr.RequestError:
        print("Network error.")
    except Exception as e:
        print(f"Error: {e}")

    return command

def run_jaddu():
    """
    Main execution logic
    """
    command = take_command()
    
    # WAKE WORD LOGIC
    if 'jaddu' in command:
        # Remove the wake word to get the actual instruction
        command = command.replace('jaddu', '').strip()
        print(f"User said: {command}")
        
        if not command:
            talk("Yes boss, I am listening.")
            return

        if 'play' in command:
            song = command.replace('play', '').strip()
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)
            
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The current time is {current_time}")
            
        elif 'who is' in command:
            person = command.replace('who is', '').strip()
            try:
                info = wikipedia.summary(person, 1)
                talk(info)
            except:
                talk("I couldn't find information on that.")
                
        elif 'joke' in command:
            talk(pyjokes.get_joke())
            
        elif 'are you single' in command:
            talk("I am in a committed relationship with my power source.")
            
        elif 'stop' in command:
            talk("Goodbye!")
            exit()
            
        else:
            talk("I heard you, but I'm not sure what to do with that command yet.")

if __name__ == "__main__":
    talk("Jaddu is starting up...")
    while True:
        try:
            run_jaddu()
        except KeyboardInterrupt:
            break
        except Exception as e:
            # Prevent crashing on main loop
            print(f"Critical Error: {e}")
