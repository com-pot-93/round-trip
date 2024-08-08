import sys, json
sys.path.append("model_evaluation")
sys.path.append("model_evaluation/evaluation")
from bpmn_schema_helper import BPMNProcessor
import bpmn_similarity

examples = "model_evaluation/examples"

filename_ground_truth = "{}/E_j04.json".format(examples)
with open(filename_ground_truth, "r") as infile:
    E4 = json.load(infile)


filename_generated = "{}/E_j04_4.bpmn2 _ Signavio.json".format(examples)
with open(filename_generated, "r") as infile:
    E4_1 = json.load(infile)


filename_generated = "{}/process_complex.json".format(examples)
with open(filename_generated, "r") as infile:
    pc = json.load(infile)

# load in a generated and a ground truth from minimal json format
filename_generated = "{}/1_generated.json".format(examples)
with open(filename_generated, "r") as infile:
    generated = json.load(infile)

filename_generated = "{}/1_1_generated.json".format(examples)
with open(filename_generated, "r") as infile:
    generated1 = json.load(infile)


filename_generated = "{}/1_groundt.json".format(examples)
with open(filename_generated, "r") as infile:
    gt = json.load(infile)

filename_generated = "{}/1_1_groundt.json".format(examples)
with open(filename_generated, "r") as infile:
    gt1 = json.load(infile)

# print(E4)
# print(E4_1)
# print(pc)
# print(generated)
# print(gt)

# parse the signavio json into minimal json format
processor = BPMNProcessor()
transformed_data = processor.transform_to_bpmn_schema(E4)
E4_json = processor.to_json()

transformed_data = processor.transform_to_bpmn_schema(E4_1)
E4_1_json = processor.to_json()
#
# transformed_data = processor.transform_to_bpmn_schema(pc)
# pc_json = processor.to_json()
#
# extract the sets of elements from the minimal
# mysets = bpmn_similarity.extract_bpmn_sets(json.loads(E4_json))
# mysets = json.dumps(mysets, sort_keys=True, indent=4)
#
# print(E4_json)
# print(E4_1_json)

# similarity = bpmn_similarity.calculate_similarity_scores(json.loads(E4_json), json.loads(E4_1_json))
# similarity = json.dumps(similarity, sort_keys=True, indent=4)
# print(similarity)

similarity = bpmn_similarity.calculate_similarity_scores(generated1, gt1)
similarity = json.dumps(similarity, sort_keys=True, indent=4)
print(similarity)

