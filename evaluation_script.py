import os
import json
import tiktoken
import sys
sys.path.append("model_evaluation")
sys.path.append("model_evaluation/evaluation")
sys.path.append("text_evaluation")
#get_simple_kpis
import text_similarity
from jsonschema import validate
from bpmn_schema_helper import BPMNProcessor
import bpmn_similarity
processor = BPMNProcessor()

def get_model_text_similarity(path, gen_tasks, thold):
    if os.path.isfile(path):
        with open(path, "r") as f:
            content = f.read()
            ground_sentences = text_similarity.split_into_sentences(content)
            recall, precision = text_similarity.get_simple_kpis(ground_sentences,gen_tasks,thold)
    else:
        raise Exception('File {} does not exist or is not a file. Please check your input!!!'.format(path))
    return recall, precision

def load_model_from_file(path):
    if os.path.isfile(path):
        with open(path, "r") as infile:
            model = json.load(infile)
    else:
        raise Exception('File {} does not exist or is not a file. Please check your input!!!'.format(path))
    return model

def validate_my_schema(model):
    schema = {
        "type" : "object",
        "properties" : {
            "tasks" : {"type" : "array"},
            "events" : {"type" : "array"},
            "pools" : {"type" : "array"},
            "gateways" : {"type" : "array"},
            "sequenceFlows" : {"type" : "array"},
            "messageFlows" : {"type" : "array"},
        },
        "required": ["tasks", "events", "pools", "gateways", "sequenceFlows", "messageFlows"],
    }
    try:
        validate(instance=model, schema=schema)
    except ValidationError as e:
        raise Exception("Provided model does not correspond to required json schema. Please check your input!!! Error: {}".format(e.message))
    return True

def convert_signavio_to_minimal_json(signavio_json):
    if type(signavio_json) is dict:
        transformed_data = processor.transform_to_bpmn_schema(signavio_json)
        minimal_json = processor.to_json()
        minimal_json = json.loads(minimal_json)
    else:
        raise Exception('File {} is not a valid json file. Please check your input!!!'.format(content_path))
    return minimal_json

def get_basics(model):
    metrix = {}
    if type(model) is str:
        try:
            model = json.loads(model)
        except:
            raise Exception("Model that you provided is not a valid json!!!")

    if type(model) is dict:
        for m in model:
            if m == 'tasks':
                metrix['tasks'] = len(model[m])
            elif m == 'events':
                metrix['events'] = len(model[m])
            elif m == 'gateways':
                metrix['gateways'] = len(model[m])
            elif m == 'pools':
                metrix['pools'] = len(model[m])
                metrix['lanes'] = 0
                for p in model[m]:
                    metrix['lanes'] = metrix['lanes'] + len(p['lanes'])
        return metrix
    else:
        raise Exception("Model that you provided is not a valid json!!!")

def eval_summary(ground_model, gen_model):
    # check models against json schema
    if validate_my_schema(ground_model) and validate_my_schema(gen_model):
        # get general info about the model
        mymetrixs = get_basics(gen_model)
        # get model similarity
        sim_one = bpmn_similarity.calculate_similarity_scores(ground_model, gen_model, method="dice", similarity_threshold=0.75)[0]["overall"]
        sim_two = bpmn_similarity.calculate_similarity_alternative(ground_model, gen_model, method="dice", similarity_threshold=0.75)["overall"]
        mymetrixs['sim_one'] = round(sim_one,2)
        mymetrixs['sim_two'] = round(sim_two,2)
        #TODOs:
        # === calculate number of tokens in originaly generated model (another format) ===
        encoding = tiktoken.get_encoding("cl100k_base")
        encoding = tiktoken.encoding_for_model("gpt-4")    # gpt-3.5-turbo
        text = str(gen_model)
        num_tokens = len(encoding.encode(text))
        mymetrixs['tokens'] = num_tokens
        # get similarity between text and model
        gen_tasks = gen_model['tasks']
        gen_tasks = [sub['name'] for sub in gen_tasks]
        ground_tasks = ground_model['tasks']
        ground_tasks = [sub['name'] for sub in ground_tasks]

        mod_recall, mod_precision = text_similarity.get_simple_kpis(ground_tasks,gen_tasks,0.75)
        recall, precision = get_model_text_similarity(description_path, gen_tasks, 0.75)

        mymetrixs['mod_recall'] = mod_recall
        mymetrixs['mod_precision'] = mod_precision
        mymetrixs['recall'] = recall
        mymetrixs['precision'] = precision
        return mymetrixs


# convert signavio json model to minimal json
ground_path = '../llm-round-trip-correctness/data/mad150/ground_json/account_payable_process_36.json'
content_path = '../text2process-evaluation/datasets/t2p_test_set/output/klu-bpmn-chatbot/account_payable_process_5.json'
description_path = '../llm-round-trip-correctness/data/mad150/process_descriptions/account_payable_process_36.txt'
# TODOs:
# - clarify input formats
# required:
#     - for generated: original generated model (custom format), signavio json model
#     - for groundtruth: minnimal json

# read data from files
ground_model = load_model_from_file(ground_path)
signavio_json = load_model_from_file(content_path)
gen_model = convert_signavio_to_minimal_json(signavio_json)
# TODOs: path original gen model to count munber of tokens

summary = eval_summary(ground_model, gen_model)
print(summary)

















#ground_tasks = ground_model['tasks']
#ground_tasks = [sub['name'] for sub in ground_tasks]
#gen_tasks = gen_model['tasks']
#gen_tasks = [sub['name'] for sub in gen_tasks]

#recall, precision = text_similarity.get_simple_kpis(ground_tasks,gen_tasks,0.75)

#adjusted_list2 = text_similarity.align_sentences(ground_tasks, gen_tasks, threshold=0.9)
#sequence_sim = text_similarity.sequence_similarity(ground_tasks, adjusted_list2)
#other_kpis = text_similarity.calculate_precision_recall(ground_tasks, adjusted_list2)
#overall_sim = 0.5 * sim + 0.5 * sequence_sim


# === model to model comparison ===
# add 3.8 with no lanes and compare it


