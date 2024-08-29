from src.llm_connect.ask_open_ai import ask_gpt, set_parameter
from src.t2m.create_model import generate_model, generate_json_model
from src.model_info.get_information import extract_mermaid_tasks, validate_mermaid, validate_custom_format
from src.m2t.create_description import generate_description, generate_description_from_json
from src.merson.merson_converter import mermaid_to_json,json_to_mermaid
from text_evaluation.text_similarity import get_cosine, sts_bert, get_kpis
import sys
sys.path.append("model_evaluation")
sys.path.append("model_evaluation/evaluation")
from bpmn_schema_helper import BPMNProcessor
import bpmn_similarity
import json
import os
import re

#=================functions================
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# set default values
processor = BPMNProcessor()
llm = "gpt-4"
orig_models = "data/pet/ground_json"
orig_desc = "data/pet/process_descriptions"
gen_desc =  "experiment/pd_t05"
gen_mods = "experiment/pm_t05"
set_parameter("temperature",0.5)

# # create directories if not exist
# create_directory(gen_desc)
# create_directory(gen_mods)
#
# # generate process descriptions from process models
# for path, folders, files in os.walk(orig_models):
#     for file_name in files:
#         print("-------{}------------------------------".format(file_name))
#         f = os.path.join(path, file_name)
#         pet_json = open(f,'r')
#         model = json.load(pet_json)
#         model = json.dumps(model)
#         description = generate_description_from_json(llm,model)
#         new_file = os.path.join(gen_desc, file_name)
#         with open(new_file, "w") as text_file:
#             text_file.write(description)

# # compare original process description with generated process description
# for path, folders, files in os.walk(gen_desc):
#     for file_name in files:
#         orig_path = os.path.join(orig_desc, file_name)
#         orig = open(orig_path,'r').read()
#         f = os.path.join(path, file_name)
#         gen = open(f,'r').read()
#         # nc_sim = get_cosine(orig,gen)
#         # nc_kpis = get_kpis(orig,gen,"cos")
#         # print(file_name,nc_sim,nc_kpis)
#         c_sim = sts_bert(orig,gen)
#         c_kpis = get_kpis(orig,gen,"bert")
#         print(file_name,c_sim,c_kpis)

# # generate models from generated process desciptions
# for path, folders, files in os.walk(gen_desc):
#      for file_name in files:
#          f = os.path.join(path, file_name)
#          gen = open(f,'r').read()
#          new_model = generate_json_model(llm,gen)
#          new_file = os.path.join(gen_mods, file_name)
#          with open(new_file, 'w') as f:
#              f.write(new_model)
#
# # clean models
# for path, folders, files in os.walk(gen_mods):
#     for file_name in files:
#         print("-------{}------------------------------".format(file_name))
#         f = os.path.join(path, file_name)
#         gen = open(f,'r').read()
#         first = gen.find('{')
#         last = gen.rfind('}') + 1
#         json_str = gen[first:last]
#         try:
#             json_obj = json.loads(json_str)
#             with open(f, 'w') as file:
#                 json.dump(json_obj, file, indent=4)
#         except json.JSONDecodeError as e:
#             print("Not a valid json", e)



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
        similarity = bpmn_similarity.calculate_similarity_scores(json.loads(orig), json.loads(gen))
        similarity = json.dumps(similarity, sort_keys=True, indent=4)
        print(similarity)


# orig_models = "data/pet/ground_json"
# for path, folders, files in os.walk(orig_models):
#     for file_name in files:
#         print("-------{}------------------------------".format(file_name))
#         orig_path = os.path.join(orig_models, file_name)
#         with open(orig_path, "r") as infile:
#             orig = json.load(infile)
#             test = json.loads(orig)
#             #test = json.dumps(test, sort_keys=True, indent=4)
#             with open(orig_path, 'w') as f:
#                 json.dump(test, f, sort_keys=True, indent=4)

# """ examples for merson package """
# generated = open('examples/mermaid_1.txt', 'r').read()
# newjson = mermaid_to_json(generated)
# print(newjson)

# model = open('examples/generated_1.txt')
# elements = json.load(model)
# mermaid = json_to_mermaid(elements)
# print(mermaid)
