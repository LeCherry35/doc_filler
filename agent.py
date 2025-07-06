from ai_utils import find_fields_for_fulfillment, fulfill_fields_with_json
from utils import get_doc_with_api, read_json

DOCUMENT_ID = '1Rwm6E3E-3aMjwbTC4aInS62ERWA5q_drRuAsr09TrIY'

doc = get_doc_with_api(DOCUMENT_ID)

fields_for_fulfillment = find_fields_for_fulfillment(doc)

dummy_json = read_json("input/dummy.json")

fulfilled_fields = fulfill_fields_with_json(fields_for_fulfillment, dummy_json)

print(fulfilled_fields['fulfilled_fields'])

