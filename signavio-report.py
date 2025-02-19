import json
import requests
from conf import *
from PIL import Image
from cairosvg import svg2png
from io import BytesIO
import time

# image = Image.open('disaster.png')
# image.show()
base_url = 'https://academic.signavio.com'
dir_ID = '7295ddbbc4534a31a96a820d72fd8cf1'
#dir_ID = 'f4beb2ad22174556ae86e902ad5de18d'
mod_format = 'json'  # data format: json, bpmn2_0_xml, PNG or SVG
#mod_format = 'bpmn2_0_xml'
#mod_format = 'svg'
#mod_format = 'png'
# function to login to signavio
def authenticate(base_url):
    login_url = base_url + '/p/login'
    data = {'name': 'nataliia.klievtsova@tum.de',
            'password': 'Mynewpassword15!',
            'tokenonly': 'true'}
    data['tenant'] = 'da542e4835ec4530be2546df1b09dd9b'
    login_request = requests.post(login_url, data)
    auth_token = login_request.content.decode('utf-8')
    jsesssion_ID = login_request.cookies['JSESSIONID']
    lb_route_ID = login_request.cookies['LBROUTEID']
    return {
        'jsesssion_ID': jsesssion_ID,
        'lb_route_ID': lb_route_ID,
        'auth_token': auth_token
    }

# function to get the content of a directory
def get_dir_content(base_url,dir_ID):
    dir_url = base_url + '/p/directory'
    auth_data = authenticate(base_url)
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
    get_dir_request = requests.get(dir_url + '/' + dir_ID, cookies=cookies, headers=headers)
    dir_content = json.loads(get_dir_request.text)
    return dir_content

# function to get the model from the signavio
def get_model(mod_format,base_url,revision_ID):
    diagram_url = base_url + '/p' + revision_ID + '/' + mod_format
    auth_data = authenticate(base_url)
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
    get_diagram_request = requests.get(diagram_url, cookies=cookies, headers=headers)
    return get_diagram_request.text

def get_imodel(mod_format,base_url,revision_ID):
    diagram_url = base_url + '/p' + revision_ID + '/' + mod_format
    auth_data = authenticate(base_url)
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
    get_diagram_request = requests.get(diagram_url, cookies=cookies, headers=headers)
    return get_diagram_request.content


diagram_ID = '387845ecd2204cc38bfa0294ec254826'
revision_url = base_url + '/p/model/' + diagram_ID + '/revisions'
auth_data = authenticate(base_url)
cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
headers = {'Accept': 'application/json','x-signavio-id':  auth_data['auth_token']}
get_revisions_request = requests.get(revision_url, cookies=cookies, headers=headers)

#print(get_revisions_request.text)

revision_ID = 'cea8571b91a94fba9812ffd44a3ef71c'
diagram_url = base_url + '/p/revision'
syntax_check_url = base_url + '/p/syntaxchecker'
cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
get_diagram_request = requests.get(diagram_url + '/' + revision_ID + '/json', cookies=cookies, headers=headers)
#print(get_diagram_request.content)
syntax_check_request = requests.post(syntax_check_url, cookies=cookies, headers=headers,
                                    data={
                                        'isJson': 'true',
                                        'data_json': get_diagram_request.content,
                                        'ns': 'http://b3mn.org/stencilset/bpmn2.0#'
                                    })

print(syntax_check_request.content)

def bp_conventions_checker(name:str, model_id: str, guideline_id: str, model_json, auth_data):
    #auth_data = SignavioAuthenticator.authenticate()
    system_instance = 'https://academic.signavio.com'
    bp_check_url = system_instance + '/p/mgeditorchecker'
    cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
    headers = {'Accept': 'application/json', 'X-Signavio-ID': auth_data['auth_token']}
    data = {'comments': '{}',
            'guidelineId': guideline_id,
            'name': name,
            'model_json': model_json,
            'id': model_id,
            'checkLinking': 'false'}

    bp_check_request = requests.post(
        bp_check_url,
        cookies=cookies,
        headers=headers,
        data=data)
    response_status = bp_check_request.status_code
    if response_status != 200:
        print(f"API error: expected 200 but received {response_status} from server")
        return

    rep_data = bp_check_request.json().get('rep', [])
    print(rep_data)
    violations_count = {
        'errors': len(rep_data[0].get('must', [])),
        'warnings': len(rep_data[0].get('should', [])),
        'info': len(rep_data[0].get('info', []))
    }
    time.sleep(0.8) # limitation for API calls (50/minute)
    return json.dumps(violations_count)


guideline_id = 'f18c31354e9746a4a0064af6b9649cb5'
name = "New Process test"
model_id = diagram_ID
model_json = get_diagram_request.content
test = bp_conventions_checker(name, model_id, guideline_id, model_json, auth_data)
print(test)








# # get all models in the directiry and save them to the folder
# dir_content = get_dir_content(base_url,dir_ID)
# for d in dir_content:
#     if d['rel'] == 'mod':
#         revision_ID = d['rep']['revision']
#         model = get_model(mod_format,base_url,revision_ID)
#         print(model)
#         if mod_format == 'json':
#             name = d['rep']['name'] + '.json'
#             model = json.loads(model)
#             filename = '../PET/pet_simple_signavio/{}'.format(name)
#             with open(filename, "w") as f:
#                 json.dump(model, f, indent=4)
#         elif mod_format == 'bpmn2_0_xml':
#             name = d['rep']['name'] + '.xml'
#             filename = '../PET/pet_json_no_lanes/{}'.format(name)
#             with open(filename, "w") as f:
#                 f.write(model)
#

# # get all models in the directiry and save them to the folder
# dir_content = get_dir_content(base_url,dir_ID)
# for d in dir_content:
#     if d['rel'] == 'mod':
#         revision_ID = d['rep']['revision']
#         model = get_imodel(mod_format,base_url,revision_ID)
#         if mod_format == 'svg':
#             name = d['rep']['name'] + '.svg'
#             filename = '../PET/pet_images/{}'.format(name)
#             with open(filename, "w") as f:
#                 f.write(model)
#         elif mod_format == 'png':
#             name = d['rep']['name'] + '.png'
#             filename = '../PET/pet_images/{}'.format(name)
#             image = Image.open(BytesIO(model))
#             image.save(filename, format="PNG")
#             #with open(filename, "w") as f:
#             #    f.write(model)
#


# copy models from one directory to antoher (in signavio)
# parent_ID = 'f4beb2ad22174556ae86e902ad5de18d'  # ID of the target directory
# namespace = 'http://b3mn.org/stencilset/bpmn2.0#'  # notation
# model_url = base_url + '/p/model'
# auth_data = authenticate(base_url)
# cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
# headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
# data = {
#    'parent': '/directory/' + parent_ID,
#    'namespace': namespace,
# }
#
# dir_content = get_dir_content(base_url,dir_ID)
# for d in dir_content:
#     if d['rel'] == 'mod':
#         revision_ID = d['rep']['revision']
#         name = d['rep']['name']
#         data['name'] = name
#         model = get_model(mod_format,base_url,revision_ID)
#         data['json_xml'] = model
#         print(data)
#         create_diagram_request = requests.post(model_url, cookies=cookies, headers=headers, data=data)
#         result = str(create_diagram_request.content)
#         print('creating diagram: ' + result)
#


# # ID of the diagram revision you want to retrieve the revision list for
# diagram_ID = '6377221b36e249a68e35213e98491c27'
# revision_url = base_url + '/p/model/' + diagram_ID + '/revisions'
# auth_data = authenticate()
#
# print("-----XXXXXXXXXXXXXXXXXX----------:", auth_data)
#
# # set credentials, response format
# cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
# headers = {'Accept': 'application/json',
#            'x-signavio-id':  auth_data['auth_token']}
#
# get_revisions_request = requests.get(revision_url,
#                                      cookies=cookies,
#                                      headers=headers)
# json_object = json.loads(get_revisions_request.text)
# last_rev = json_object[0]['rep']['size']
# revision_ID = json_object[last_rev]['href']
#

# target_ID = '36e9deae64d9493a9e96e9d3e7b816b1'
# # copy models from one directory to antoher (in signavio)
# namespace = 'http://b3mn.org/stencilset/bpmn2.0#'  # notation
# model_url = base_url + '/p/model'
# auth_data = authenticate(base_url)
# cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
# headers = {'Accept': 'application/json', 'x-signavio-id':  auth_data['auth_token']}
# data = {
#    'parent': '/directory/' + target_ID,
#    'namespace': namespace,
# }
#
# directory = '/home/i17/projects/SAP/domain-models/'
# for filename in os.listdir(directory):
#     file = os.path.join(directory, filename)
#     if file.endswith(('.json')):
#         print(filename)
#         with open(file, 'r') as content:
#             #model = json.load(content)
#             model = content.read()
#             data['name'] = filename
#             data['json_xml'] = model
#             create_diagram_request = requests.post(model_url, cookies=cookies, headers=headers, data=data)
#             result = str(create_diagram_request.content)
#             print('creating diagram: ' + result)
#

