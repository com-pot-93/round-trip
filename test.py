from source.llm_connect.ask_open_ai import ask_gpt
from source.t2m.create_model import generate_model, extract_mermaid_tasks, validate_mermaid, validate_custom_format
from source.m2t.create_description import generate_description
from source.merson.merson_converter import mermaid_to_json
import json
# test = ask_gpt('gpt-3.5-turbo-instruct','do you know that bpmn is?')
# print(test)

# test = ask_gpt('gpt-3.5-turbo','do you know that bpmn is?')
# print(test)

# test = ask_gpt('gpt-4','do you know that bpmn is?')
# print(test)

# test = ask_gpt('gpt-4','do you know that bpmn is?','imagine please that you are a process modeler and an expert in this domain')
# print(test)

#model = 'gpt-3.5-turbo'
#description = "The MSPN sents a dismissal to the MSPO .  The MSPO reviews the dismissal .  The MSPO rejects the dismissal of the MSPN or The MSPO confirms the dismissal of the MSPN ."

#generated = generate_model(model,description)
#print(generated)

#description = generate_description(model,generated)
#print(description)
generated = """graph LR
1:startevent:((start event)) --> 2:task:(MSPN sends a dismissal)
2:task:(MSPN sends a dismissal) --> 3:task:(MSPO reviews the dismissal)
3:task:(MSPO reviews the dismissal) --> 4:exclusivegateway:{Decision}
4:exclusivegateway:{Decision} -- Rejected --> 5:task:(MSPO rejects the dismissal of the MSPN)
4:exclusivegateway:{Decision} -- Confirmed --> 6:task:(MSPO confirms the dismissal of the MSPN)
5:task:(MSPO rejects the dismissal of the MSPN) --> 7:endevent:((end event))
6:task:(MSPO confirms the dismissal of the MSPN) --> 7:endevent:((end event))
"""
generated="""
flowchart LR
0:startevent:((startevent))-->1:task:(employee submits vacation request)
1:task:-->2:task:(register the requirement)
2:task:-->3:task:(supervisor receives the request)
3:task:-->4:task:(supervisor approves the request)
4:task:-->5:exclusivegateway:{x}
5:exclusivegateway:-->|not approved|6:task:(return application)
5:exclusivegateway:-->|approved|8:task:(generate notification)
6:task:-->7:exclusivegateway:{x}
8:task:-->9:task:(HR completes the respective management procedures)
9:task:-->7:exclusivegateway:
7:exclusivegateway:-->10:endevent:((endevent))
"""
#generated = """
#graph LR
#1:startevent:((start event)) --> 2:task:(MSPN sends a d)ismissal)
#2:task:( ) --> 3:task:(MSPO reviews the dismissal)
#8:startevent: --> 3:task:
#3 --> 4:exclusivegateway:(Decision)
#3 --> 4:exclusivegateway:(Decision)
#4:gateway: -- Rejected --> 5:task:(MSPO rejects the dismissal of the MSPN)
#4:exclusivegateway: -- Confirmed -> 6:task:(MSPO confirms the dismissal of the MSPN)
#5:task: --> 7:endevent:((end event)
#6:task: --> 7:endevent:((end event))
#"""
#tasks = extract_mermaid_tasks(generated)
#print(tasks)

status = validate_mermaid(generated)
print(status)
new,errors = validate_custom_format(generated)
print(new)
test = mermaid_to_json(generated)
print(test)


