import streamlit as st
import random
import wikipedia
import requests
from googlesearch import search

st.set_page_config(page_title="AnswerBot", page_icon="🤖", layout="wide")

st.title("AnswerBot 🤖")
st.markdown("Ungaloda smart Tamil AI assistant 🔥")

# ---------------- BASIC KNOWLEDGE ---------------- #

knowledge = {
    "vanakkam": "Vanakkam 😊 Ungalukku eppadi help panna?",
    "nee yaru": "Naan unga AnswerBot assistant 😎",
    "who created you": "Naan Python & Streamlit use panni create pannapatten 😁"
}

greetings = ["hi", "hello", "hlo", "hey", "vanakkam"]

default_replies = [
    "Konjam detail ah sollunga 😄",
    "Interesting question 🤔",
    "Idha konjam clarify pannunga 👀"
]

# ---------------- WEATHER FUNCTION ---------------- #
elif "weather" in question:
    
    words = question.split()
    
    # Find city name after "weather"
    if "in" in words:
        city = words[words.index("in") + 1]
    else:
        # If user types "mumbai weather"
        city = words[0]
    
    response = get_weather(city)
# ---------------- GOOGLE SEARCH ---------------- #

def google_search(query):
    try:
        results = list(search(query, num_results=3))
        if results:
            return f"🔎 Google Result:\n{results[0]}"
        else:
            return "Google la result kidaikala 😅"
    except:
        return "Search error 😅"

# ---------------- SESSION ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "show_history" not in st.session_state:
    st.session_state.show_history = False

# ---------------- SIDEBAR (3 DOT STYLE) ---------------- #

with st.sidebar:
    if st.button("⋮ Chat History"):
        st.session_state.show_history = not st.session_state.show_history

    if st.session_state.show_history:
        st.markdown("### 💬 Chat History")
        for sender, message in st.session_state.chat_history:
            st.markdown(f"**{sender}:** {message}")

        if st.button("Clear Chat 🗑️"):
            st.session_state.chat_history = []
            st.rerun()

# ---------------- INPUT AREA ---------------- #

st.markdown("---")

col1, col2 = st.columns([6,1])

user_input = col1.text_input("Type your message...", label_visibility="collapsed")
if col2.button("➤"):

    if user_input:

        question = user_input.lower().strip()
        response = ""

        # 1️⃣ Calculator
        if any(op in question for op in ["+", "-", "*", "/"]):
            try:
                result = eval(question)
                response = f"🧮 Answer: {result}"
            except:
                response = "Calculator error 😅"

        # 2️⃣ Weather
        elif "weather" in question:

            words = question.split()
            city = None

            if "in" in words:
                index = words.index("in")
                if index + 1 < len(words):
                    city = words[index + 1]

            if city is None and len(words) > 1:
                city = words[0]

            if city is None:
                city = "Chennai"

            response = get_weather(city)

        # 3️⃣ Local Knowledge
        elif question in knowledge:
            response = knowledge[question]

        # 4️⃣ Wikipedia / Google fallback
        else:
            try:
                wikipedia.set_lang("en")
                response = wikipedia.summary(user_input, sentences=2)
            except:
                response = google_search(user_input)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))
        st.rerun()

