import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()

GOOGLE_API_KEY = "AIzaSyA6VAI5qzNfsMnCr3c5X4z5X7LkQNji6-I"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def fill_with_model(doc, json):

    prompt = f"""Ти досвідчений спеціаліст з проведення різного рода закупівель. 
    Ти отримуєш документ у форматі HTML і JSON, який містить інформацію релевантну до цього договору. Твоя задача - заповнити шаблон договору, який знаходиться у документі HTML, використовуючи дані з JSON. Якщо деякі дані відсутні, то ти можеш їх пропустити.

    Текст договору:
    {doc}

    Дані для заповнення:
    {json}"""

    model_response = model.generate_content(prompt)
    return model_response.text

def ask_model(prompt):
    model_response = model.generate_content(prompt)
    return model_response.text