import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import numpy as np

llm = 'gpt'
#llm = 'gemini'
path = '../llm-round-trip-correctness/results/'
file_name = '{}_mad_m2m.csv'.format(llm)
file_name = '{}_mad_t2t.csv'.format(llm)
#file_name = '{}_real_setm2m.csv'.format(llm)

csv_file = pd.read_csv('{}{}'.format(path,file_name))
#csv_file['model_name'] = csv_file['model_name'].str.extract(r'^(.*?)_\d*.json')
csv_file['model_name'] = csv_file['model_name'].str.extract(r'^(.*?)_\d*.txt')
csv_file['model_name'] = csv_file['model_name'].str.replace('_','\n')

colours = [['#8ff0a4','#26a269'],['#99c1f1','#1a5fb4']]
#colours = [['#8ff0a4','#26a269'],['#99c1f1','#1a5fb4'],['#ffa8db','#f35eb5'],['#dc8add','#813d9c']]
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
    print(collist)
    #collist = list(map(float, collist))
    mymean = np.nanmean(collist)
    print(mymean)

    palette = sns.blend_palette(colours[c], n_colors=15)
    plt.figure(figsize=(18, 14))
    ax = sns.boxplot(data=df, palette=palette)
    ax = sns.swarmplot(data=df, color="black", size = 6)
    plt.axhline(mymean, c='#cb4335', linestyle='--', linewidth = 1, label=f'Mean: {mymean:.2f}')
    plt.legend()
    plt.ylim(0.4, 1)

    plt.rcParams["figure.dpi"] = 300
    plt.xlabel("Domains", size=12)
    plt.xticks(fontsize=8)
    plt.ylabel('pics/{} - {}'.format(names[c],llm.upper()), size=12)
    plt.margins(0.05)
    plt.savefig('pics/{} - {} - mad.png'.format(names[c],llm.upper()))
    plt.savefig('pics/{} - {} - mad.pdf'.format(names[c],llm.upper()))


