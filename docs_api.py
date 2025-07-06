from google.oauth2 import service_account
from googleapiclient.discovery import build
from utils import ask_file_name_and_write

# 🔒 Путь к JSON-файлу сервисного аккаунта
SERVICE_ACCOUNT_FILE = 'credentials.json'

# 🔭 Области доступа — только чтение документа
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# 📄 ID Google Docs-документа (замени на свой!)
DOCUMENT_ID = '1Rwm6E3E-3aMjwbTC4aInS62ERWA5q_drRuAsr09TrIY'

# 🔌 Загрузка учетных данных
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

def get_doc_service():
    """Создает и возвращает сервис для работы с Google Docs API."""
    return build('docs', 'v1', credentials=credentials)
# 🔧 Инициализация клиента Docs API
# docs_service = build('docs', 'v1', credentials=credentials)

# ✅ Пробуем получить документ
# document = docs_service.documents().get(documentId=DOCUMENT_ID).execute()

# print(f"Документ: {document}")

# ask_file_name_and_write(document)
