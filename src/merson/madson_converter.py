from src.model_info.get_information import get_task_nodes
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
    tasks = []
    gateways = []
    events = []
    temp = []
    tempflow = []
    content = content.splitlines()
    counter = 0
    for c in content:
        if '->' in c:
            flow = {}
            nodes = c.split("->")
            for i in range(len(nodes)):
                n = nodes[i].strip()
                if '"' in n:
                    n = re.findall('"([^"]*)"', n)[0]
                if n not in temp:
                    temp.append(n)
                flow["id"] = "sf{}".format(counter)
                if i == 0:
                    flow["sourceRef"] = n
                elif i == 1:
                    flow["targetRef"] = n
            if flow:
                tempflow.append(flow)
                counter = counter + 1

    for t in range(0,len(temp)):
        node_id = t
        node_label = temp[t]
        if '_SPLIT' in node_label or '_JOIN' in node_label:
            if 'AND' in node_label:
                elements["gateways"][node_id] = 'parallelgateway'
            elif 'OR' in node_label:
                elements["gateways"][node_id] = 'inclusivegateway'
            elif 'XOR' in node_label:
                elements["gateways"][node_id] = 'exclusivegateway'
        elif '_NODE' in node_label:
            if 'START' in node_label:
                elements["events"][node_id] = 'startevent'
            elif 'END' in node_label:
                elements["events"][node_id] = 'endevent'
        else:
             elements["tasks"][node_id] = node_label

    for tf in tempflow:
        tf['sourceRef'] = temp.index(tf['sourceRef'])
        tf['targetRef'] = temp.index(tf['targetRef'])
    elements["sequenceFlows"] = tempflow
    return elements


""" return the last id in the model """
def get_max_keys(elements):
    elements.pop('sequenceFlows', None)
    ids = []
    for e in elements:
        key = list(elements[e].keys())
        ids.extend(key)
    ids = [eval(i) for i in ids]
    maxi = max(ids) + 1
    return maxi

""" adjust the list of unique elements according to the sap schema """
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
                elif "parallel" in elements[e][t]:
                    gateway = {'id': t,'type':'Parallel'}
                elif "inclusive" in elements[e][t]:
                    gateway = {'id': t,'type':'Inclusive'}
                else:
                    gateway = {'id': t,'type':'UNDEFINED'}
                final["gateways"].append(gateway)
    final["sequenceFlows"] = elements["sequenceFlows"]
    final = json.dumps(final, indent = 4)
    return final

""" convert mermaid.js model into bpmn.json """
def mad_to_json(generated):
    all_nodes = get_elements(generated,deepcopy(template))
    converted = sort_elements(all_nodes,deepcopy(final_template))
    return converted

def transform_nodes(model):
    nodes = {}
    for etype in model:
        for e in model[etype]:
            elem_id = e["id"]
            if etype == "tasks":
                task_label = e["name"]
                node = "{}:{}:({})".format(elem_id,"task",task_label)
                nodes[elem_id] = node
            elif etype == "events":
                event_type = e["type"]
                if "start" in event_type.lower():
                    node_type = "startevent"
                    event_label = "start event"
                elif "end" in event_type.lower():
                    node_type = "endevent"
                    event_label = "end event"
                else:
                    continue
                node = "{}:{}:(({}))".format(elem_id,node_type,event_label)
                nodes[elem_id] = node
            elif etype == "gateways":
                gateway_type = e["type"].lower()
                if gateway_type == "exclusive" or "exclusive" in gateway_type:
                    node_type = "exclusivegateway"
                    gate_label = "x"
                elif gateway_type == "parallel" or "parallel" in gateway_type:
                    node_type = "parallelgateway"
                    gate_label = "AND"
                else:
                    continue
                node = "{}:{}:{{{}}}".format(elem_id,node_type,gate_label)
                nodes[elem_id] = node
    print(nodes)
    return nodes

def define_structure(model,nodes):
    tupels = []
    flow = model["sequenceFlows"]
    for f in flow:
        source = f["sourceRef"]
        target = f["targetRef"]
        tupel = "{} --> {}".format(nodes[source],nodes[target])
        tupels.append(tupel)
    mermaid = "\n".join(tupels)
    mermaid = "graph LR\n" + mermaid
    return mermaid

def json_to_mermaid(json_data):
    nodes = transform_nodes(json_data)
    new_model = define_structure(json_data,nodes)
    return new_model

