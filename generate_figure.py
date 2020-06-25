import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
from scipy.stats import ttest_ind

# create network
print('creating network...')
network_data_frame = pd.read_csv('data.txt', sep=' ', header = 0)
network = nx.from_pandas_edgelist(network_data_frame, source = 'protein1', target = 'protein2', 
                                  edge_attr = 'combined_score')
# make partition
print('making partition...')
protein_high_degree = [n.split('.')[1] for n, d in network.degree if d>100]
protein_low_degree = [n.split('.')[1] for n, d in network.degree if d<=100]

# load domain data
print('loading domain data...')
domain_data = pd.read_csv('proteins_w_domains.txt', sep='\t', header = 0)
domain_data.dropna(inplace=True)

# count domains for each protein
print('counting domains for each protein...\nThis may cost several minutes...')
dic_high = {protein:[len(domain_data[domain_data['Protein stable ID']==protein]),
                    'high'] 
          for protein in protein_high_degree}
dic_low = {protein:[len(domain_data[domain_data['Protein stable ID']==protein]),
                  'low'] 
         for protein in protein_low_degree}
dic=dic_high
dic.update(dic_low)
df=pd.DataFrame.from_dict(dic, orient='index',columns=['count','group'])

# plot and t-test
print('generating figures...')
ax=sns.boxplot(x='group',y='count',data=df,showfliers = False)
statistic,p = ttest_ind(df[df['group']=='high']['count'].values,
                        df[df['group']=='low']['count'].values)
ax.set_title('t-test p-value='+str(p))
ax.set(xticklabels=['node degree > 100', 'node degree <= 100'])
ax.set_ylabel('domains of the protein')
ax.get_figure().savefig("protein_domains_vs_string_degree.png")
