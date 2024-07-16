from source.t2m.prompt_engineering import mermaid, graphviz
from source.llm_connect.ask_open_ai import ask_gpt
import re
import mermaid as md
from mermaid.graph import Graph
import os

""" prompt for model generation """
def create_prompt(description,set_of_rules,graph_type="mermaid.js"):
    prompt = "Process description: {}. {}. Considering provided process description and a set of custom rules create a valid {} graph.".format(description,set_of_rules,graph_type)
    prompt += "Only a valid graph without any additional text or information must be returned."
    if graph_type == "mermaid.js":
        prompt += "It is also prohibeted to return mermaid diagram with ```mermaid ``` notation!!!"
    return prompt

""" call llm to generate model """
def generate_model(model,description,graph_type="mermaid.js"):
    try:
        if "mermaid" in graph_type:
            set_of_rules = mermaid
        else:
            set_of_rules = graphviz
        prompt = create_prompt(description,set_of_rules,graph_type)
        response = ask_gpt(model,prompt)
        if "```mermaid" in response:
            response = response[response.find('\n')+1:response.rfind('\n')]
        return response
    except Exception as e:
        return e

""" extract text between () from string """
def get_task_nodes(t,reg_ex):
    try:
        label = re.findall(reg_ex, t)
        if label:
            return label[0]
    except:
        return None

""" extract unique list of tasks from generated mermaid.js model """
def extract_mermaid_tasks(content):
    content = content.splitlines()
    elements = []
    try:
        for c in content:
            tasks = c.split("-->")
            for t in tasks:
                if "task" in t:
                    label = get_task_nodes(t,r'\((.*?)\)')
                    if label:
                        elements.append(label)
    except:
        pass
    if elements:
        elements = list(dict.fromkeys(elements))
    return elements

""" check if mermaid model is a valid mermaid.js """
def validate_mermaid(mermaid,file_name="temp"):
    status = 0
    file = "{}.svg".format(file_name)
    graph: Graph = Graph('example-flowchart',mermaid)
    graphe: md.Mermaid = md.Mermaid(graph)
    graphe.to_svg(file)
    f = open(file, "r")
    if "invalid encoded code" in f.read():
        status = 0
    else:
        status = 1
    os.remove(file)
    return status

""" check if mermaid model corresponds to custom predefined rules """
def validate_custom_format(content,details=0):
    status = 1
    elements = {"tasks":{},"events":{}}
    errors = []
    content = content.splitlines()
    counter = 0
    for j in range(len(content)):
        c = content[j]
        if c and "graph" not in c and "flowchart" not in c:
            nodes = c.split("-->")
            if len(nodes) > 2:
                errors.append("There are more nodes than allowed nodes in line #{}".format(j))
            elif len(nodes) <= 1:
                errors.append("There are less nodes than allowed in line #{}".format(j))
            else:
                for i in range(len(nodes)):
                    n = nodes[i]
                    node_parts = n.split(":")
                    if node_parts:
                        if len(node_parts) <= 1:
                            errors.append("There is a node than violate predefined structure in line #{}".format(j))
                        else:
                            node_id = node_parts[0].strip()
                            if "|" in node_id:
                                node_id = re.search(r'(\d+$)',node_id).group()
                            node_type = node_parts[1].strip()
                            node_text = node_parts[2].strip()
                            if "--" in node_text:
                                node_text = node_text.split("--")[0].strip()
                            if "task" in node_type:
                                label = get_task_nodes(n,r'\((.*?)\)$')
                                if label:
                                    if node_id in elements["tasks"]:
                                        if re.search('[a-zA-Z]',label):
                                            if label != elements["tasks"][node_id]:
                                                errors.append("Node #{} has multiple labels".format(node_id))
                                        else:
                                            errors.append("Node #{} has no label".format(node_id))
                                    else:
                                        if re.search(r'[(|)]+',label):
                                            errors.append("Node #{} violates the predefined rules".format(node_id))
                                        else:
                                            elements["tasks"][node_id] = label
                            elif "event" in node_type:
                                if "start" not in node_type and "end" not in node_type:
                                    errors.append("Type of node #{} is not coresponding to the predefined format.".format(node_id))
                                else:
                                    if "start" in node_type:
                                        elements["events"][node_id] = node_type
                                    if not re.match(r'(^\(\(.*?\)\)$)',node_text):
                                       errors.append("The syntax of node #{} is not coresponding to the predefined format.".format(node_id))
                            elif "gateway" in node_type:
                                if "exclusive" not in node_type and "parallel" not in node_type:
                                    errors.append("Type of node #{} is not coresponding to the predefined format.".format(node_id))
                                else:
                                  if node_text:
                                      if not re.match(r'(^\{.*?\}$)',node_text):
                                         errors.append("The syntax of node #{} is not coresponding to the predefined format.".format(node_id))
                            else:
                                errors.append("Nodetype {} is not defined".format(node_type))
    if len(elements["events"]) > 1:
        errors.append("There are multiple start events in the model.".format(node_type))
    if len(errors) > 0:
        status = 0
    return status, errors


