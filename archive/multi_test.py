import sys
sys.path.append("..")

from src.llm_connect.ask_open_ai import ask_gpt, set_parameter
from src.t2m.create_model import generate_model
from src.model_info.get_information import extract_mermaid_tasks, validate_mermaid, validate_custom_format
from src.m2t.create_description import generate_description
from src.merson.merson_converter import mermaid_to_json,json_to_mermaid
from src.text_evaluation.text_similarity import get_cosine, sts_bert
import json
import os

import mermaid as md
from mermaid.graph import Graph

set_parameter("temperature",0)

# path = "multi"
# """ examples for t2m package """
# for i in range(0,20):
#     print(i)
#     model = 'gpt-3.5-turbo'
# #    description = "The MSPN sents a dismissal to the MSPO .  The MSPO reviews the dismissal .  The MSPO rejects the dismissal of the MSPN or The MSPO confirms the dismissal of the MSPN ."
#     description = """
# After a claim is registered , it is examined by a claims officer .
# The claims officer then writes a settlement recommendation .
# This recommendation is then checked by a senior claims officer who may mark the claim as OK or Not OK .
# If the claim is marked as Not OK , it is sent back to the claims officer and the recommendation is repeated .
# If the claim is OK , the claim handling process proceeds .
#     """
#     new_model = generate_model(model,description)
#     new_file = os.path.join(path, "{}.txt".format(i))
#     with open(new_file, 'w') as f:
#         f.write(new_model)
#


directory = "multi"
# Iterate over files in directory
for path, folders, files in os.walk(directory):
    if files:
        for file_name in files:
            f = os.path.join(path, file_name)
            mermaid = open(f,'r').read()
            for i in range(0,20):
                new_file = os.path.join(directory, "{}.txt".format(i))
                another = open(new_file,'r').read()
                if mermaid == another:
                    print(file_name,new_file)
                #else:
                #    print("files are different:{},{}".format(file_name,new_file))


directory = "multi"
for path, folders, files in os.walk(directory):
    if files:
        for file_name in files:
            f = os.path.join(path, file_name)
            model = open(f,'r').read()
            sequence = Graph('Sequence-diagram',model)
            mermaid = md.Mermaid(sequence)
            mermaid.to_png("mermaids/{}.png".format(file_name))































