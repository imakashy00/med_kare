import os

import google.generativeai as genai

genai.configure(api_key='AIzaSyAfvGLS6bXV99yzu6NEjVHLIunt9Bw7wwM')

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "IMP:You are an AI healthcare assistant 'Med'"
                "You only talks to user about healthcare topics only no other domains."
                "welcome user",
                "If user  talks casual about healthcare give him precise and very short answer."
                "If user gives \"<Location>\" or \"<Specialization>\" of doctor like physician or "
                "or any combination of these context ."
                "Return query detail in Object format.",
                "Name of \"<Location>\" should start with capital letter and \"<Specialization>\" also should start with capital letter."
                    "{"
                    "\"Specialization\":\"<Specialization>\"\n"
                    "\"Location\":\"<Location>\"\n"
                    "}"

                ,
            ],
        },
        {
            "role": "model",
            "parts": [
                "Hi I am Med how can I help you?"
            ],
        },
    ]
)


def talk_to_gemini(input_text):
    print("Med: Hi how can I help you?")
    while input_text != "exit":
        input_text = input("Ak:")
        response = chat_session.send_message(input_text)
        print(response.text)
        if input_text == "exit":
            break


talk_to_gemini("hi gemini")
