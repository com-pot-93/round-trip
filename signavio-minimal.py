import sys
sys.path.append("model_evaluation")
sys.path.append("model_evaluation/evaluation")
from bpmn_schema_helper import BPMNProcessor
import os
import json
import glob

folder_name = '../text2process-evaluation/datasets/'

for filename in os.listdir(folder_name):
    filepath = folder_name + filename
    approaches = filepath + "/generations/"
    if os.path.exists(approaches):
        for app in os.listdir(approaches):
            if app != ".gitkeep":
                apppath = "{}{}/".format(approaches,app)
                if os.path.exists(apppath):
                    for model in os.listdir(apppath):
                        modelpath = "{}{}/".format(apppath,model)
                        if os.path.isdir(modelpath):
                            target_name = modelpath.replace("generations", "generations_minimal")
                            if not os.path.isdir(target_name):
                                os.makedirs(target_name)
                            genlist = glob.glob(modelpath+"*.json")
                            for g in genlist:
                                with open(g, "r") as infile:
                                    signavio_json = json.load(infile)
                                    # parse the signavio json into minimal json format
                                    processor = BPMNProcessor()
                                    transformed_data = processor.transform_to_bpmn_schema(signavio_json)
                                    minimal_json = processor.to_json()
                                    minimal_json = json.loads(minimal_json)
                                    minimalfile = target_name + g.split("/")[-1]
                                    with open(minimalfile, "w") as f:
                                        json.dump(minimal_json, f, indent=4)

