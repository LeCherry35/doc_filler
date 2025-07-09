from datetime import date
import re

# from weasyprint import HTML
import pdfkit

from app.utils.utils import get_json_data, read_json
# from app.services.google_api import copy_template, replace_placeholders, create_test_file


config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')


DOC_1_TEMPLATE_ID = "1sNA0rrfSfNM3qdFyt1EQmdyteCXWynKK8hw_IrSNFME"
DOC_2_TEMPLATE_ID = "1ZVjHBZ_VaELphD8helt36R6A7E_WysA-EM2BsjGLu08"
DOC_3_TEMPLATE_ID = "1p_wYjLyq4EfVS_-Jcm52FIOlIRYlZlmmAH5iiNOmwGQ"

class DocumentFillerService:
    def serialize_json_data(self, json_id: str):
        json_data_url = f"https://public-api.prozorro.gov.ua/api/2.5/plans/{json_id}"
        print(f"Fetching JSON data from: {json_data_url}")
        data_json = get_json_data(json_data_url)
        
        protocol_number = ""
        today = date.today()
        locality = data_json["data"]["procuringEntity"]["address"]["locality"] or ""
        legal_name = data_json["data"]["procuringEntity"]["identifier"]["legalName"] or ""
        subject_description = data_json["data"]["budget"]["description"] or ""
        dk_id = data_json["data"]["classification"]["id"] or ""
        authorized_person = ""
        
        serialized_data = {
            "protocol_number": protocol_number,
            "protocol_date": str(today),
            "locality": locality,
            "legal_name": legal_name,
            "subject_description": subject_description,
            "dk_id": dk_id,
            "authorized_person": authorized_person,
            
        }
        
        return serialized_data
    
    def fill_html_template(self, html_path: str, values: dict) -> str:

        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        def replacer(match):
            key = match.group(1).strip()
            return str(values.get(key, match.group(0)))

        filled_html = re.sub(r'{{\s*(\w+)\s*}}', replacer, html_content)
        return filled_html
    
    def html_to_pdf_bytes(self, html: str) -> bytes:
        print("Converting HTML to PDF bytes...")
        return pdfkit.from_string(html, False, configuration=config)
    
    # def fill_documents(self, documents, replacements: dict):
    #     replacements = {
    #         "protocol_number": replacements.get("protocol_number", "______"),
    #         "protocol_date": replacements.get("protocol_date", str(date.today())),
    #         "locality": replacements.get("locality", "______"),
    #         "legal_name": replacements.get("legal_name", "___________________"),
    #         "subject_description": replacements.get("subject_description", "__________________"),
    #         "dk_id": replacements.get("dk_id", "______"),
    #         "authorized_person": replacements.get("authorized_person", "____________________"),
    #     }
    #     if "Doc1" in documents:
    #         # document_id = copy_template(DOC_1_TEMPLATE_ID, "Протокол Уповноваженої особи про затвердження Річного плану")
    #         document_id = "12eoQGExvQ4HnVBx5byvQlzSRYXBD8PQ6YYLCORqySt8"
    #         replace_placeholders(document_id, replacements)
    #     if "Doc2" in documents:
    #         # document_id = copy_template(DOC_2_TEMPLATE_ID, "Протокол Уповноваженої особи про початок відкритих торгів та затвердження тендерної документації")
    #         document_id = "16vhJiifCme9nPkPpfuCYXHlRGUFZ8Lyz9pN_-a__6pE"
    #         replace_placeholders(document_id, replacements)
    #     if "Doc3" in documents:
    #         # document_id = copy_template(DOC_3_TEMPLATE_ID, "Протокол Уповноваженої особи про надання роз'яснень до тендерної документації")
    #         document_id = "14l6aG_QqeFBENRXqFJ12pIzgoPzs2ggeDI-bOjCBf6U"
    #         replace_placeholders(document_id, replacements)
        
    
        
    
    