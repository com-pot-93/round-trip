from src.llm_connect.ask_open_ai import ask_gpt
from src.t2m.create_model import generate_model
from src.model_info.get_information import extract_mermaid_tasks, validate_mermaid, validate_custom_format
from src.m2t.create_description import generate_description
from src.merson.merson_converter import mermaid_to_json,json_to_mermaid
import json

""" examples for llm_connect package """
response = ask_gpt('gpt-3.5-turbo-instruct','do you know that bpmn is?')
response = ask_gpt('gpt-3.5-turbo','do you know that bpmn is?')
response = ask_gpt('gpt-4','do you know that bpmn is?')

""" examples for t2m package """
model = 'gpt-3.5-turbo'
description = "The MSPN sents a dismissal to the MSPO .  The MSPO reviews the dismissal .  The MSPO rejects the dismissal of the MSPN or The MSPO confirms the dismissal of the MSPN ."
generated = generate_model(model,description)
tasks = extract_mermaid_tasks(generated)
status = validate_mermaid(generated)
status,errors = validate_custom_format(generated)

""" examples for m2t package """
description = generate_description(model,generated)

""" examples for merson package """
generated = open('examples/mermaid_1.txt', 'r').read()
newjson = mermaid_to_json(generated)
print(newjson)

model = open('examples/generated_1.txt')
elements = json.load(model)
mermaid = json_to_mermaid(elements)
print(mermaid)






































