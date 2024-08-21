from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import re
import numpy as np

model = SentenceTransformer('sentence-transformers/stsb-mpnet-base-v2')

""" this function returns the cosine similarity betweeen 2 documents using TF-IDF """
def get_cosine(text1,text2):
    corpus = [text1,text2]
    vectorizer = TfidfVectorizer()
    trsfm=vectorizer.fit_transform(corpus)
    cos_sim = cosine_similarity(trsfm[0:1], trsfm)
    cos_sim = cos_sim[0][1]
    cos_sim = round(cos_sim, 2)
    return cos_sim

""" this function returns the cosine similarity betweeen 2 documents using pre-trained BERT model """
def sts_bert(t1,t2):
    sentences = [t1, t2]
    embedding_1= model.encode(sentences[0], convert_to_tensor=True)
    embedding_2 = model.encode(sentences[1], convert_to_tensor=True)
    score = util.pytorch_cos_sim(embedding_1, embedding_2)
    score = score.tolist()
    score = round(score[0][0], 2)
    return score

""" this function splits plain text into array of sentences """
def split_into_sentences(paragraph):
    sentence_endings = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
    sentences = re.split(sentence_endings, paragraph)
    return sentences

""" this function splits string into array of sentences and removes spaces/new lines """
def split_and_clean(text):
    clean_sentences = []
    sentences = split_into_sentences(text)
    for s in sentences:
        if s != "" and s!="\n":
            clean_sentences.append(s)
    return clean_sentences

""" this function genertes similarity matrix betweeen two arrays of sentences: list1 - original, list2 - generated """
""" sim_type : cos or bert """
def create_matrix(list1,list2,sim_type):
    final = []
    for l in list1:
        row = []
        for ll in list2:
            if sim_type == "cos":
                val = get_cosine(l,ll)
            else:
                val = sts_bert(l,ll)
            row.append(val)
        final.append(row)
    new = pd.DataFrame(final)
    return new

""" this function returns only matrix values greater than threshold and their indexes """
def find_match(matrix,thold):
    new_matrix = matrix.drop(columns=[col for col in matrix if (matrix[col] <= thold).all()])
    clean_matrix = new_matrix.drop(index=[index for index, row in new_matrix.iterrows() if (row <= thold).all()])
    over_thold = clean_matrix.idxmax()
    return over_thold

""" this function calculates recall """
def find_recall(matrix,thold):
    shape = matrix.shape
    # get the number of sentences in original text
    all_orig = shape[0]
    matches = find_match(matrix,thold)
    columns = list(matches)
    # get number of sentences in original text that are also present in generated text
    match_orig = len(list(dict.fromkeys(columns)))
    recall = round(match_orig/all_orig,2)
    return recall

""" this function calculates precision """
def find_precision(matrix,thold):
    shape = matrix.shape
    all_gen = shape[1]
    matches = find_match(matrix,thold)
    indexes = list(matches.index)
    match_gen = len(list(dict.fromkeys(indexes)))
    precision = round(match_gen/all_gen,2)
    return precision

""" this function takes two texts as input and return precision and recall: text1 - original, text2 - generated """
def get_kpis(text1,text2,sim_type="cos"):
    list1 = split_and_clean(text1)
    list2 = split_and_clean(text2)
    matrix = create_matrix(list1,list2,sim_type)
    if sim_type == "cos":
        thold = 0.2
    else:
        thold = 0.5
    recall = find_recall(matrix,thold)
    precision = find_precision(matrix,thold)
    return recall, precision






