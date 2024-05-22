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
                "If user gives \"<Location>\" or \"<practice>\" of doctor like physician or "
                "or any combination of these context ."
                "Provide the details of at least 5 doctors if no of doctors not specified by user strictly in below "
                "format no other format."
                "Details:"
                    "\"Name\":\"<DOCTOR_NAME>\"\n"
                    "\"Specialization\":\"<DOCTOR_SPECIALIZATION>\"\n"
                    "\"Address\":\"<DOCTOR_ADDRESS>\"\n"
                    "\"Rating\":\"<DOCTOR_RATING>\""
                    "\"Experience\":\"<DOCTOR_EXPERIENCE>\"\n"
                    "\"Fee\":\"<DOCTOR_FEE>\"\n"
                    "\"Email\":\"<DOCTOR_EMAIL>\"\n"
                    "\"Timeslots\":\"<DOCTOR_TIMESLOTS>\"\n"
                "Assume \"<DOCTOR_TIMESLOTS>\" from your side."
                "DOCTOR_TIMESLOTS like: \"9:00-10:00\", \"10:00-11:00\", \"11:00-12:00\" etc."
                "If user says to book an appointment with some doctor that you provided "
                "First confirm the doctor the ask user following details:"
                "details:"
                "1. \"<Name>\", 2. \"<Gender>\", 3. \"<Age>\", 4. \"<Date>\", 5.\"<DOCTOR_TIMESLOTS>\" 6. \"<Email>\""
                "User can select DOCTOR_TIMESLOTS from the timeslots you provided only.If user selects other "
                "timeslots ask him to select from the provided timeslots only then only book appointment."
                "If user provide half details ask for remaining details."
                "IMP:when user provides all the \"<details>\" print the \"<doctor>\"  and \"<user>\" detail in "
                "strictly JSON format."
                "Do not tell the user that it is sample tell them its original and print a 10 digit random number as "
                "booking id."

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
