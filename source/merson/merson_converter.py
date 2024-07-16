from source.t2m.create_model import get_task_nodes
from copy import deepcopy
import json
import re

template = {
    "tasks":{},
    "events":{},
    "gateways":{},
    "sequenceFlows":[]
}

final_template = {
    "tasks":[],
    "events":[],
    "gateways":[],
    "pools":[],
    "sequenceFlows":[],
    "messageFlows":[]
}

""" extract unique list of tasks from generated mermaid.js model """
def get_elements(content,elements):
    content = content.splitlines()
    counter = 0
    for c in content:
        flow = {}
        nodes = c.split("-->")
        for i in range(len(nodes)):
            n = nodes[i]
            if ":" in n:
                node_id = n.split(":")[0].strip()
                node_type =  n.split(":")[1].strip()
                if "|" in node_id:
                    node_id = re.search(r'(\d+$)',node_id).group()
                flow["id"] = "sf{}".format(counter)
                if i == 0:
                    flow["sourceRef"] = node_id
                elif i == 1:
                    flow["targetRef"] = node_id

                if "task" in node_type:
                    label = get_task_nodes(n,r'\((.*?)\)')
                    if label:
                        elements["tasks"][node_id] = label
                elif "event" in node_type:
                    elements["events"][node_id] = node_type
                elif "gateway" in node_type:
                    elements["gateways"][node_id] = node_type
        if flow:
            elements["sequenceFlows"].append(flow)
            counter = counter + 1
    return elements

def get_max_keys(elements):
    elements.pop('sequenceFlows', None)
    ids = []
    for e in elements:
        key = list(elements[e].keys())
        ids.extend(key)
    ids = [eval(i) for i in ids]
    maxi = max(ids) + 1
    return maxi

def sort_elements(elements,final):
    for e in elements:
        for t in elements[e]:
            if e == "tasks":
                task = {'id': t,'name':elements[e][t],'type':'User'}
                final["tasks"].append(task)
            elif e == "events":
                if "start" in elements[e][t]:
                    event = {'id': t,'name':'start','type':'StartNoneEvent'}
                elif "end" in elements[e][t]:
                    event = {'id': t,'name':'end','type':'EndNoneEvent'}
                final["events"].append(event)
            elif e == "gateways":
                if "exclusive" in elements[e][t]:
                    gateway = {'id': t,'type':'Exclusive'}
                elif "end" in elements[e][t]:
                    gateway = {'id': t,'type':'Parallel'}
                final["gateways"].append(gateway)
    final["sequenceFlows"] = elements["sequenceFlows"]
    final = json.dumps(final, indent = 4)
    return final

def mermaid_to_json(generated):
    all_nodes = get_elements(generated,deepcopy(template))
    converted = sort_elements(all_nodes,deepcopy(final_template))
    return converted

