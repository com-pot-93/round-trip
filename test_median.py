import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import numpy as np

llm = 'gpt'
llm = 'gemini'
path = '../llm-round-trip-correctness/results/'
file_name = '{}_mad_m2m.csv'.format(llm)
#file_name = '{}_madt2t.csv'.format(llm)
#file_name = '{}_real_setm2m.csv'.format(llm)

csv_file = pd.read_csv('{}{}'.format(path,file_name))
csv_file['model_name'] = csv_file['model_name'].str.extract(r'^(.*?)_\d*.json')
csv_file['model_name'] = csv_file['model_name'].str.replace('_','\n')

#colours = [['#8ff0a4','#26a269'],['#99c1f1','#1a5fb4'],['#ffa8db','#f35eb5'],['#dc8add','#813d9c']]
colours = [['#99c1f1','#1a5fb4'],['#dc8add','#813d9c']]
if 'm2m' in file_name:
    columns = ['m2m_eval_1','m2m_eval_2']
    names = ['Model Similarity Scores (1)','Model Similarity Scores (2)']
else:
    columns = ['t2t_eval_1','t2t_eval_2']
    names = ['Text Similarity Score (1)','Text Similarity Scores (2)']

for c in range(0,len(columns)):
    t2t_eval_1 = csv_file[['model_name', columns[c]]]
    final = t2t_eval_1.groupby('model_name')
    df = pd.DataFrame()
    for key, item in final:
        temp = final.get_group(key).reset_index()
        df[key] = temp[columns[c]]

    collist = csv_file[columns[c]].tolist()
    mymean = np.mean(collist)
    allmean = df.mean()
    for a in allmean:
        print(a)
    plt.plot(allmean, linestyle = 'dotted')
    plt.show()
    #plt.savefig('pics/{} - {} - mad.png'.format(names[c],llm.upper()))
    #plt.savefig('pics/{} - {} - mad.pdf'.format(names[c],llm.upper()))


