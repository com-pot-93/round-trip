from src.llm_connect.ask_open_ai import ask_gpt
from src.t2m.create_model import generate_model
from src.model_info.get_information import extract_mermaid_tasks, validate_mermaid, validate_custom_format
from src.m2t.create_description import generate_description
from src.merson.merson_converter import mermaid_to_json,json_to_mermaid
from text_evaluation.text_similarity import get_cosine, sts_bert
import json
import os

# """ examples for llm_connect package """
# response = ask_gpt('gpt-3.5-turbo-instruct','do you know that bpmn is?')
# response = ask_gpt('gpt-3.5-turbo','do you know that bpmn is?')
# response = ask_gpt('gpt-4','do you know that bpmn is?')
#
# """ examples for t2m package """
# model = 'gpt-3.5-turbo'
# description = "The MSPN sents a dismissal to the MSPO .  The MSPO reviews the dismissal .  The MSPO rejects the dismissal of the MSPN or The MSPO confirms the dismissal of the MSPN ."
# generated = generate_model(model,description)
# tasks = extract_mermaid_tasks(generated)
# status = validate_mermaid(generated)
# status,errors = validate_custom_format(generated)
#
# """ examples for m2t package """
# description = generate_description(model,generated)
#
# """ examples for merson package """
# generated = open('examples/mermaid_1.txt', 'r').read()
# newjson = mermaid_to_json(generated)
# print(newjson)
#
# model = open('examples/generated_1.txt')
# elements = json.load(model)
# mermaid = json_to_mermaid(elements)
# print(mermaid)

""" example for text similarity """
text1 = open('examples/text1.txt', 'r').read()
text2 = open('examples/text2.txt', 'r').read()
sim_score = get_cosine(text1,text2)
sim_score_2 = sts_bert(text1,text2)
print(sim_score,sim_score_2)


# directory = "/home/i17/projects/SAP/round-trip/data/pet/ground_mermaid"
# target_directory = "/home/i17/projects/SAP/round-trip/data/pet/ground_json"
# # Iterate over files in directory
# for path, folders, files in os.walk(directory):
#     if files:
#         print(files)
#         #sub = path.split("/")[-1]
#         #print(sub)
#         #os.makedirs(os.path.join(target_directory,sub), exist_ok=True)
#         for file_name in files:
#             f = os.path.join(path, file_name)
#             mermaid = open(f,'r').read()
#             json_model = mermaid_to_json(mermaid)
#             target_file = os.path.join(target_directory,file_name)
#             with open(target_file, 'w') as f:
#                 json.dump(json_model, f)
#


































