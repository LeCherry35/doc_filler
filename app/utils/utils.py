import requests
import json
import html

def get_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
    
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def get_doc_html(id):
    url = f"https://docs.google.com/document/d/{id}/export?format=html"
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        decoded_text = html.unescape(text)
        return decoded_text
    else:
        raise Exception(f"Error fetching HTML: {response.status_code}")
    
