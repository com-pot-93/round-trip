from source.llm_connect.ask_open_ai import ask_gpt

""" prompt for process description generation """
def create_prompt(process_model,graph_type="mermaid.js",elref=1):
    if elref == 0:
        prompt = "Read this {} model: {}. Convert this model to a textual process description using simple natural language. Return only text summary".format(graph_type,process_model)
    else:
        prompt = "Read this {} model: {}. Convert this model to a textual process description using simple natural language without mentioning types of the model elements (i.e., task, startevent, endevent,gateway, etc.). Return only text summary".format(graph_type,process_model)
    return prompt

def generate_description(model,process_model,graph_type="mermaid.js",elref=1):
    try:
        prompt = create_prompt(process_model,graph_type,elref)
        response = ask_gpt(model,prompt)
        return response
    except Exception as e:
        return e
