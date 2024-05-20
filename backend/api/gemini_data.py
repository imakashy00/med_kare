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
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
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
                "You are an AI assistant.You are given \"<Location>\" or \"<practice>\" of doctor like physician or "
                "or any combination of these context .Provide the details of doctors in JSON FORMAT.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "["
                "{"
                "\"doc_name\":\"<DOCTOR_NAME>\",\n\n"
                "\"doc_specialization\":\"<DOCTOR_SPECIALIZATION>\",\n\n"
                "\"doc_address\":\"<DOCTOR_ADDRESS>\",\n\n",
                "\"doc_rating\":\"<DOCTOR_RATING>,\"\n\n",
                "\"doc_experience\":\"<DOCTOR_EXPERIENCE>\",\n\n"
                "\"doc_fee\":\"<DOCTOR_FEE>\",\n\n"
                "\"doc_email\":\"<DOCTOR_EMAIL>\",\n\n"
                "}",
                "]"
            ],
        },
    ]
)


# ask gemini to generate a response

def gemini_response(user_input):
    response = chat_session.send_message(user_input)
    return response.parts[0].text
