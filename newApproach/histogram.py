import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os
from collections import defaultdict
import sys
import seaborn as sb
import re
import math


def plotHopsSB( xlabel):
    fig, axes = plt.subplots(1, 2, sharex=True, sharey=True,figsize=(9, 4))
   
    sb.set_style("white")
    sb.set_context(font_scale = 1.5, rc={"grid.linewidth": 5})
    
    finall = [[0.65, 0.6483928571428571, 0.6112202380952381, 0.5835912698412697, 0.5733184523809524, 0.65, 0.7274999999999999, 0.6641964285714285, 0.6438690476190475, 0.6316517857142856, 0.65, 0.7224999999999999, 0.6825, 0.6525, 0.6541071428571429, 0.65, 0.7224999999999999, 0.6783333333333333, 0.6633333333333333, 0.66625, 0.59375, 0.4973214285714286, 0.4999702380952381, 0.49609126984126983, 0.5330505952380953],
    [1.0, 0.8, 0.8, 0.8333333333333334, 0.825, 1.0, 0.8, 0.8, 0.8333333333333334, 0.825, 1.0, 0.8, 0.85, 0.8666666666666667, 0.85, 1.0, 0.8, 0.85, 0.8666666666666667, 0.85, 0.75, 0.75, 0.8, 0.7, 0.7]]

    count = 0
    names = ['(a) D-MultiWoz', '(b) D-SGD']
    for scores in finall:
        y1_data = scores
        raw_data = {
        # cat:    A                  B                  C                    D
        'Top K Questions': ['1',   '5',          '10',         '15',           '20',
            '1', '5',          '10',         '15',           '20',
            '1', '5',          '10',         '15',           '20',
            '1', '5',          '10',         '15',           '20',
            '1', '5',          '10',         '15',           '20'],
        'GPT Score': y1_data,
        'category': ['Markov-based:  $ PR^{wd} = 0.25$', 'Markov-based:  $ PR^{wd} = 0.25$', 'Markov-based:  $ PR^{wd} = 0.25$', 'Markov-based:  $ PR^{wd} = 0.25$', 'Markov-based:  $ PR^{wd} = 0.25$',
        'Markov-based:  $ PR^{wd} = 0.5$', 'Markov-based:  $ PR^{wd} = 0.5$', 'Markov-based:  $ PR^{wd} = 0.5$', 'Markov-based:  $ PR^{wd} = 0.5$', 'Markov-based:  $ PR^{wd} = 0.5$',
        'Markov-based:  $ PR^{wd} = 0.75$', 'Markov-based:  $ PR^{wd} = 0.75$', 'Markov-based:  $ PR^{wd} = 0.75$', 'Markov-based:  $ PR^{wd} = 0.75$', 'Markov-based:  $ PR^{wd} = 0.75$',
        'Markov-based:  $ PR^{wd} = 0.9$', 'Markov-based:  $ PR^{wd} = 0.9$', 'Markov-based:  $ PR^{wd} = 0.9$', 'Markov-based:  $ PR^{wd} = 0.9$', 'Markov-based:  $ PR^{wd} = 0.9$',
            'Frequency-based', 'Frequency-based', 'Frequency-based', 'Frequency-based', 'Frequency-based']
            }
        #plt.gca().get_legend().remove()
        g =sb.barplot(x='Top K Questions', y='GPT Score',  hue= 'category', data=raw_data, palette = "muted", estimator = np.median,
            ax=axes[count])
        g.set_title(names[count], fontsize= 12)
        count +=1
        if count>1:
           g.legend(bbox_to_anchor=(0.66,1.15), fontsize='small', loc='upper left', borderaxespad=0)#, prop={'size':12})
        else:
            g.legend_.remove()
        
    plt.margins(x = 0.05) 
   
    plt.savefig(os.path.join('/Users/jannatarameem/Desktop/Fall23/OQS/ChatGPT/histogram/',  'GPT_Scores.pdf'), bbox_inches='tight')
    plt.show()



def main():
    plotHopsSB("# of Selected Top Questions")


# main()

def n2():
# Data for the pie charts
    data1 = [25, 30, 45]
    data2 = [15, 40, 45]
    data3 = [10, 20, 70]
    data4 = [40, 10, 50]
    data5 = [5, 25, 70]

    # Labels for each pie chart
    labels = ['Label 1', 'Label 2', 'Label 3']

    # Create subplots
    plt.figure(figsize=(15, 4))
    plt.subplots_adjust(wspace=0.05)

    # Subplot 1
    plt.subplot(1, 5, 1)
    plt.pie(data1, autopct='%1.1f%%', startangle=90)
    plt.title('Subplot 1')

    # Subplot 2
    plt.subplot(1, 5, 2)
    plt.pie(data2, autopct='%1.1f%%', startangle=90)
    plt.title('Subplot 2')

    # Subplot 3
    plt.subplot(1, 5, 3)
    plt.pie(data3, autopct='%1.1f%%', startangle=90)
    plt.title('Subplot 3')

    # Subplot 4
    plt.subplot(1, 5, 4)
    plt.pie(data4, autopct='%1.1f%%', startangle=90)
    plt.title('Subplot 4')

    # Subplot 5
    plt.subplot(1, 5, 5)
    plt.pie(data5,  autopct='%1.1f%%', startangle=90)
    plt.title('Subplot 5')

    # Adjust layout
    plt.tight_layout()
    plt.legend(labels)

    # Show the plots
    plt.show()

# n2()

def n3(data):
    labelsSGD = ['less likely', 'more likely']
    labelsMTZ = ['unlikely', 'somewhat likely', 'likely', 'very likely']
    # Create subplots with reduced wspace and hspace
    fig, axes = plt.subplots(2, 5, figsize=(15, 8), sharex=True, sharey=True)
    plt.subplots_adjust(wspace=0.01, hspace=0.01)  # Adjust the wspace and hspace parameters

    # Generate and plot data for each subplot
    for i in range(2):
        if i <1:
            key = 'MultiWoz'
            labels = labelsMTZ 
        else:
            key = 'SGD'
            labels = labelsSGD
        keys = list(data[key].keys())
        p=0
        for j in range(5):
            if i == 0:
                axes[i, j].pie(data[key][keys[p]][0], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired(np.arange(4)*4))
            else:
                axes[i, j].pie(data[key][keys[p]][0], autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1(np.arange(3)*4))
            s = keys[p]
            axes[i, j].set_title(f'{s}', fontsize='small' )
            if j == 4 and i== 0:
                axes[i, j].legend(labels, bbox_to_anchor=(1.34,1.3), fontsize='small')
            elif j == 4 and i== 1:
                axes[i, j].legend(labels, bbox_to_anchor=(1.1,1.3), fontsize='small')
            p+=1

    # Add captions for each row
    
    for i, row_caption in enumerate(['(a) D-MultiWoz: Top 10', '(b) D-SGD: Top 10']):
        axes[i, 0].text(5, -1.5, row_caption, fontsize=10, ha='center')

    plt.savefig(os.path.join('/Users/jannatarameem/Desktop/Fall23/OQS/ChatGPT/histogram/',  'GPT_PieCharts_Top10.pdf'), bbox_inches='tight')
    
    # plt.figure(figsize=(15, 4))
    # plt.subplots_adjust(wspace=0.01, hspace=0.05)  # Adjust the wspace and hspace parameters

    # # First row of subplots
    # k = [1,5,10,15,20]

    # p = 0

    # keys = list(data['MultiWoz'].keys())
    # print(keys)
    # for i in range(1, 6):
    #     plt.subplot(1, 5, i)
    #     plt.pie(data['MultiWoz'][keys[p]][1], autopct=lambda p: '{:.1f}%'.format(p), startangle=90, textprops={'fontsize': 'small'})
    #     plt.title(f'{keys[p]}', fontsize='small' )
    #     p+=1
    #     if i == 5:
    #         plt.legend(labelsMTZ, bbox_to_anchor=(1.2,1.1), fontsize='small')

    # plt.subplot(2, 5, 1)
    # plt.text(5, -1.5, '(a) D-MultiWoz: Top 20', fontsize=10, ha='center')

    # # Second row of subplots
    # p = 0
    # keys = list(data['SGD'].keys())
    # for i in range(6, 11):
    #     plt.subplot(2, 5, i)
    #     plt.pie(data['SGD'][keys[p]][1], autopct=lambda p: '{:.1f}'.format(p), startangle=90, textprops={'fontsize': 'small'})
    
    #     plt.title(f'{keys[p]}', fontsize='small' )
    #     p+=1
    #     if i == 10:
    #         plt.legend(labelsSGD, bbox_to_anchor=(1.4,1.6), fontsize='small')

    # # Add caption for the second row
    # plt.subplot(2, 5, 2)
    # plt.text(5, -1.5, '(b) D-SGD: Top 20', fontsize=10, ha='center')

    

    # Show the plots
    plt.show()

# n3()

################### SGD ##################

"""
'SGD':
{
'0.9':
[[5, 10],
[8, 17]],
'Frequency-based':
[[7, 9],
[15, 11]],
'PR25':[
[7, 9],
[10, 16]],
'PR75':[
[5, 10],
[8, 17]],
'PR50': [[7, 9], [10, 16]]
}
"""
# data1 = [5, 10]
# data2 = [8, 17]
# labels = ['less likely', 'more likely']

# # Create a figure with two subplots (1 row, 2 columns)
# fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# # Subplot 1
# axs[0].pie(data1, labels=labels, autopct='%1.1f%%', startangle=90)
# axs[0].set_title('D-SGD: Top 10')

# # Subplot 2
# axs[1].pie(data2, labels=labels, autopct='%1.1f%%', startangle=90)
# axs[1].set_title('D-SGD: Top 20')

# # Adjust layout
# plt.tight_layout()

# # Show the plot
# plt.show()




################ MultiWoz ##############

"""
'MultiWoz':
{
'PR90':[[0, 17, 13, 6],
[4, 33, 20, 13]],
'FR':[[15, 37, 11, 2],
[23, 62, 26, 5]],
'PR25':[[1, 39, 15, 5],
[17, 59, 27, 8]],
'PR75':
[[0, 17, 14, 6],
[4, 39, 22, 13]],
'PR50':
[[0, 25, 16, 5],
[3, 54, 29, 9]]
}
"""
DICT = {
'SGD':
{
'$ PR^{wd}$ = 0.9':
[[5, 10],
[8, 17]],
'Frequency-based':
[[7, 9],
[15, 11]],
'$ PR^{wd}$ = 0.25':[
[7, 9],
[10, 16]],
'$ PR^{wd}$ = 0.75':[
[5, 10],
[8, 17]],
'$ PR^{wd}$ = 0.50': [[7, 9], [10, 16]]
},

'MultiWoz':
{
'$ PR^{wd}$ = 0.9':[[0, 17, 13, 6],
[4, 33, 20, 13]],
'Frequency-based':[[15, 37, 11, 2],
[23, 62, 26, 5]],
'$ PR^{wd}$ = 0.25':[[1, 39, 15, 5],
[17, 59, 27, 8]],
'$ PR^{wd}$ = 0.75':
[[0, 17, 14, 6],
[4, 39, 22, 13]],
'$ PR^{wd}$ = 0.50':
[[0, 25, 16, 5],
[3, 54, 29, 9]]
}
}

n3(DICT)

# import matplotlib.pyplot as plt
# import numpy as np

# # Function to generate random data for the pie charts
# def generate_random_data():
#     return np.random.randint(10, 100, size=3)

# ##Labels for each pie chart
# labels = ['Category 1', 'Category 2', 'Category 3']

# # Create subplots with reduced wspace and hspace
# fig, axes = plt.subplots(2, 5, figsize=(15, 8), sharex=True, sharey=True)
# plt.subplots_adjust(wspace=0.3, hspace=0.4)  # Adjust the wspace and hspace parameters

# ## Generate and plot data for each subplot
# for i in range(2):
#     for j in range(5):
#         data = generate_random_data()
#         axes[i, j].pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
#         axes[i, j].set_title(f'Subplot {i*5 + j + 1}')

# # Add captions for each row
# for i, row_caption in enumerate(['Row 1 Caption', 'Row 2 Caption']):
#     axes[i, 0].text(-2.5, 1.5, row_caption, fontsize=12, ha='center')

# # Add common y-axis label
# fig.text(0.04, 0.5, 'Percentage', va='center', rotation='vertical')

# # Show the plots
# plt.show()
