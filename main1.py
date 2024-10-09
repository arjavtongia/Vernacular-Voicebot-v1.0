import streamlit as st
import io
import time
import csv
import os
import pandas as pd
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator

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

def translate_text(text, src_lang='en', dest_lang='hi'):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
    return translated_text

def main():
    st.markdown(
        "<h1 style='text-align: center; color: #ff6600; font-size: 48px; font-weight: bold;'>🤖Vernacular Voicebot🔊</h1>",
        unsafe_allow_html=True)

    language = st.selectbox("Select language / भाषा चुने", options=["English", "हिंदी"])
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

    start_button = st.button("Talk")
    search_button = st.button("Search")

    if start_button:
        st.write("Please speak your answers.")
        responses = []

        for i, question in enumerate(questions[lang_code]):
            if lang_code == 'en':
                st.markdown(f" **Question - {i+1} : [English] :**")
            elif lang_code == 'hi':
                st.markdown(f" **प्रश्न - {i+1} : [हिंदी] :**")

            st.markdown(f"### **{question}**")
            st.audio(text_to_speech(question, lang=lang_code).read(), format="audio/wav")

            countdown_placeholder = st.empty()

            for number in range(3, 0, -1):
                countdown_placeholder.markdown(f"<h2 style='color: blue;'>{number}</h2>", unsafe_allow_html=True)
                time.sleep(1)

            countdown_placeholder.write(f"<h2 style='color: blue;'>🔊</h2>", unsafe_allow_html=True)
            answer = speech_to_text(lang=lang_code)
            st.write(f"Your answer: {answer}")
            responses.append(answer)

        translator = Translator()
        responses_en = [translator.translate(response, src='hi', dest='en').text for response in responses]

        filename = "user_responses.csv"
        if not os.path.exists(filename):
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(questions['en'])

        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(responses_en)

        st.write("Your answers:")
        if lang_code == 'en':
            for i, response in enumerate(responses):
                st.write(f"Answer ({i+1}) [English]: {response}")
        elif lang_code == 'hi':
            translated_responses = [translate_text(response, src_lang='en', dest_lang='hi') for response in responses]
            for i, response in enumerate(translated_responses):
                st.write(f"Answer ({i+1}) [Hindi]: {response}")

        if search_button:


            id_number = st.text_input("Enter your ID number:")
            if id_number:
              df = pd.read_csv(filename)
              matched_records = df[df['What is your ID?'] == id_number]
            if not matched_records.empty:
              st.write("Matched Records:")
              st.write(matched_records)
            else:
              st.write("No records found for the given ID.")





if __name__ == "__main__":
    main()
