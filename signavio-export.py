import json
import requests
from conf import *
from PIL import Image
from cairosvg import svg2png
from io import BytesIO

# image = Image.open('disaster.png')
# image.show()

base_url = 'https://academic.signavio.com'
dir_ID = '7295ddbbc4534a31a96a820d72fd8cf1'
dir_ID = 'f4beb2ad22174556ae86e902ad5de18d'
mod_format = 'json'  # data format: json, bpmn2_0_xml, PNG or SVG
#mod_format = 'bpmn2_0_xml'
#mod_format = 'svg'
mod_format = 'png'
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

# get all models in the directiry and save them to the folder
# dir_content = get_dir_content(base_url,dir_ID)
# for d in dir_content:
#     if d['rel'] == 'mod':
#         revision_ID = d['rep']['revision']
#         model = get_model(mod_format,base_url,revision_ID)
#         print(model)
#         if mod_format == 'json':
#             name = d['rep']['name'] + '.json'
#             model = json.loads(model)
#             filename = '../PET/pet_json_pools/{}'.format(name)
#             with open(filename, "w") as f:
#                 json.dump(model, f, indent=4)
#         elif mod_format == 'bpmn2_0_xml':
#             name = d['rep']['name'] + '.xml'
#             filename = '../PET/pet_json_no_lanes/{}'.format(name)
#             with open(filename, "w") as f:
#                 f.write(model)
#

# get all models in the directiry and save them to the folder
dir_content = get_dir_content(base_url,dir_ID)
for d in dir_content:
    if d['rel'] == 'mod':
        revision_ID = d['rep']['revision']
        model = get_imodel(mod_format,base_url,revision_ID)
        if mod_format == 'svg':
            name = d['rep']['name'] + '.svg'
            filename = '../PET/pet_images/{}'.format(name)
            with open(filename, "w") as f:
                f.write(model)
        elif mod_format == 'png':
            name = d['rep']['name'] + '.png'
            filename = '../PET/pet_images/{}'.format(name)
            image = Image.open(BytesIO(model))
            image.save(filename, format="PNG")
            #with open(filename, "w") as f:
            #    f.write(model)



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

