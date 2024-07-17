# round-trip
prepare pipeline (m2t,t2m) for roundtriping with LLMs

data-sets (data/):
    Pet Data Set [ADD LINK]
        data/pet/process\_descriptions: textual descriptions for 7 selected examples from PET data set
        data/pet/bpmn-xml:             models in BPMN2.0 format with process descriptions
        data/pet/mermaid:              models in mermaid.js format associated with process descriptions

    Internal Uni Data Set [ADD ZOTTERO]
        source/inter/bpmn-xml:              multiple models in BPMN2.0 format with process descriptions
        source/inter/process\_descriptions: textual process descriptions

code (source/):
    source/llm\_connect
        ask\_open\_ai.py:               interface to communicate with llms
        docs.txt:                       info about supported models
    source/m2t
        create\_descriptions.py:        convert mermaid.js models into textual process descriptions
    source/t2m
        prompt\_engineering.py:         custom rules for mermaid.js output format
        create\_model.py:               convert textual process descriptions into mermaid.js process models
    source/merson
        merson\_converter.py:            conver mermaid.js into bpmn.json

Pipfile, Pipfile.lock: virtual environment
.env: environmental variables
    OPENAI\_API\_KEY: add your openai key

examples.py: some examples to test the funtionality
