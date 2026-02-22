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

if col2.button("➤") or (user_input and st.session_state.get("last_input") != user_input):

    if user_input:
        st.session_state.last_input = user_input
        question = user_input.lower()
        response = ""

        # 1️⃣ Greetings direct reply
        if question in greetings:
            response = "Hey vanakkam! 😊 Eppadi help pannalam?"

        # 2️⃣ Calculator
        elif any(op in question for op in ["+", "-", "*", "/"]):
            try:
                result = eval(question)
                response = f"🧮 Answer: {result}"
            except:
                response = "Calculator error 😅"

        # 3️⃣ Weather
        elif "weather" in question:
            words = question.split("in")
            city = words[1].strip() if len(words) > 1 else "Chennai"
            response = get_weather(city)

        # 4️⃣ Local Knowledge
        else:
            found = False
            for key in knowledge:
                if key in question:
                    response = knowledge[key]
                    found = True
                    break

            # 5️⃣ Wikipedia
            if not found:
                try:
                    wikipedia.set_lang("en")
                    response = wikipedia.summary(user_input, sentences=2)
                except:
                    response = google_search(user_input)

        st.session_state.chat_history.append(("🧑 You", user_input))
        st.session_state.chat_history.append(("🤖 Bot", response))
        st.rerun()

# ---------------- MAIN CHAT DISPLAY ---------------- #

for sender, message in st.session_state.chat_history:
    if "You" in sender:
        st.markdown(f"**{sender}:** {message}")
    else:
        st.markdown(f"**{sender}:** {message}")



