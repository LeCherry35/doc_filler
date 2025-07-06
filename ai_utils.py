from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

class ResponseForHTML(BaseModel):
    document_html: str = Field(description="Заповнений HTML документ даними з JSON")
    filled_info: str = Field(description="Інформація з JSON, яка була використана для заповнення HTML документу у форматі поле : значення")
    missing_info: str = Field(description="Список полів з документу якы не були заповнены через те що в JSON не було відповідних даних.")
    comments: str = Field(description="Коментарі до заповнення HTML документу")
    

def fill_html_with_agent(doc, json):
    llm_w_structured_output_for_html = llm.with_structured_output(ResponseForHTML)

    prompt = f"""Ти досвідчений спеціаліст з проведення різного роду закупівель. 
Ти отримуєш документ у форматі HTML і JSON, який містить релевантну інформацію до цього договору. 

Твоя задача —:
1. Заповнити шаблон договору в HTML, використовуючи дані з JSON.
2. Повернути заповнений HTML у полі `document_html`.
3. Повернути `filled_info` як **словник** `поле : значення`, які були використані.
4. Повернути `missing_info` як **список полів**, які потребуются для заповнення документу, але таких не було знайдено в наданому JSON.
5. Додати короткі коментарі у полі `comments`.

Формат відповіді має відповідати зазначеній структурі.

Текст договору:
{doc}

Дані для заповнення:
{json}
"""

    model_response = llm_w_structured_output_for_html.invoke(prompt)
    
    return model_response

class ResponseForStructuredOutput(BaseModel):
    fields: str = Field(description="Список полів, які потребують заповнення у форматі масиву строк 'путь.до.поля': 'якою інформацією заповнити'")
    
def find_fields_for_fulfillment(doc):
    
    llm_w_structured_output_for_g_doc = llm.with_structured_output(ResponseForStructuredOutput)
    prompt = f"""Ти досвідчений експерт по заповненню різного роду документів.
    Ти отримуєш документ у форматі json, структурованного google docs.
    Твоя задача уважно проаналізувати документ та знайти всі поля, які потребують заповнення і визнати якою інформацією ці поля заповняти.
    Поверни список полів, які потребують заповнення у форматі:
    {{
        "путь.до.поля1": "якою інформацією заповнити",
        "путь.до.поля2": "якою інформацією заповнити",
        ...
    }}
    Формат відповіді має відповідати зазначеній структурі.
    
    Документ:
    {doc}
    """
    
    model_response = llm_w_structured_output_for_g_doc.invoke(prompt)
    
    return model_response

class ResponsoForFulfillFields(BaseModel):
    fulfilled_fields: str = Field(description="Список полів, які були заповнені у форматі масиву строк 'путь.до.поля': 'значення'")
    missing_fields: str = Field(description="Список полів, які не були заповнені через відсутність даних у JSON")
    comments: str = Field(description="Коментарі до заповнення полів")
    
def fulfill_fields_with_json(fields, json):
    prompt = f"""Ти досвідчений експерт по заповненню різного роду документів.
    Ти отримуєш список полів, які потребують заповнення та JSON, який містить інформацію для заповнення цих полів. Не вся потрібна інформація може бути знайдена в JSON
    Твоя задача заповнити список полів, які потребують заповнення, інформацією з JSON.
    1.Поверни список полів, які були заповнені у полі fulfilled_fields у форматі:
    {{
        "путь.до.поля1": "значення",
        "путь.до.поля2": "значення",
        ...
    }}
    2.Поверни список полів, які не були заповнені через відсутність даних у JSON у полі missing_fields у форматі:
    ["путь.до.поля1": "опис очікуванного значення", "путь.до.поля2": "опис очікуванного значення", ...]
    3. Додай короткі коментарі до заповнення полів у полі comments якщо необхідно.
    Формат відповіді має відповідати зазначеній структурі.
    Список полів для заповнення:
    {fields}
    Дані для заповнення:
    {json}
    """
    
    llm_for_fulfill_fields = llm.with_structured_output(ResponsoForFulfillFields)
    
    model_response = llm_for_fulfill_fields.invoke(prompt)
    return model_response
    