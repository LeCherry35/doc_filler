
import json

from utils import get_json, get_html, read_json, ask_file_name_and_write
from model import fill_with_model
from ai_utils import fill_html_with_agent, find_fields_for_fulfillment


object_url = "https://public-api.prozorro.gov.ua/api/2.5/plans/683a384dea814302b18a3e87af863848"

DOC_ID = "1UIPymd5qjzs_Xwcyo_A3nf8nYCdTrH7CUl3qyU219xA"

doc_response = get_html(DOC_ID)

dummy_json = read_json("input/dummy.json")

# model_response = fill_with_model(doc_response, dummy_json)

# with open("response.html", "w", encoding="utf-8") as f:
#     f.write(model_response)

# agent_response = fill_html_with_agent(doc_response, dummy_json)

doc = read_json("output/docum1.json")
agent_response = find_fields_for_fulfillment(doc)

print(agent_response)
ask_file_name_and_write(str(agent_response))
