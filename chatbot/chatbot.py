import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import speech_recognition as sr
from googletrans import Translator

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# Streamlit configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# Custom styling for a cleaner interface and visual clarity
st.markdown(
    """
    <style>
        /* Styling code as in your previous version */
    </style>
    """, unsafe_allow_html=True
)

# Chat header with styling
st.markdown(
    """
    <div style="background-color: #4CAF50; color: white; padding: 15px; text-align: center; font-size: 22px; font-weight: bold; border-radius: 10px;">
        🌟 Welcome to Your AI Chatbot 🌟
    </div>
    """, unsafe_allow_html=True
)

# Main interface section for settings (language selection)
st.markdown("### Language Settings")
language = st.selectbox("Choose Response Language", ["English", "Spanish", "French", "German", "Italian", "Portuguese"])

# Sidebar for other settings
with st.sidebar:
    st.header("Settings")
    dark_mode = st.checkbox("Dark Mode", value=False)
    st.markdown("---")
    st.info("Interact with the AI via text or voice input.")

if dark_mode:
    st.markdown(
        """
        <style>
            body { background-color: #121212; color: white; }
            .stMarkdown { color: white; }
        </style>
        """, unsafe_allow_html=True
    )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function for speech-to-text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening for your speech...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"✅ Recognized: {text}")
            return text
        except sr.UnknownValueError:
            st.error("⚠️ Sorry, I could not understand the speech.")
        except sr.RequestError:
            st.error("⚠️ Could not request results from Google Speech Recognition service.")
        return ""

# Translate text to selected language
def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Display chat messages
for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "assistant"
    message_style = f"""
    <div class="{role_class}">{message['content']}</div>
    """
    st.markdown(message_style, unsafe_allow_html=True)

# Chat input and speech detection
col1, col2 = st.columns([4, 1])

with col1:
    if prompt := st.chat_input("Type your message here..."):
        # Translate the user input to the selected language
        translated_input = translate_text(prompt, language.lower())
        st.session_state.messages.append({"role": "user", "content": translated_input})
        st.markdown(f"<div class='user'>{translated_input}</div>", unsafe_allow_html=True)
        
        # AI generates the response in the selected language
        with st.spinner("🤔 Thinking..."):
            try:
                response = model.generate_content(translated_input).text
                translated_response = translate_text(response, language.lower())
            except Exception as e:
                translated_response = f"❌ Error: {e}"
                
            st.session_state.messages.append({"role": "assistant", "content": translated_response})
            st.markdown(f"<div class='assistant'>{translated_response}</div>", unsafe_allow_html=True)

with col2:
    if st.button("🎙️ Speak"):
        speech_input = recognize_speech()
        if speech_input:
            # Translate speech input to the selected language
            translated_input = translate_text(speech_input, language.lower())
            st.session_state.messages.append({"role": "user", "content": translated_input})
            st.markdown(f"<div class='user'>{translated_input}</div>", unsafe_allow_html=True)
            
            # AI generates the response in the selected language
            with st.spinner("🤔 Thinking..."):
                try:
                    response = model.generate_content(translated_input).text
                    translated_response = translate_text(response, language.lower())
                except Exception as e:
                    translated_response = f"❌ Error: {e}"
                
                st.session_state.messages.append({"role": "assistant", "content": translated_response})
                st.markdown(f"<div class='assistant'>{translated_response}</div>", unsafe_allow_html=True)
