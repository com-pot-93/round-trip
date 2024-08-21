from text_evaluation.text_similarity import get_cosine, sts_bert, get_kpis

text1 = """After a claim is registered , it is examined by a claims officer .
The claims officer then writes a settlement recommendation .
This recommendation is then checked by a senior claims officer who may mark the claim as OK or Not OK .
If the claim is marked as Not OK , it is sent back to the claims officer and the recommendation is repeated .
If the claim is OK , the claim handling process proceeds ."""

text2 = """The process begins with the claims officer registering the claim. After registration, the claims officer examines the claim. Following the examination, there are two possible paths.
In one path, the claims officer writes a settlement recommendation. This recommendation is then checked by a senior claims officer. After checking, the senior claims officer marks the claim. If the marking is okay, the claim handling process proceeds and the process ends.
In the other path, if the marking is not okay, the senior claims officer sends the recommendation back. This leads back to the point where the claims officer writes a settlement recommendation, and the process repeats from there.
"""

sim_score = get_cosine(text1,text2)
sim_score_2 = sts_bert(text1,text2)

print(sim_score,sim_score_2)

values_cos = get_kpis(text1,text2,"cos")
values_bert = get_kpis(text1,text2,"bert")
print(values_cos)
print(values_bert)

