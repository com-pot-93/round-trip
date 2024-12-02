from datasets import load_dataset
import pandas as pd
import numpy as np

pet = pd.read_parquet('data/raw_pet/test-00000-of-00001-4cd746ae057084a3.parquet')
print(pet)

for index, p in pet.iterrows():
    print("------------------------------------")
    print(p['document name'])
    relations = p['relations']['relation-type']
    text = p['tokens']
    tags = p['ner_tags']
    sentences = p['sentence-IDs']
    maxi = max(sentences) + 1
    print(' '.join(text))
    sentence_dictionary = {}

    for i in range(0,maxi):
        print('sentence ',i)
        inds = [u for u, e in enumerate(sentences) if e == i]
        current = text[inds[0]:inds[-1]]
        cur_tags = tags[inds[0]:inds[-1]]
        print(' '.join(current))
        print(cur_tags)
        if i not in sentence_dictionary:
            sentence_dictionary[i] = current
    for r in range(0,len(relations)):
        rel = relations[r]
        ssentID = p['relations']['source-head-sentence-ID'][r]
        swordID = p['relations']['source-head-word-ID'][r]
        tsentID = p['relations']['target-head-sentence-ID'][r]
        twordID = p['relations']['target-head-word-ID'][r]
        source = sentence_dictionary[ssentID][swordID]
        target = sentence_dictionary[tsentID][twordID]
        try:
            target1 = sentence_dictionary[tsentID][twordID+1]
            print(rel,": ",source,target,target1)
        except:
            print(rel,": ",source,target)







#for p in pet:
#    print(p)
    #print(p[0])
    #sentences = p['sentence-IDs']
    #print(sentences)
    #maxi = max(sentences)
    #for i in range(0,maxi):
    #    print(i)

## initialize lists
#test_list1 = ["a", "b", "c", "d","b","b"]
#test_list2 = ["b"]

# printing original lists
#print("The original list 1 : " + str(test_list1))
#print("The original list 2 : " + str(test_list2))

#res = [i for i, e in enumerate(test_list1) if e == 'b']
#print(res)
