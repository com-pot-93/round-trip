import os
import re

files = []
grep_command = "grep '\"en\"' *.meta.json | grep bpmn20"
result = subprocess.run(grep_command, capture_output=True, text=True, shell=True)
lines = result.stdout.splitlines()
for l in lines:
    file_id = re.findall("^\d*[^.meta]", txt)[0]
    files.append(file.id)
