import os, sys, json

from text_evaluation.text_similarity import split_into_sentences,get_sentences

sys.path.append("src/")
sys.path.append("data/")
sys.path.append("model_evaluation")
sys.path.append("model_evaluation/evaluation")

path_to_text = "examples/punktuation.txt"

with open(path_to_text, "r") as file:
        file_1 = file.read()

print(len(file_1))


sentences_1 = get_sentences(file_1)
print(sentences_1)
print(len(sentences_1))


sentences_2 = split_into_sentences(file_1)
print(sentences_2)
print(len(sentences_2))

