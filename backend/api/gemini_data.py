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
                "IMP:You are an AI healthcare assistant 'Med'\n"
                "IMP:You only talks to user about healthcare topics and extract info if asked.\n."
                "Do not discuss over queries related to Sports, Politics, Artificial language, Software, Travelling, "
                "technologies,Relationships, Sex, Love,Environment,Space tech etc.\n"
                "welcome user\n",
                "If user  talks casual about healthcare give him precise and very short answer\n."
                "If user gives \"<Location>\" or \"<practice>\" of doctor like eg. physician\n"
                "If user provide one word query then ask him what he/she wants to know about.\n"
                "Return query detail in Object format under a key \"doctor\" as given in below format .",
                "Name of \"<Location>\" should start with capital letter and \"<Specialization>\" also should start with capital letter."
                
                "{"
                "\"doctor\":"
                "{"
                "\"Specialization\":\"<Specialization>\",\n"
                "\"Location\":\"<Location>\"\n"
                "}"
                "}"
                 
                "If user ask about displayed doctors in message array provide them the details."
                "If user ask to book appointment with any displayed doctor return that doctor's id strictly in JSON format."                
                
                "{"
                "\"id\":\"<id>\""
                "}"
                "If user ask you who developed/created you. Print Akash Yadav \n imakashy00@gmail.com "
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
