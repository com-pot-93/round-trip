import os, sys
import json
import logging
import argparse
import csv

sys.path.append("./data/")
sys.path.append("./model_evaluation")
sys.path.append("./round_trip")

import bpmn_similarity
from text_evaluation import text_similarity

from round_trip.t2m.prompt_engineering import json_desc
from round_trip.llm_connect.gen_ai_llm_call import generate_gpt_with_timeout
from round_trip.m2t.create_description import generate_prompt_gpt as generate_prompt_gpt_m2t
from round_trip.t2m.create_model import generate_prompt_gpt as generate_prompt_gpt_t2m

from round_trip.llm_connect.gen_ai_llm_call import generate_gemini_with_timeout
from round_trip.m2t.create_description import generate_prompt_gemini as generate_prompt_gemini_m2t
from round_trip.t2m.create_model import generate_prompt_gemini as generate_prompt_gemini_t2m


class Prompt:
    def __init__(self, llm, path_to_json, path_to_text, json_desc,temp_in,temp_out):
        self.temp_in = temp_in
        self.temp_out = temp_out
        if llm == 'gemini':
            self.system_prompt_gemini_t2m, self.examples_t2m = generate_prompt_gemini_t2m(path_to_json, path_to_text, json_desc)
            self.system_prompt_gemini_m2t, self.examples_m2t = generate_prompt_gemini_m2t(path_to_json, path_to_text)
        elif llm == 'gpt':
            self.system_prompt_t2m, self.user_prompt_t2m, self.assistant_prompt_t2m = generate_prompt_gpt_t2m(path_to_json, path_to_text, json_desc)
            self.system_prompt_m2t, self.user_prompt_m2t, self.assistant_prompt_m2t = generate_prompt_gpt_m2t(path_to_json, path_to_text)

def generate_artefacts_with_gemini(prompt, direction, model, description):
    gen_text = ''
    gen_model = ''
    if direction == 'm2m':
        gen_text = generate_gemini_with_timeout(
            prompt.system_prompt_gemini_m2t,
            prompt.examples_m2t,
            "Here is the model: " + str(model),
            prompt.temp_in,
            response_format=False
        )

        if gen_text:
            gen_model = generate_gemini_with_timeout(
                prompt.system_prompt_gemini_t2m,
                prompt.examples_t2m,
                "Here is the textual description: " + gen_text,
                prompt.temp_out,
                response_format=True
            )
    elif direction == 't2t':
        gen_model = generate_gemini_with_timeout(
            prompt.system_prompt_gemini_t2m,
            prompt.examples_t2m,
            "Here is the texual description: " + str(description),
            prompt.temp_in,
            response_format=True
        )

        if gen_model:
            gen_text = generate_gemini_with_timeout(
                prompt.system_prompt_gemini_m2t,
                prompt.examples_m2t,
                "Here is the model: " + str(gen_model),
                prompt.temp_out,
                response_format=False
            )
    return gen_text, gen_model

def generate_artefacts_with_gpt(prompt, direction, model, description):
    gen_text = ''
    gen_model = ''
    if direction == 'm2m':
        gen_text = generate_gpt_with_timeout(
            prompt.system_prompt_m2t,
            prompt.user_prompt_m2t,
            prompt.assistant_prompt_m2t,
            "Here is the model: " + str(model),
            prompt.temp_in,
            response_format=False
        )
        if gen_text:
            gen_model = generate_gpt_with_timeout(
                prompt.system_prompt_t2m,
                prompt.user_prompt_t2m,
                prompt.assistant_prompt_t2m,
                "Here is the textual description: " + gen_text,
                prompt.temp_out,
                response_format=True
            )
    elif direction == 't2t':
        gen_model = generate_gpt_with_timeout(
            prompt.system_prompt_t2m,
            prompt.user_prompt_t2m,
            prompt.assistant_prompt_t2m,
            "Here is the texual description: " + str(description),
            prompt.temp_in,
            response_format=True
        )
        if gen_model:
            gen_text = generate_gpt_with_timeout(
                prompt.system_prompt_m2t,
                prompt.user_prompt_m2t,
                prompt.assistant_prompt_m2t,
                "Here is the model: " + str(gen_model),
                prompt.temp_out,
                response_format=False
            )
    return gen_text, gen_model



def main_pipeline(llm):
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger("{}Logger".format(llm.upper()))
    path_to_json = "./data/prompt_ex_json_pet.json"
    path_to_text = "./data/prompt_ex_text_pet.txt"


    temp_in = 1
    temp_out = 0
    direction = 'm2m'
    model = "This is the model"
    description = "Tis is the text"

    if llm == 'gpt':
        print("================================GPT=============================")
        gpt_prompt = Prompt(llm, path_to_json, path_to_text, json_desc, temp_in,temp_out)
        print("================================M2T=============================")
        #print('system prompt: ',gpt_prompt.system_prompt_m2t)
        #print('user prompt: ', gpt_prompt.user_prompt_m2t)
        #print('assistant prompt: ', gpt_prompt.assistant_prompt_m2t)
        #print("================================T2M=============================")
        #print(gpt_prompt.system_prompt_t2m, gpt_prompt.user_prompt_t2m, gpt_prompt.assistant_prompt_t2m)
        gen_text, gen_model = generate_artefacts_with_gpt(gpt_prompt, direction, model, description)
    elif llm == 'gemini':
        print("================================Gemini=============================")
        gemini_prompt = Prompt(llm, path_to_json, path_to_text, json_desc, temp_in,temp_out)
        print("================================M2T=============================")
        #print(gemini_prompt.system_prompt_gemini_m2t,gemini_prompt.examples_m2t)
        #print("================================T2M=============================")
        #print(gemini_prompt.system_prompt_gemini_t2m,gemini_prompt.examples_t2m)
        gen_text, gen_model = generate_artefacts_with_gemini(gemini_prompt, direction, model, description)

    direction = 't2t'
    if llm == 'gpt':
        print("================================GPT=============================")
        gpt_prompt = Prompt(llm, path_to_json, path_to_text, json_desc, temp_in,temp_out)
        print("================================T2M=============================")
        gen_text, gen_model = generate_artefacts_with_gpt(gpt_prompt, direction, model, description)
    elif llm == 'gemini':
        print("================================Gemini=============================")
        gemini_prompt = Prompt(llm, path_to_json, path_to_text, json_desc, temp_in,temp_out)
        print("================================T2M=============================")
        gen_text, gen_model = generate_artefacts_with_gemini(gemini_prompt, direction, model, description)



if __name__ == "__main__":
    llm = 'gpt'
    main_pipeline('gpt')
    main_pipeline('gemini')

