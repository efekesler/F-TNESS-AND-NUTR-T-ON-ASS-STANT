from ollama import chat
from argostranslate import translate


def tr_to_en(text: str) -> str:
    return translate.translate(text, "tr", "en")


def en_to_tr(text: str) -> str:
    return translate.translate(text, "en", "tr")


FITNESS_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a friendly and professional fitness coach.\n"
        "You only talk about physical fitness, exercise, sports, and workouts.\n"
        "You always assume the user is talking about physical training.\n\n"

        "You respond naturally, like a human fitness trainer.\n"
        "You never explain rules, instructions, or how you work.\n"
        "You never mention artificial intelligence, technology, or programming.\n"
        "You never give meta explanations.\n\n"

        "If the user greets you, greet them back and offer fitness-related help.\n"
        "If the user is unclear, ask a short fitness-related follow-up question.\n"
        "Always keep responses simple, encouraging, and practical.\n"
    )
}


# 🔹 Hidden conversation memory
conversation_history = [FITNESS_SYSTEM_PROMPT]


def ask_fitness_assistant(user_input_tr: str) -> str:
    global conversation_history

    # 1️⃣ Translate input
    user_input_en = tr_to_en(user_input_tr)

    # 2️⃣ Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_input_en
    })

    # 3️⃣ Call model with full history
    response = chat(
        model="tinyllama",
        messages=conversation_history
    )

    assistant_reply_en = response["message"]["content"]

    # 4️⃣ Save assistant reply
    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply_en
    })

    # 5️⃣ Translate back
    return en_to_tr(assistant_reply_en)


NUTRITION_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a professional sports nutritionist.\n"
        "You only talk about nutrition, diet, supplements, hydration, and meal planning.\n"
        "You always assume the user is asking about diet or nutrition.\n\n"

        "You respond naturally like a real nutrition coach.\n"
        "You never mention artificial intelligence.\n"
        "You never explain system rules.\n"
        "You never give meta commentary.\n\n"

        "Give practical, realistic, and safe nutrition advice.\n"
        "If information is missing, ask a short relevant nutrition question.\n"
        "Keep answers clear and structured but conversational.\n"
        "Encourage healthy and sustainable habits.\n"
    )
}

conversation_history_two = [NUTRITION_SYSTEM_PROMPT]
def ask_nutrition_assistant(user_input_tr: str) -> str:
    global conversation_history_two

    # 1️⃣ Translate input
    user_input_en = tr_to_en(user_input_tr)

    # 2️⃣ Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_input_en
    })

    # 3️⃣ Call model with full history
    response = chat(
        model="tinyllama",
        messages=conversation_history
    )

    assistant_reply_en = response["message"]["content"]

    # 4️⃣ Save assistant reply
    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply_en
    })

    # 5️⃣ Translate back
    return en_to_tr(assistant_reply_en)





