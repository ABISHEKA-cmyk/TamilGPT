import streamlit as st
import random
import wikipedia
import requests
from googlesearch import search

st.set_page_config(page_title="AnswerBot", page_icon="🤖", layout="wide")

st.title("AnswerBot 🤖")
st.markdown("Ungaloda smart Tamil AI assistant 🔥")
user_input=user_input.lower()
if user_input in ["hi","Hi","Hello","hello","hlo","Hey","Vanakkam"]:
response="Hey vanakkam eppadi help pannanum?","Hi,solu ena pannanum?"
else:
#normal LLM call

# ---------------- BASIC KNOWLEDGE ---------------- #

knowledge = {
    "vanakkam": "Vanakkam 😊 Ungalukku eppadi help panna?",
    "nee yaru": "Naan unga AnswerBot assistant 😎",
    "who created you": "Naan Python & Streamlit use panni create pannapatten 😁"
}

default_replies = [
    "Konjam detail ah sollunga 😄",
    "na innum kathukitu iruka 🤔",
    "na training eduthutu iruka seekram best answer kuduka 👀"
]

# ---------------- WEATHER FUNCTION ---------------- #

def get_weather(city):
    try:
        api_key = st.secrets["3187ea149fd7bd9f10294e6f442727ab"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"🌤️ {city.title()} Weather:\nTemperature: {temp}°C\nCondition: {desc}"
        else:
            return "Weather info kidaikala 😅"
    except:
        return "Weather system error 😅"

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

# ---------------- DISPLAY CHAT ---------------- #

chat_container = st.container()

with chat_container:
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 Bot:** {message}")

st.markdown("---")

# ---------------- INPUT AREA ---------------- #

col1, col2 = st.columns([5,1])

user_input = col1.text_input("Type your message...", label_visibility="collapsed")

if col2.button("➤"):

    if user_input:

        question = user_input.lower()
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
            words = question.split("in")
            if len(words) > 1:
                city = words[1].strip()
            else:
                city = "Chennai"
            response = get_weather(city)

        # 3️⃣ Local Knowledge
        else:
            found = False
            for key in knowledge:
                if key in question:
                    response = knowledge[key]
                    found = True
                    break

            # 4️⃣ Wikipedia
            if not found:
                try:
                    wikipedia.set_lang("en")
                    response = wikipedia.summary(user_input, sentences=2)
                except:
                    response = google_search(user_input)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))
        st.rerun()

# ---------------- CLEAR CHAT ---------------- #

if st.button("Clear Chat 🗑️"):
    st.session_state.chat_history = []
    st.rerun()




