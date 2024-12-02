import os
import re
import pandas as pd
import json

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

ids = {}
# create lists of ids for mad data set
df = pd.read_excel(excel_file, None)
sheet_names = list(df.keys())
for sheet in sheet_names:
    df_sheet = pd.read_excel(excel_file, sheet_name=sheet)
    df_sheet = df_sheet.dropna()
    #myids  = df_sheet[0].dropna()
    myids = df_sheet[0]
    myids = myids.astype(int)
    myids = myids.tolist()
    myids = sorted(myids)
    ids[sheet] = myids

with open("smallMAD.json", "w") as json_file:
    json.dump(ids, json_file, indent=4)
    #for index, row in df_sheet.iterrows():
    #    print(row['status'], row[0])


