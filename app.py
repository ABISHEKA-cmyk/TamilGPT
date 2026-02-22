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
    "hi": "Hi 😄 Eppadi help pannalaam?",
    "hello": "Hello 😄 Eppadi help pannalaam?",
    "hlo": "Hello 😄 Eppadi help pannalaam?",
    "nee yaru": "Naan unga AnswerBot assistant 😎",
}

# ---------------- WEATHER FUNCTION ---------------- #
def get_weather(city):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_res = requests.get(geo_url).json()
        if "results" not in geo_res:
            return "City kidaikala 😅"

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url).json()

        temp = weather_res["current_weather"]["temperature"]
        wind = weather_res["current_weather"]["windspeed"]

        return f"🌤️ {city.title()} Weather\n🌡 Temperature: {temp}°C\n💨 Wind Speed: {wind} km/h"
    except:
        return "Weather error 😅"

# ---------------- GOOGLE SEARCH ---------------- #
def google_search(query):
    try:
        results = list(search(query, num_results=1))
        if results:
            return f"🔎 Google Result:\n{results[0]}"
        else:
            return "Google la result kidaikala 😅"
    except:
        return "Search error 😅"

# ---------------- SESSION ---------------- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

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
user_input = col1.text_input(
    "Type your message...",
    value=st.session_state.user_input,
    key="user_input",
    label_visibility="collapsed"
)

# ---------------- MAIN LOGIC ---------------- #
if col2.button("➤") and user_input.strip():

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
        city = question.replace("weather", "").replace("in", "").strip()
        if city == "":
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

    # Append chat history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

    # ✅ Clear input box immediately
    st.session_state.user_input = ""
    st.rerun()

# ---------------- CLEAR CHAT ---------------- #
if st.button("Clear Chat 🗑️"):
    st.session_state.chat_history = []
    st.rerun()
