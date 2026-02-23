import streamlit as st
import random
import wikipedia
import requests
from googlesearch import search
import ast, operator

# ------------------ Page Setup ------------------ #
st.set_page_config(page_title="AnswerBot", page_icon="🤖", layout="wide")
st.title("AnswerBot 🤖")
st.markdown("Ungaloda smart Tamil AI assistant 🔥")

# ------------------ Basic Knowledge ------------------ #
knowledge = {
    "vanakkam": "Vanakkam 😊 Ungalukku eppadi help panna?",
    "hi": "Hi ungaluku ena help venum",
    "hlo": "hlo ungaluku ena help venum",
    "hello": "hello ungaluku ena help venum",
    "Hi": "Hi ungaluku ena help venum",
    "Hello": "Hello ungaluku ena help venum",
    "hey": "hey ungaluku ena help venum",
    "Hey": "Hey ungaluku ena help venum",
    "nee yaru": "Naan unga AnswerBot assistant 😎",
    "who created you": "Naan Python & Streamlit use panni abisheka create pannina oru assistant😁"
}

default_replies = [
    "Konjam detail ah sollunga 😄",
    "Interesting question 🤔",
    "Idha konjam clarify pannunga 👀"
]

# ------------------ Weather Function ------------------ #
def get_weather(city):
    try:
        
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response = requests.get(geo_url).json()
        
        if not geo_response.get("results"):
            return f"Sariyaana city name kudunga. {city} kidaikala! 😅"
            
        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(weather_url)
        data = response.json()
        
        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]
        
        return f"☁️ {city.title()} Weather:\nTemperature: {temp}°C\nWind Speed: {wind} km/h"
    
    except Exception:
        return "Weather info kidaikala 😅"



# ------------------ Google Search Function ------------------ #
def google_search(query):
    try:
        results = list(search(query, num_results=3))
        if results:
            return f"🔎 Google Result:\n{results[0]}"
        else:
            return "Google la result kidaikala 😅"
    except:
        return "Search error 😅"

# ------------------ Safe Calculator ------------------ #
ops= {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
def safe_eval(expr):
    try:
        # Step 1: String-a tree-ah mathuvom
        node = ast.parse(expr, mode='eval').body
        
        # Step 2: Helper function to calculate recursively
        def eval_node(node):
            # Enn (Number) ah irundha apdiye return pannu
            if isinstance(node, ast.Constant): 
                return node.value
            # Operator (+, -, *, /) ah irundha calculation pannu
            elif type(node.op) in ops:
                left_val = eval_node(node.left)
                right_val = eval_node(node.right)
                return ops[type(node.op)](left_val, right_val)
            else:
                raise ValueError("Unsupported operation")

        return eval_node(node)
    except Exception as e:
        return f"Calculator error 😅"


# ------------------ Session ------------------ #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ Display Chat ------------------ #
chat_container = st.container()
with chat_container:
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 Bot:** {message}")

st.markdown("---")

# ------------------ Input Area ------------------ #
col1, col2 = st.columns([5,1])
# key="input_box" nu neenga kuduthurukinga, athanala session state use panna mudiyum
user_input = col1.text_input("Type your message...", key="input_box", label_visibility="collapsed")


if col2.button("➤"):
    if user_input:
        question = user_input.lower()
        response = ""

        # 1️⃣ Calculator
        if any(op in question for op in ["+", "-", "*", "/"]):
            response = f"🧮 Answer: {safe_eval(question)}"

        # 2️⃣ Weather
        elif "weather" in question:
            words = question.split("in")
            city = words[1].strip() if len(words) > 1 else "Chennai"
            response = get_weather(city)

        # 3️⃣ Local Knowledge
        else:
            found = False
            for key in knowledge:
                if key in question:
                    response = knowledge[key]
                    found = True
                    break

            # 4️⃣ Wikipedia / Google fallback
            if not found:
                try:
                    wikipedia.set_lang("en")
                    response = wikipedia.summary(user_input, sentences=2)
                except:
                    response = google_search(user_input)

        # ------------------ Update Session ------------------ #
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

        # Clear input box
        st.session_state.input_box = " " 
        st.rerun()

# ------------------ Clear Chat ------------------ #
if st.button("Clear Chat 🗑️"):

    st.session_state.chat_history = []








