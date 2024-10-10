from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from googletrans import Translator
import speech_recognition as sr
import threading
import pyttsx3
from gtts import gTTS
import pygame
from langdetect import detect
import os
import time
translator = Translator()

# ---------------------------------------------------------------------------
# Declaration
language_map = {
    'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 
    'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 
    'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 
    'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 
    'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 
    'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 
    'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 
    'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 
    'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 
    'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 
    'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 
    'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 
    'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 
    'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 
    'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 
    'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 
    'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 
    'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu'
}

languages = ['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 
             'azerbaijani', 'basque', 'belarusian', 'bengali', 'bosnian',
             'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)',
             'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 
             'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 'frisian', 
             'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 
             'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic',
             'igbo', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 
             'kazakh', 'khmer', 'korean', 'kurdish (kurmanji)', 'kyrgyz', 'lao', 'latin', 
             'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay',
             'malayalam', 'maltese', 'maori', 'marathi', 'mongolian', 'myanmar (burmese)', 
             'nepali', 'norwegian', 'odia', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 
             'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian', 'sesotho', 'shona', 'sindhi',
             'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik',
             'tamil', 'telugu', 'thai', 'turkish', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh',
             'xhosa', 'yiddish', 'yoruba', 'zulu']

# Reverse the dictionary to map full language names to short codes
language_map_reversed = {v: k for k, v in language_map.items()}

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.stop_listening = threading.Event()
        self.create_widgets()
        self.engine = pyttsx3.init()
         # Initialize pygame mixer for playing audio
        pygame.mixer.init()
    
    def create_widgets(self):
        self.root.title("Translator")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        button_width = int(screen_width * 0.1)
        button_height = int(screen_height * 0.05)

        self.root.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")

        #  Recognization Button Image
        self.recognize_button_image = Image.open("./Assets/mic.png")
        self.recognize_button_image = self.recognize_button_image.resize((20, 20))
        self.recognize_button_photo = ImageTk.PhotoImage(self.recognize_button_image)

       #  Wave Button Image
        self.wave_image = Image.open("./Assets/wave.png")
        self.wave_image = self.wave_image.resize((40, 40))
        self.wave = ImageTk.PhotoImage(self.wave_image)

        topframe = Frame(self.root, bd=2, height=50, bg="#1f2326")
        topframe.pack(side=TOP, fill=X)

        label = Label(topframe, text="Translator", font=("Arial", 20), bg="#1f2326", fg="#fff")
        label.pack(pady=10)

        inputData = Frame(self.root, bd=2, bg="#1f2326")
        inputData.pack(side=TOP, fill=BOTH, expand=True)

        self.input_area = Text(inputData, height=11, width=40)
        self.input_area.pack(side=TOP, padx=10, pady=10, fill=BOTH, expand=True)

        self.language_var = StringVar()
        self.language_var.set("Select Language")  # default value

        buttonFrame = Frame(inputData, bd=2, bg="#1f2326")
        buttonFrame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        # Create the language selection combobox
        language_combobox = ttk.Combobox(buttonFrame, textvariable=self.language_var, font=("Arial", 10))
        language_combobox['values'] = languages
        language_combobox.pack(side=LEFT, padx=10, pady=10, expand=True)

        recognize_button = Button(buttonFrame, image=self.recognize_button_photo, bg='#1f2326')
        recognize_button.pack(side=LEFT)
        recognize_button.bind('<ButtonPress>', self.start_recognizing)
        recognize_button.bind('<ButtonRelease>', self.stop_recognizing)

        translate_button = Button(buttonFrame, text="Translate", command=self.translate_text, fg="#fff", bg="#2862c7", font=("Arial", 13))
        translate_button.pack(side=RIGHT, padx=10, pady=10)

        outputFrame = Frame(self.root, bd=2, bg="#1f2326")
        outputFrame.pack(side=TOP, fill=BOTH, expand=True)

        forLabel = Frame(outputFrame, bg="#1f2326")
        forLabel.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        Label(forLabel, text="Translated data", bg="#1f2326", fg="#fff", font=("Arial", 15)).pack(side=LEFT)
        # waveButton = Label(forLabel, image=self.wave, bg="#1f2326")
        # waveButton.pack(side=RIGHT)
        waveButton = Button(forLabel, image=self.wave, bg='#1f2326', command=self.speakTranslatedData)
        waveButton.pack(side=RIGHT)
        

        self.output_area = Text(outputFrame, height=9, width=40)
        self.output_area.pack(padx=10, pady=10, fill=BOTH, expand=True)
        self.output_area.config(state='disabled')  # make it non-editable

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        

    def recognize_voice(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while not self.stop_listening.is_set():
                print("Listening...")
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    text = recognizer.recognize_google(audio)
                    self.update_text_area(text)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand your audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                except sr.WaitTimeoutError:
                    pass

    def start_recognizing(self, event):
        self.stop_listening.clear()
        threading.Thread(target=self.recognize_voice).start()

    def stop_recognizing(self, event):
        self.stop_listening.set()

    def update_text_area(self, text):
        self.input_area.insert(END, text + " ")
        self.input_area.see(END)

    def on_closing(self):
        self.stop_listening.set()
        self.root.destroy()

    def translate_text(self):
        
        file_path = "./Assets/translated_text.mp3"

        if os.path.exists(file_path):
          os.remove(file_path)
          print("File removed successfully.")
        else:
            print("File is in use, waiting...")
            time.sleep(2)

        print("Function Called")
        input_text = self.input_area.get("1.0", END).strip()
        selected_language = self.language_var.get()
        if selected_language == "Select Language":
            selected_language = "english"
        
        target_language = language_map_reversed.get(selected_language, "en")
        
        # Translate the text
        translated = translator.translate(input_text, dest=target_language)
        print(translated.text)
        self.output_area.config(state=NORMAL)
        self.output_area.delete("1.0", END)
        self.output_area.insert("1.0", translated.text)
        self.output_area.config(state=DISABLED)
        
    def speakTranslatedData(self):
        translated_text = self.output_area.get("1.0", END)
        detected_lang = detect(translated_text)
        save_path = "./Assets/translated_text.mp3"

        try:
            tts = gTTS(text=translated_text, lang=detected_lang)
            tts.save(save_path)
            print(f"MP3 file saved successfully: {save_path}")

            pygame.mixer.init()
            pygame.mixer.music.load(save_path)
            pygame.mixer.music.play()

            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Attempt to delete the MP3 file with retry mechanism
            retry_count = 5  # Number of times to retry
            wait_time = 2    # Seconds to wait between retries

            pygame.mixer.quit()
            for _ in range(retry_count):
                try:
                    os.remove(save_path)
                    print(f"MP3 file deleted successfully: {save_path}")
                    break
                except PermissionError:
                    print("File is in use, waiting...")
                    time.sleep(wait_time)
            else:
                print("Failed to delete the file after several retries.")
                
            pygame.mixer.quit()

        except Exception as e:
            print(f"Error: {e}")


         
   

if __name__ == "__main__":
    root = Tk()
    app = TranslatorApp(root)
    root.mainloop()
