import streamlit as st
import streamlit_webrtc as webrtc
from gtts import gTTS
import speech_recognition as sr
import pandas as pd
import time
import io
from googletrans import Translator
import csv
import os

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    return audio_data

def speech_to_text(lang='en'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        st.write("Listening...")
        audio = recognizer.listen(source, timeout=5)
        try:
            if lang == 'en':
                text = recognizer.recognize_google(audio)
            elif lang == 'hi':
                text = recognizer.recognize_google(audio, language='hi-IN')
                translator = Translator()
                text = translator.translate(text, src='hi', dest='en').text
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Error fetching results from Google Speech Recognition service: {e}")

def main():
    st.markdown(
    "<h1 style='text-align: center; color: #ff6600; font-size: 48px; font-weight: bold;'>"
    "🤖Vernacular Voicebot🔊</h1>",
    unsafe_allow_html=True)
    language = st.selectbox("Select language / भाषा चुने", options=["English", "हिंदी"])
    # Convert language selection to language code
    lang_code = 'en' if language == "English" else 'hi'
    questions = {
        "en": [
            "What is your ID?",
            "What is your name?",
            "What is your address?",
            "What is your city?",
            "What is your state?"
        ],
        "hi": [
            "आपका आईडी क्या है?",
            "आपका नाम क्या है?",
            "आपका पता क्या है?",
            "आपका शहर क्या है?",
            "आपका राज्य क्या है?"
        ]
    }
    start_button = st.button("Start")
    if start_button:
        st.write("Please speak your answers.")
        responses = []
        for i, question in enumerate(questions[lang_code]):
            st.write(f"Question ({i+1}): {question}")
            st.audio(text_to_speech(question, lang=lang_code).read(), format="audio/wav")
            st.write("3...")
            time.sleep(1)
            st.write("2...")
            time.sleep(1)
            st.write("1...")
            time.sleep(1)
            answer = speech_to_text(lang=lang_code)
            st.write(f"Your answer: {answer}")
            responses.append(answer)
        # Translate Hindi responses to English for storing in the CSV file
        translator = Translator()
        responses_en = [translator.translate(response, src='hi', dest='en').text for response in responses]
        # Save responses to CSV file
        filename = "user_responses.csv"
        if not os.path.exists(filename):
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(questions['en'])  # Writing column headers
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(responses_en)

if __name__ == "__main__":
    main()
