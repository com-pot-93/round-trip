from src.t2m.prompt_engineering import mermaid, graphviz
from src.llm_connect.ask_open_ai import ask_gpt

""" prompt for model generation """
def create_prompt(description,set_of_rules,graph_type="mermaid.js"):
    prompt = "Process description: {}. {}. Considering provided process description and a set of custom rules create a valid {} graph.".format(description,set_of_rules,graph_type)
    prompt += "Only a valid graph without any additional text or information must be returned."
    if graph_type == "mermaid.js":
        prompt += "It is also prohibeted to return mermaid diagram with ```mermaid ``` notation!!!"
    return prompt

""" call llm to generate model """
def generate_model(model,description,graph_type="mermaid.js"):
    try:
        if "mermaid" in graph_type:
            set_of_rules = mermaid
        else:
            set_of_rules = graphviz
        prompt = create_prompt(description,set_of_rules,graph_type)
        response = ask_gpt(model,prompt)
        if "```mermaid" in response:
            response = response[response.find('\n')+1:response.rfind('\n')]
        return response
    except Exception as e:
        return e


