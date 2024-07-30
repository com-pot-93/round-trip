# round-trip
Info: Pipeline (m2t,t2m) for roundtriping with LLMs

<h1> Data Sets [data/] </h1>

[Pet Data Set](https://huggingface.co/datasets/patriziobellan/PET) </br>
* **data/pet/process\_descriptions**: textual descriptions for 7 selected examples from PET data set
* **data/pet/bpmn-xml**:             models in BPMN2.0 format with process descriptions
* **data/pet/mermaid**:              models in mermaid.js format associated with process descriptions
* **data/pet/generated_mermaid**:              models in mermaid.js format generated for process descriptions
* **data/pet/generated_json**:              models in json format generated for process descriptions

[Internal Uni Data Set](https://zenodo.org/records/7783492) </br>
* **source/inter/bpmn-xml**:              multiple models in BPMN2.0 format with process descriptions
* **source/inter/process\_descriptions**: textual process descriptions

<h1> Pipeline Implementation [source/] </h1>

* **source**:
    * *docu.md*:                        documentation

* **source/llm\_connect**:
    * *ask\_open\_ai.py*:               interface to communicate with llms
* **source/m2t**:
    * *create\_descriptions.py*:        convert mermaid.js models into textual process descriptions
* **source/t2m**:
    * *prompt\_engineering.py*:         custom rules for mermaid.js output format
    * *create\_model.py*:               convert textual process descriptions into mermaid.js process models
* **source/merson**:
    * *merson\_converter.py*:           conver mermaid.js into bpmn.json
* **source/model_info**:
    * *get\_information.py*:            validate mermaid.js models, extract tasks, .etc

<h1> Virtual Environment </h1>

* **Pipfile, Pipfile.lock**: virtual environment
* **.env**: environmental variables
    * $\color{VioletRed}{\textsf{OPENAI\\_API\\_KEY}}$: add your openai key

<h1> Execution </h1>

* **examples.py**: some examples to test the funtionality

1. clone the repo
   - `git clone <repo_name>`
3. navigate to the round-trip directory
4. set $\color{VioletRed}{\textsf{OPENAI\\_API\\_KEY}}$
5. create virtual environment
   - `pipenv install`
7. install all required libraries
   - `pipenv install -r requirements.txt`
9. start the environment
    - `pipenv shell`
11. execute your python scripth
    - `python <file\_name.py>`




