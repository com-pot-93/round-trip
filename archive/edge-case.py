from src.llm_connect.ask_open_ai import ask_gpt
from src.t2m.create_model import generate_model, generate_json_model
from src.model_info.get_information import extract_mermaid_tasks, validate_mermaid, validate_custom_format, clean_model
from src.m2t.create_description import generate_description, generate_description_from_json
from src.merson.merson_converter import mermaid_to_json,json_to_mermaid
from text_evaluation.text_similarity import get_cosine, sts_bert
import sys
sys.path.append("model_evaluation")
sys.path.append("model_evaluation/evaluation")
from bpmn_schema_helper import BPMNProcessor
import bpmn_similarity

import json
import os
import csv
import pandas as pd

llm = "gpt-4"

# directory = "data/edge_case/changed/ground_mermaid"
# target_directory = "data/edge_case/changed/ground_json"
# # Iterate over files in directory
# for path, folders, files in os.walk(directory):
#     if files:
#         print(files)
#         for file_name in files:
#             f = os.path.join(path, file_name)
#             mermaid = open(f,'r').read()
#             json_model = mermaid_to_json(mermaid)
#             json_model = json.loads(json_model)
#             target_file = os.path.join(target_directory,file_name)
#             print(json_model)
#             print(type(json_model))
#             with open(target_file, 'w') as f:
#                 json.dump(json_model, f, indent=4)
#


# ------------- generate process description ------------------------------
# directory = "data/edge_case/changed/ground_json"
# target_directory = "data/edge_case/changed/generated_process_description"
# directory = "data/edge_case/original/ground_json"
# target_directory = "data/edge_case/original/generated_process_description"
# # Iterate over files in directory
# for path, folders, files in os.walk(directory):
#     if files:
#         print(files)
#         for file_name in files:
#             f = os.path.join(path, file_name)
#             pet_json = open(f,'r')
#             model = json.load(pet_json)
#             model = json.dumps(model)
#             description = generate_description_from_json(llm,model)
#             number = file_name.split(".")[0]
#             new_file = os.path.join(target_directory, "{}.txt".format(number))
#             with open(new_file, "w") as text_file:
#                 text_file.write(description)

# -------------- generate process models ------------------------------------
# directory = "data/edge_case/changed/generated_process_description"
# target_directory = "data/edge_case/changed/generated_json"
# directory = "data/edge_case/original/generated_process_description"
# target_directory = "data/edge_case/original/generated_json"
# Iterate over files in directory
# for path, folders, files in os.walk(directory):
#     if files:
#         print(files)
#         for file_name in files:
#             f = os.path.join(path, file_name)
#             gen = open(f,'r').read()
#             new_model = generate_json_model(llm,gen)
#             print(new_model)
#             clean_json = clean_model(new_model)
#             number = file_name.split(".")[0]
#             new_file = os.path.join(target_directory, "{}.json".format(number))
#             with open(new_file, 'w') as f:
#                 json.dump(clean_json, f, indent=4)
#

#  compare original process description with generated process description
# gen_mods = "data/edge_case/original/generated_json"
# orig_models = "data/edge_case/original/ground_json"
# gen_mods = "data/edge_case/changed/generated_json"
# orig_models = "data/edge_case/changed/ground_json"

orig_models = "data/edge_case/original/ground_json"
gen_mods = "data/edge_case/changed/ground_json"


output2 = []

for path, folders, files in os.walk(gen_mods):
    for file_name in files:
        print("-------{}------------------------------".format(file_name))
        orig_path = os.path.join(orig_models, file_name)
        with open(orig_path, "r") as infile:
            orig = json.load(infile)
            orig = json.dumps(orig)
        f = os.path.join(path, file_name)
        with open(f, "r") as infile:
            gen = json.load(infile)
            gen = json.dumps(gen)
        sim = bpmn_similarity.calculate_similarity_scores(json.loads(orig), json.loads(gen))
        recall = bpmn_similarity.calculate_similarity_scores(json.loads(orig), json.loads(gen), method="recall")
        precision = bpmn_similarity.calculate_similarity_scores(json.loads(orig), json.loads(gen), method="precision")
        result = {'example': file_name, 'similarity': sim[1], 'recall': recall[1], 'precision': precision[1]}
        output2.append(result)

output_frame2 = pd.DataFrame.from_dict(output2)

with pd.ExcelWriter("orig-chang.xlsx",mode='w') as writer:
    output_frame2.to_excel(writer, sheet_name="m2m", index=False)


























