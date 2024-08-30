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
import csv
import pandas as pd

#=================functions================
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_model(gen):
    first = gen.find('{')
    last = gen.rfind('}') + 1
    json_str = gen[first:last]
    try:
        json_obj = json.loads(json_str)
    except json.JSONDecodeError as e:
        json_obj = {"error":"Not a valid json"}
    return json_obj


# set default values
processor = BPMNProcessor()
llm = "gpt-4"
orig_models = "data/pet/ground_json"
orig_desc = "data/pet/process_descriptions"
main_directory = "experiment"
temp1 = 0     #temp1 > temp2
temp2 = 0
sub_dir1 = "pd_{}_{}".format(temp1,temp2)
sub_dir2 = "pm_{}_{}".format(temp1,temp2)
output1 = []
output2 = []
#set_parameter("temperature",0.5)

# create directories if not exist
create_directory(main_directory)

# generate process descriptions from process models

for i in range(1,4):
    gen_desc =  os.path.join(main_directory,sub_dir1,str(i))
    # set_parameter("temperature",temp1)
    # create_directory(gen_desc)
    # for path, folders, files in os.walk(orig_models):
    #     for file_name in files:
    #         print("-------{}-------".format(file_name))
    #         f = os.path.join(path, file_name)
    #         pet_json = open(f,'r')
    #         model = json.load(pet_json)
    #         model = json.dumps(model)
    #         description = generate_description_from_json(llm,model)
    #         number = file_name.split(".")[0]
    #         new_file = os.path.join(gen_desc, "{}.txt".format(number))
    #         with open(new_file, "w") as text_file:
    #             text_file.write(description)

    #   compare original process description with generated process description
    # for path, folders, files in os.walk(gen_desc):
    #     for file_name in files:
    #         orig_path = os.path.join(orig_desc, file_name)
    #         orig = open(orig_path,'r').read()
    #         f = os.path.join(path, file_name)
    #         gen = open(f,'r').read()
    #         sim = sts_bert(orig,gen)
    #         kpis = get_kpis(orig,gen,"bert")
    #         result = {'round':i,'example': file_name, 'similarity': sim, 'recall': kpis[0], 'precision': kpis[1]}
    #         output1.append(result)

    # output_frame1 = pd.DataFrame.from_dict(output1)
    # average_metrics = output_frame1.groupby('example').mean()

    # with pd.ExcelWriter("test.xlsx") as writer:
    #     output_frame1.to_excel(writer, sheet_name="t2t", index=False)
    #     average_metrics.to_excel(writer, sheet_name="t2t-aver", index=True)

    # generate models from generated process desciptions
    # set_parameter("temperature",temp2)
    gen_mods =  os.path.join(main_directory,sub_dir2,str(i))
    # create_directory(gen_mods)
    # for path, folders, files in os.walk(gen_desc):
    #      for file_name in files:
    #          f = os.path.join(path, file_name)
    #          gen = open(f,'r').read()
    #          new_model = generate_json_model(llm,gen)
    #          clean_json = clean_model(new_model)
    #          number = file_name.split(".")[0]
    #          new_file = os.path.join(gen_mods, "{}.json".format(number))
    #          with open(new_file, 'w') as f:
    #              json.dump(clean_json, f, indent=4)

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
            result = {'round':i,'example': file_name, 'similarity': sim[1], 'recall': recall[1], 'precision': precision[1]}
            output2.append(result)

    output_frame2 = pd.DataFrame.from_dict(output2)
    average_metrics = output_frame2.groupby('example').mean()

    with pd.ExcelWriter("test.xlsx",mode='a',if_sheet_exists='replace') as writer:
        output_frame2.to_excel(writer, sheet_name="m2m", index=False)
        average_metrics.to_excel(writer, sheet_name="m2m-aver", index=True)

