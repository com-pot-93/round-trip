import os
import re
import pandas as pd
import json
from src.merson.madson_converter import mad_to_json


# get unique entries from mad for the excel sheet
main_path = '/home/i17/projects/TUM/data-sets/mad/test_dataset/'
list_folders = next(os.walk(main_path))[1]
excel_file = '/home/i17/projects/TUM/data-sets/mad.xlsx'
# for folder in list_folders:
#     tasksdict = {}
#     final = {}
#     mydict = {}
#     ids = []
#     alldata = []
#
#     folder_name ='/home/i17/projects/TUM/data-sets/mad/test_dataset/{}/'.format(folder)
#     for filename in os.listdir(folder_name):
#         filepath = folder_name + filename
#         if os.path.isfile(filepath):
#             if not '.pdf' in filepath:
#                 with open(filepath, "r") as infile:
#                     tasks = []
#                     and_gateways = []
#                     or_gateways = []
#                     xor_gateways = []
#                     lines = infile.readlines()
#                     for line in lines:
#                         if '[shape=box]' in line:
#                             label = re.findall('"([^"]*)"', line)[0]
#                             tasks.append(label)
#                         elif '->' in line:
#                             parts = line.split('->')
#                             for part in parts:
#                                 part = part.strip()
#                                 if 'AND_SPLIT' in part:
#                                     if part not in and_gateways:
#                                         and_gateways.append(part)
#                                 elif 'OR_SPLIT' in part:
#                                     if part not in or_gateways:
#                                         or_gateways.append(part)
#                                 elif 'XOR_SPLIT' in part:
#                                     if part not in xor_gateways:
#                                         xor_gateways.append(part)
#                     mystring = '{}{}{}{}'.format(len(tasks),len(and_gateways),len(or_gateways),len(xor_gateways))
#                     fileid = re.findall(r'\d+', filename)[0]
#                     mydict[int(fileid)] = mystring
#                     tasksdict[int(fileid)] = tasks
#
#     sorteddict = dict(sorted(mydict.items()))
#     uniquedict = set(sorteddict.values())
#
#     for s in sorteddict:
#         key = sorteddict[s]
#         if not key in final.keys():
#             final[key] = s
#
#     output = []
#     for f in final:
#         file = final[f]
#         output.append([file,f,tasksdict[file]])
#     output_frame = pd.DataFrame(output)
#     with pd.ExcelWriter(excel_file,mode='a',if_sheet_exists='replace') as writer:
#         output_frame.to_excel(writer, sheet_name=folder, index=False)
#

# target_path = '../MAD-150/'
# mypath = '../../TUM/data-sets/'
# with open('{}smallMAD.json'.format(mypath), 'r') as json_file:
#     data = json.load(json_file)
#     for d in data:
#         file_list = data[d]
#         ind_path = '{}mad/test_dataset/{}/'.format(mypath,d)
#         dir_path = '{}{}/'.format(target_path,d)
#         os.makedirs(dir_path, exist_ok=True)
#         for f in file_list:
#             desc_path = '{}{}.txt'.format(dir_path,f)
#             json_path = '{}{}.json'.format(dir_path,f)
#             mad_file = '{}{}_{}.gv'.format(ind_path,d,f)
#             # get process description
#             with open(mad_file,'r') as mad:
#                 lines = mad.readlines()
#                 process_desc = []
#                 for l in range(0, len(lines)):
#                     line = lines[l]
#                     if 'fontsize=15' in line:
#                         while lines[l+1].strip() != '"':
#                             process_desc.append(lines[l+1].strip())
#                             l = l + 1
#                 #TODO: save file to a folder, even if folder does not exist
#                 #description = ' '.join(process_desc)
#                 #with open(desc_path, 'w') as final:
#                 #    final.write(description)
#             # convert dot model to json
#             generated = open(mad_file).read()
#             minimal_json = mad_to_json(generated)
#             minimal_json = json.loads(minimal_json)
#             with open(json_path, "w") as final:
#                 json.dump(minimal_json, final, indent=4)

target_path = '../MAD-150/'
mypath = '../../TUM/data-sets/'
with open('{}smallMAD.json'.format(mypath), 'r') as json_file:
    data = json.load(json_file)
    for d in data:
        file_list = data[d]
        ind_path = '{}mad/test_dataset/{}/'.format(mypath,d)
        for f in file_list:
            desc_path = '{}process_descriptions/{}_{}.txt'.format(target_path,d,f)
            json_path = '{}ground_json/{}_{}.json'.format(target_path,d,f)
            mad_file = '{}{}_{}.gv'.format(ind_path,d,f)
            # get process description
            with open(mad_file,'r') as mad:
                lines = mad.readlines()
                process_desc = []
                for l in range(0, len(lines)):
                    line = lines[l]
                    if 'fontsize=15' in line:
                        while lines[l+1].strip() != '"':
                            process_desc.append(lines[l+1].strip())
                            l = l + 1
                #TODO: save file to a folder, even if folder does not exist
                description = ' '.join(process_desc)
                with open(desc_path, 'w') as final:
                    final.write(description)
            # convert dot model to json
            generated = open(mad_file).read()
            minimal_json = mad_to_json(generated)
            minimal_json = json.loads(minimal_json)
            with open(json_path, "w") as final:
                json.dump(minimal_json, final, indent=4)

