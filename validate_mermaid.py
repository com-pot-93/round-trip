from source.merson.merson_converter import mermaid_to_json
import json
import os

mermaid = open('examples/errors/mg_1_1.txt','r').read()



json_model = mermaid_to_json(mermaid)
print(json_model)


# # # Import module
# #
# # # Assign directory
directory = "/home/i17/projects/SAP/round-trip/data/pet/generated_mermaid"
target_directory = "/home/i17/projects/SAP/round-trip/data/pet/generated_json"
# Iterate over files in directory
for path, folders, files in os.walk(directory):
    if files:
        sub = path.split("/")[-1]
        print(sub)
        os.makedirs(os.path.join(target_directory,sub), exist_ok=True)
        for file_name in files:
            f = os.path.join(path, file_name)
            mermaid = open(f,'r').read()
            json_model = mermaid_to_json(mermaid)
            target_file = os.path.join(target_directory,sub,file_name)
            with open(target_file, 'w') as f:
                json.dump(json_model, f)
























