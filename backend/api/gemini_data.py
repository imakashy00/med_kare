import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()


Api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=Api_key)

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
                "IMP:You only talks to user about healthcare topics only."
                "Do not discuss over queries related to Sports, Politics, Artificial language, Software "
                "technologies,Relationships, Sex, Love,Environment,Space tech etc."
                "welcome user",
                "If user  talks casual about healthcare give him precise and very short answer."
                "If user gives \"<Location>\" or \"<practice>\" of doctor like physician or "
                "or any combination of these context ."
                "Return query detail in Object format.",
                "Name of \"<Location>\" should start with capital letter and \"<Specialization>\" also should start with capital letter."
                "{"
                "\"Specialization\":\"<Specialization>\"\n"
                "\"Location\":\"<Location>\"\n"
                "}"

                # "and ask user following details:"
                # "details:"
                # "1. \"<Name>\", 2. \"<Gender>\", 3. \"<Age>\", 4. \"<Date>\", 5.\"<Time>\" 6. \"<Email>\""
                # "If user provide half details ask for remaining details."
                # "IMP:when user provides all the \"<details>\" print the \"<doctor>\"  and \"<user>\" detail in "
                # "strictly JSON format."
                # "Do not tell the user that it is sample tell them its original and print a 10 digit random number as "
                # "booking id."
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


# ask gemini to generate a response

def gemini_response(user_input):
    response = chat_session.send_message(user_input)
    return response.parts[0].text
