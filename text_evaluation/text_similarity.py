from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

def get_cosine(text1,text2):
    corpus = [text1,text2]
    vectorizer = TfidfVectorizer()
    trsfm=vectorizer.fit_transform(corpus)
    cos_sim = cosine_similarity(trsfm[0:1], trsfm)
    cos_sim = cos_sim[0][1]
    cos_sim = round(cos_sim, 2)
    return cos_sim

model = SentenceTransformer('sentence-transformers/stsb-mpnet-base-v2')
def sts_bert(t1,t2):
    sentences = [t1, t2]
    embedding_1= model.encode(sentences[0], convert_to_tensor=True)
    embedding_2 = model.encode(sentences[1], convert_to_tensor=True)
    score = util.pytorch_cos_sim(embedding_1, embedding_2)
    score = score.tolist()
    score = round(score[0][0], 2)
    return score
