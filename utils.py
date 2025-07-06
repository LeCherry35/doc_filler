import requests
import html
import json

from docs_api import get_doc_service

def get_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
    
def get_html(id):
    url = f"https://docs.google.com/document/d/{id}/export?format=html"
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        decoded_text = html.unescape(text)
        return decoded_text
    else:
        raise Exception(f"Error fetching HTML: {response.status_code}")

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def ask_file_name_and_write(content, format = "txt"):
    file_name = input("Enter the file name to save the content: ")
    
    if format == "json":
        with open(f"output/{file_name}.json", 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
        print(f"Content saved to {file_name}.json")
    else:
        with open(f"output/{file_name}.{format}", 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Content saved to {file_name}.{format}")
    
def get_doc_with_api(doc_id):
    doc_service = get_doc_service()
    document = doc_service.documents().get(documentId=doc_id).execute()
    return document