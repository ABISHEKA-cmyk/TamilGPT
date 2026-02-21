import streamlit as st
import random

st.set_page_config(page_title="TamilGPT", page_icon="🤖")

st.title("TamilGPT 🤖")
st.write("Ungal Tamil Assistant")

# ---------------- KNOWLEDGE DATABASE ---------------- #

knowledge = {

# Greetings
"vanakkam": "Vanakkam 😊 Ungalukku eppadi help panna?",
"hello": "Hello 👋",
"hi": "Hi 😄",
"good morning": "Good Morning ☀️",
"good night": "Good Night 🌙",

# Personal
"nee yaru": "Naan unga Tamil assistant 😎",
"ungal peyar": "En peyar TamilGPT 🤖",
"epadi iruka": "Naan nalla iruken 😄 Neenga epadi?",

# Education
"school": "Padippu mukkiyam 📚",
"college": "College life super 🎓",
"exam": "Nalla prepare pannunga ✍️",

# Motivation
"success": "Hard work panna success varum 💪",
"failure": "Tholviyum oru lesson dhaan 📘",
"dream": "Kanavu kaanum ungal future 🔥",

# Tech
"python": "Python easy programming language 🐍",
"ai": "AI na Artificial Intelligence 🤖",

# Tamil Nadu
"tamil": "Tamil oru pazhamaiana mozhi ❤️",
"chennai": "Chennai Tamil Nadu capital 🏙️",
"india": "India oru periya naadu 🇮🇳",

# Add your own below 👇
# "your question": "your answer",

}

default_replies = [
    "Konjam detail ah sollunga 😄",
    "Interesting question 🤔",
    "Naan innum kathukittu iruken 😅",
    "Nice kelvi 👍",
]

# ---------------- SESSION MEMORY ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- USER INPUT ---------------- #

user_input = st.text_input("Ungal kelvi:")

col1, col2 = st.columns(2)

# ---------------- ENTER BUTTON ---------------- #

if col1.button("Enter ✅"):

    if user_input:

        question = user_input.lower()
        response = ""

        # Calculator check
        if any(op in question for op in ["+", "-", "*", "/"]):
            try:
                result = eval(question)
                response = f"🧮 Answer: {result}"
            except:
                response = "Calculator error 😅"

        else:
            found = False

            for key in knowledge:
                if key in question:
                    response = knowledge[key]
                    found = True
                    break

            if not found:
                response = random.choice(default_replies)

        # Save chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

# ---------------- CLEAR BUTTON ---------------- #

if col2.button("Clear Chat 🗑️"):
    st.session_state.chat_history = []

# ---------------- SHOW CHAT HISTORY ---------------- #

st.write("---")
st.subheader("Chat History")

for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.write(f"🧑 You: {message}")
    else:
        st.write(f"🤖 Bot: {message}")