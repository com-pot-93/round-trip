import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
import seaborn as sns
import os
import numpy as np


def call_regression(x,y):
    reshape_x = np.array(x).reshape((-1, 1))
    reshape_y = np.array(y)
    predictor = LinearRegression()
    predictor.fit(reshape_x,reshape_y)
    expected_sim = predictor.predict(reshape_x)
    return expected_sim


main_directory = "experiment/pipe1"
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

# # plot data
#     plt.figure(figsize=(16,12), dpi =500)
#     plt.scatter(model_sim, sim, label = "sim")
#     plt.scatter(model_sim, seq_sim, label = "seq_sim")
#     plt.scatter(model_sim, overall_sim, label = "overall_sim")
#     plt.legend()
#     plt.savefig('{}scatter_plot.pdf'.format(sub_dir))

# calculate correlation
#    data = [model_sim, sim, seq_sim, overall_sim]
#    sim_df = pd.DataFrame(data)
#    sim_df = sim_df.transpose()
#    corr = sim_df.corr(method = 'pearson')
##    corr = sim_df.corr(method = 'kendall')
#    corr = sim_df.corr(method = 'spearman')

# plot correlation matrix
#    ticks = ["model_sim","sim","seq_sim","overall_sim"]
#    plt.figure(figsize=(16,12), dpi =500)
#    sns.heatmap(corr,annot=True,yticklabels=ticks,xticklabels=ticks)
#    plt.yticks(rotation=0)
#    plt.savefig('{}kendall_correlation_plot.pdf'.format(sub_dir))

#    fig = plt.figure(figsize =(16, 12))
#    ax = fig.add_axes([0, 0, 1, 1])
#    bp = ax.boxplot(data)
#    plt.show()

# linear regression
    fig = plt.figure()
    expected_sim = call_regression(model_sim,sim)
    ax1 = fig.add_subplot(131)
    ax1.scatter(model_sim,sim)
    ax1.scatter(model_sim,expected_sim, c='Red')
#    ax1.title('Text similarity vs. Model Similarity')
#    ax1.xlabel('Model Similarity')
#    ax1.ylabel('Text Similarity')

    expected_seq_sim = call_regression(model_sim,seq_sim)
    ax2 = fig.add_subplot(132)
    ax2.scatter(model_sim,seq_sim)
    ax2.scatter(model_sim,expected_seq_sim, c='Red')
#    ax2.title('Text similarity vs. Model Similarity')
#    ax2.xlabel('Model Similarity')
#    ax2.ylabel('Text Similarity')

    expected_over_sim = call_regression(model_sim,overall_sim)
    ax3 = fig.add_subplot(133)
    ax3.scatter(model_sim,overall_sim)
    ax3.scatter(model_sim,expected_over_sim, c='Red')
#    ax3.title('Text similarity vs. Model Similarity')
#    ax3.xlabel('Model Similarity')
#    ax3.ylabel('Text Similarity')

    plt.savefig('{}regression.pdf'.format(sub_dir))


