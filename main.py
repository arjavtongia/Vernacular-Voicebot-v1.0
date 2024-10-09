
#this is final code
import base64
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
        st.write("Listening..." if lang == 'en' else "मैं सुन रहा हूँ...")
        audio = recognizer.listen(source, timeout=5)
        try:
            if lang == 'en':
                text = recognizer.recognize_google(audio)
            elif lang == 'hi':
                text = recognizer.recognize_google(audio, language='hi-IN')
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Error fetching results from Google Speech Recognition service: {e}")
def display_and_speak_message(message, lang_code):
    """
    Display and speak the provided message according to the selected language.
    Args:
        message (str): The message to be displayed and spoken.
        lang_code (str): The language code ('en' for English, 'hi' for Hindi).
    """
    st.write(message)
    audio_message = text_to_speech(message, lang=lang_code)
    with open("message_audio.mp3", "wb") as f:
        f.write(audio_message.getbuffer())
    autoplay_audio("message_audio.mp3", delay=len(message) * 0.1)  # Adding a buffer delay
    time.sleep(len(message) * 0.1)  # Additional delay for processing

def translate_text(text, src_lang='en', dest_lang='hi'):
    translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang).text
    return translated_text
def autoplay_audio(file_path: str, delay=0):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )
        time.sleep(delay)
# def write_to_csv(user_responses):
#     filename = "user_responses.csv"
#     file_exists = os.path.exists(filename)
#     with open(filename, mode="a", newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)
#         if not file_exists:
#             writer.writerow(["ID", "Name", "Address", "City", "State"])  # Writing header row if file is empty
#         if lang_code == 'hi':
#             user_responses = [translate_text(response, src_lang='hi', dest_lang='en') for response in user_responses]
#         writer.writerow(user_responses)
def main():
    st.markdown(
        "<h1 style='text-align: center; color: #ff6600; font-size: 48px; font-weight: bold;'>🤖Vernacular Voicebot🔊</h1>",
        unsafe_allow_html=True)
    language = st.selectbox("Select language / भाषा चुने", options=["English", "हिंदी"])
    lang_code = 'en' if language == "English" else 'hi'
    start_button_label = "New User" if lang_code == 'en' else "नए उपयोगकर्ता"
    speak_answers_msg = "Please speak your answers." if lang_code == 'en' else "कृपया अपने उत्तर बोलें।"
    listening_msg = "Listening..." if lang_code == 'en' else "सुन रहा है..."
    details = {
        "en": [
            "What is your ID?",
            "Name",
            "Address",
            "City",
            "State"
        ],
        "hi": [
            "आईडी",
            "नाम",
            "पता",
            "शहर",
            "राज्य"
        ]
    }
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
    start_button = st.button(start_button_label)
    if start_button:
        user_responses = []
        i = 0
        while i < len(questions[lang_code]):
            st.write(speak_answers_msg)
            # Create audio file for the question
            question_audio = text_to_speech(questions[lang_code][i], lang=lang_code)
            with open("question_audio.mp3", "wb") as f:
                f.write(question_audio.getbuffer())
            # Play audio of the question
            autoplay_audio("question_audio.mp3", delay=2)  # Wait for 2 seconds before playing the next audio
            countdown_placeholder = st.empty()
            for number in range(3, 0, -1):
                countdown_placeholder.markdown(f"<h2 style='color: blue;'>{number}</h2>", unsafe_allow_html=True)
                time.sleep(1)
            countdown_placeholder.write(f"<h2 style='color: blue;'>🔊</h2>", unsafe_allow_html=True)
            answer = speech_to_text(lang=lang_code)
            #st.write(f"Your answer: {answer}")
            your_ans = f"You Said: {answer}" if lang_code == 'en' else f"आपने कहा: {answer}"
            display_and_speak_message(your_ans, lang_code)
            user_responses.append(answer)
            i += 1
        # Print and speak details
        st.write("<div style='background-color:#e6f7ff; padding:10px; border-radius:10px;'>",unsafe_allow_html=True)
        st.write("<h3 style='color:#0077b3;'>Details:</h3>",unsafe_allow_html=True)
        st.write("<table>",unsafe_allow_html=True)
        for i in range(len(details[lang_code])):
            st.write(f"<tr><td><b>{details[lang_code][i]}:</b></td><td>{user_responses[i]}</td></tr>", unsafe_allow_html=True)
            # Read the details out loud
            detail_text = f"{details[lang_code][i]}: {user_responses[i]}"
            detail_audio = text_to_speech(detail_text, lang=lang_code)
            with open(f"detail_{i}_audio.mp3", "wb") as f:
                f.write(detail_audio.getbuffer())
            autoplay_audio(f"detail_{i}_audio.mp3", delay=len(detail_text) * 0.1)  # Adjust the delay based on the length of the detail text
            time.sleep(len(detail_text) * 0.1)  # Additional delay for processing
        st.write("</table>",unsafe_allow_html=True)
        st.write("</div>",unsafe_allow_html=True)
        # Write user responses to CSV
        filename = "user_responses.csv"
        file_exists = os.path.exists(filename)
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["ID", "Name", "Address", "City", "State"])  # Writing header row if file is empty
            if lang_code == 'hi':
                user_responses = [translate_text(response, src_lang='hi', dest_lang='en') for response in user_responses]
            writer.writerow(user_responses)
           # Adding Search by ID functionality
    search_id_button_label = "Update Details" if lang_code == 'en' else "विवरण बदले"
    search_id_button = st.button(search_id_button_label)
    if search_id_button:
        id_prompt = "Please speak your ID." if lang_code == 'en' else "कृपया अपना आईडी बोलें।"
        #st.write(id_prompt)
        display_and_speak_message(id_prompt, lang_code)
        user_id = speech_to_text(lang=lang_code)
        # Load records from CSV file
        filename = "user_responses.csv"
        records_found = False
        if os.path.exists(filename):
            with open(filename, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == user_id:  # Assuming the ID is in the first column
                        records_found = True
                        st.write("<div style='background-color:#e6f7ff; padding:10px; border-radius:10px;'>",unsafe_allow_html=True)
                        st.write("<h3 style='color:#0077b3;'>Record found! Details:</h3>",unsafe_allow_html=True)
                        st.write("<table>",unsafe_allow_html=True)
                        # Display details and read them out loud
                        for i in range(1, len(row)):
                            if lang_code == 'en':
                                st.write(f"<tr><td><b>{details['en'][i]}:</b></td><td>{row[i]}</td></tr>", unsafe_allow_html=True)
                            elif lang_code == 'hi':
                                translated_detail = translate_text(row[i], src_lang='en', dest_lang='hi')
                                st.write(f"<tr><td><b>{details['hi'][i]}:</b></td><td>{translated_detail}</td></tr>", unsafe_allow_html=True)
                            # Read the details out loud
                            detail_text = f"{details[lang_code][i]}: {row[i]}"
                            detail_audio = text_to_speech(detail_text, lang=lang_code)
                            with open(f"detail_{i}_audio.mp3", "wb") as f:
                                f.write(detail_audio.getbuffer())
                            autoplay_audio(f"detail_{i}_audio.mp3", delay=len(detail_text) * 0.1)  # Adjust the delay based on the length of the detail text
                            time.sleep(len(detail_text) * 0.1)  # Additional delay for processing
                        st.write("</table>",unsafe_allow_html=True)
                        # Ask if the user wants to update any record
                        update_prompt = "What do you want to update?" if lang_code == 'en' else "आप क्या बदलना चाहते हैं?"
                        st.write(update_prompt)
                        update_audio = text_to_speech(update_prompt, lang=lang_code)
                        with open("update_audio.mp3", "wb") as f:
                            f.write(update_audio.getbuffer())
                        autoplay_audio("update_audio.mp3", delay=len(update_prompt.split()) * 0.1)  # Adding a buffer delay
                        time.sleep(len(update_prompt) * 0.1)  # Additional delay for processing
                        update_response = speech_to_text(lang=lang_code)
                        field_names = [field.lower() for field in details[lang_code]]
                        if update_response.lower() in field_names:
                            #st.write(f"Please speak the updated {update_response}.")
                            ask_what_to_change = f"Please speak the updated {update_response}." if lang_code == 'en' else f"कृपया नया  {update_response} बोलें."
                            display_and_speak_message(ask_what_to_change, lang_code)
                            updated_value = speech_to_text(lang=lang_code)
                            # Update the value in the row
                            index = field_names.index(update_response.lower())
                            updated_value = updated_value if lang_code == 'en' else translate_text(updated_value, src_lang='hi', dest_lang='en')
                            row[index] = updated_value
                            success_message = "Record updated successfully." if lang_code == 'en' else "रिकॉर्ड सफलतापूर्वक अपडेट किया गया।"
                            display_and_speak_message(success_message, lang_code)
                            for i in range(1, len(row)):
                                if lang_code == 'en':
                                    st.write(f"<tr><td><b>{details['en'][i]}:</b></td><td>{row[i]}</td></tr>", unsafe_allow_html=True)
                                elif lang_code == 'hi':
                                    translated_detail = translate_text(row[i], src_lang='en', dest_lang='hi')
                                    st.write(f"<tr><td><b>{details['hi'][i]}:</b></td><td>{translated_detail}</td></tr>", unsafe_allow_html=True)
                                # Read the details out loud
                                detail_text = f"{details[lang_code][i]}: {row[i]}"
                                detail_audio = text_to_speech(detail_text, lang=lang_code)
                                with open(f"detail_{i}_audio.mp3", "wb") as f:
                                    f.write(detail_audio.getbuffer())
                                autoplay_audio(f"detail_{i}_audio.mp3", delay=len(detail_text) * 0.1)  # Adjust the delay based on the length of the detail text
                                time.sleep(len(detail_text) * 0.1)
                                #Additional delay for processing
                            st.write("</table>",unsafe_allow_html=True)
                            # Rewrite the updated row to CSV file
                            updated_records = []
                            with open(filename, mode="r", encoding="utf-8") as file:
                                reader = csv.reader(file)
                                for r in reader:
                                    if r[0] == user_id:
                                        updated_records.append(row)
                                    else:
                                        updated_records.append(r)
                            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                                writer = csv.writer(file)
                                writer.writerows(updated_records)
                        else:
                            #st.write("Invalid field name.")
                            inv_field_name = "Invalid Field Name" if lang_code == 'en' else "अमान्य फ़ील्ड नाम"
                            display_and_speak_message(inv_field_name, lang_code)
                        break
        if not records_found:
            st.write("<div style='background-color:#ffe6e6; padding:10px; border-radius:10px;'>",unsafe_allow_html=True)
            st.write("<h3 style='color:#ff3333;'>Record not present.</h3>",unsafe_allow_html=True)
            st.write("</div>",unsafe_allow_html=True)
if __name__ == "__main__":
    main()

