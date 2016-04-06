#A cute script to visualise the super transcripts blocks and the blocks from the transcripts which build it
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from matplotlib.pyplot import cm
import seaborn as sns
#plt.style.use('fivethirtyeight')

##################################################
###### Visualise blocks in SuperTranscript #######
##################################################

#Match transcripts to super transcript
#if(os.path.isfile('supercomp.psl') == False):
print("Producing match to super transcript")
BLAT_command = "./blat Super.fasta ESR1_transcripts_for_Michael.fasta supercomp.psl"
#BLAT_command = "./blat Super.fasta s.cerevisiae/Cluster-1220.1.fasta supercomp.psl"
os.system(BLAT_command)

#First read in BLAT output:
Header_names = ['match','mismatch','rep.','N\'s','Q gap count','Q gap bases','T gap count','T gap bases','strand','Q name','Q size','Q start','Q end','T name','T size','T start','T end','block count','blocksizes','qStarts','tStarts']
vData = pd.read_table('supercomp.psl',sep='\t',header = None,names=Header_names,skiprows=5)

#Make list of transcripts
transcripts = np.unique(list(vData['Q name']))

#First pass attempt, make a stacked bar chart of all the nodes in C in order, with size dependent on length of string, iterate through coloirs

#Get Super Transcript Length
ST_length = vData.iloc[0,14]

plt.barh(len(transcripts),ST_length,color='Black',left=0)

plot_dict = {}
col_dict = {}
labs = []

col2=iter(cm.plasma(np.linspace(0,1,len(transcripts))))
for i,key in enumerate(transcripts):
        plot_dict[key] = i
        col_dict[key] = next(col2)
        lab = "T"+str(i)
        labs.append(lab)

for irow in range(0,len(vData)):

        #Get blocks
        block_sizes = (vData.iloc[irow,18]).rstrip(',').split(',')
        tStarts = (vData.iloc[irow,20]).rstrip(',').split(',')
        qName = vData.iloc[irow,9]

        #Print transcripts blocks
        for block in range(0,len(block_sizes)):
                si = int(block_sizes[block])
                left = int(tStarts[block])
                plt.barh(plot_dict[qName],si,color=col_dict[qName],left=left,alpha=0.7)

################
#Get Metrics ###
################

#Check if there is one entry per file
print("Transcript in gene: ", len(transcripts))
print("Blocks in SuperTranscripts: ", len(vData.index))

#Check if each transcript is given in order
counter = 0
for i in range(0,len(vData.index)):
	if(int(vData.iloc[0,10]) == int(vData.iloc[0,0])):
		counter = counter + 1
print("Transcripts fully matched to SuperTranscript: ", counter)

#Fix y-axis
ind=np.arange(len(transcripts)+1)
width=0.8
labs.append('Super')
plt.yticks(ind + width/2.,labs)
plt.title('Breakdown of Super Transcript')
plt.xlabel('Bases')
plt.ylabel('Transcripts')
plt.show()



