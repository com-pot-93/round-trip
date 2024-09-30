import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

main_directory = "experiment/pipe2"
dir_list = os.listdir(main_directory)
for folder_name in dir_list:
    print("-------{}--------".format(folder_name))
    sub_dir = '{}/{}/'.format(main_directory,folder_name)
    excel_data = '{}evaluation_overall.xlsx'.format(sub_dir)

# read data
    text_data = pd.read_excel(excel_data, 't2t')
    model_data = pd.read_excel(excel_data, 'm2m')

# all model columns: similarity    recall  precision
# all text columns : similarity  recall  precision  sequence_similarity   recall2  precision2  overall_sim

    model_sim = model_data['similarity']
    sim = text_data['similarity']
    seq_sim = text_data['sequence_similarity']
    overall_sim = text_data['overall_sim']

# plot data
    plt.figure(figsize=(16,12), dpi =500)
    plt.scatter(model_sim, sim, label = "sim")
    plt.scatter(model_sim, seq_sim, label = "seq_sim")
    plt.scatter(model_sim, overall_sim, label = "overall_sim")
    plt.legend()
    plt.savefig('{}scatter_plot.pdf'.format(sub_dir))

# calculate correlation
    data = [model_sim, sim, seq_sim, overall_sim]
    sim_df = pd.DataFrame(data)
    sim_df = sim_df.transpose()
    corr = sim_df.corr(method = 'pearson')

#plot correlation matrix
    ticks = ["model_sim","sim","seq_sim","overall_sim"]
    plt.figure(figsize=(16,12), dpi =500)
    sns.heatmap(corr,annot=True,yticklabels=ticks,xticklabels=ticks)
    plt.yticks(rotation=0)
    plt.savefig('{}correlation_plot.pdf'.format(sub_dir))
