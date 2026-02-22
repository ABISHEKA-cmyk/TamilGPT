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
