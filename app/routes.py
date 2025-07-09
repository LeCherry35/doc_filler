import io
from flask import Blueprint, render_template, request, jsonify, send_file, make_response

from app.services.document_filler import DocumentFillerService
from app.services.google_api import get_drive_quota

main = Blueprint('main', __name__)

document_filler_service = DocumentFillerService()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/fill-docs', methods=['POST'])
def fill_docs():
    data = request.get_json()
    selected_docs = data.get('selected_docs')
    print(f"Selected documents: {selected_docs}")
    user_data = data.get('user_data')
    doc_id = data.get('document')
    
    res = document_filler_service.fill_html_template(html_path = f"app/protocols/{doc_id}.html", values = user_data)
    
    pdf_bytes = document_filler_service.html_to_pdf_bytes(res)
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='document.pdf'
    )
    
@main.route('/get-json-data/<json_id>', methods=['GET'])
def get_json_data(json_id):
    
    data_json = document_filler_service.serialize_json_data(json_id)
    
    return jsonify(data_json)