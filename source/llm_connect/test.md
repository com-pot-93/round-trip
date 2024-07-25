<h1> llm_connect [source/llm_connect] </h1>

llm_connect is a folder to provide multiple interfaces to communicate with different LLMs. 
Currently only interface to Open AI models is provided. 

<h2> OPEN AI [source/llm_connect/ask_open_ai.py] </h2>

Import package: `from source.llm_connect.ask_open_ai import <function_name>`

All **'davinci'** models are now replaced through **'gpt-3.5-turbo-instruct'**. 
See https://platform.openai.com/docs/deprecations for more details.

**'gpt-3.5-turbo-instruct'** can be executed with *'completions'* api.

Newly released models can be accessed with *'chat.completions'* api. See https://platform.openai.com/docs/models for more details.

* To make a call to OpenAI model use 
`ask_gpt(llm_model,prompt)`, where: 
  * llm_model: *string* : llm model name ("gpt-4", "gpt-3.5-turbo", etc.) 
  * prompt: *string* : your prompt

<h1> t2m  [source/t2m/] </h1>

<h2> Model Generation [source/t2m/create_model] </h2>

Import package: `from source.t2m.create_model import <function_name>`

<h3> Functions: </h3>

* To generate new mermaid.js model based on provided textual description use</br>
`generate_model(llm_model,description)`, where:
  * llm_model: *string* : llm model name ("gpt-4", "gpt-3.5-turbo", etc.) 
  * description: *string* : textual process description </br>
  
  **Function returns**: 
  * mermaid_model: *string* : generated mermaid.js process model 

* To validate whether newly generated mermaid.js model conforms to the Mermaid.js specificatio use</br>
`validate_mermaid(mermaid_model)`, where:
  * mermaid_model: *string* : generated mermaid.js process model
  
  **Function returns**: 
  * status: *int* : validation status of generated model (1 - correct, 0 - not correct)  

* To validate whether newly generated mermaid.js model conforms customly predefined output format use</br>
`validate_custom_format(mermaid_model)`, where:
  * mermaid_model: *string* : generated process mermaid.js model
  
  **Function returns**: 
  * status: *int* : validation status of generated model (1 - correct, 0 - not correct)
  * errors: *array*: list of errors that were found during validation

* To extract the list of tasks from generated model use</br>
`extract_mermaid_tasks(mermaid_model)`, where:
  * mermaid_model: *string* : generated mermaid.js process model
  
  **Function returns**: 
  * task\_list: *array*: list of tasks from generated mermaid.js model

<h2> Prompt Engineering [source/t2m/prompt_engineering] </h2>

File contains suplimentary material (i.e., rules for predefined output format for different model types) that is required for proper prompt engineering to be able to generate models. 

<h1> m2t [source/m2t/] </h1>

<h2> Process Description Generation [source/t2m/create_description] </h2>

Import package: `from source.m2t.create_description import <function_name>`

<h3> Functions: </h3>

* To generate new textual process description based on provided mermaid.js process model use</br>
`generate_description(llm_model,mermaid_model)`, where:
  * llm_model: *string* : llm model name ("gpt-4", "gpt-3.5-turbo", etc.) 
  * mermaid_model: *string* : mermaid.js process model
  
  **Function returns**: 
  * description: *string* : textual process description </br>

<h1> merson [source/merson/] </h1>

<h2> Mermaid.js-BPMN.json Convertor [source/merson/merson_converter] </h2>

Import package: `from source.merson.merson_converter import <function_name>`

<h3> Functions: </h3>

* To convert mermaid.js process model into BPMN.json format use</br>
`mermaid_to_json(mermaid_model)`, where:
  * mermaid_model: *string* : generated mermaid.js process model
  
  **Function returns**: 
  * json_model: *string* : BPMN.json model

* To convert BPMN.json into mermaid.js process model use</br>
`json_to_mermaid(json_model)`, where:
  * json_model: *dict* : BPMN.json model
  
  **Function returns**: 
  * mermaid_model: *string* : generated mermaid.js process model
