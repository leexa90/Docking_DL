import os
import numpy as np
f1 = open('seqres_V2.fa','r')
temp = []
name='0'
fasta = {}
for line in f1:
    if '>' in line:
        #print temp
        fasta[name] = temp
        name = line[1:-1]
        temp = ''
    else:
        temp += line[:-1]
    
fasta[name] = temp
np.save('fasta.npy',fasta)
f1 = open('NR_0_5_topo.txt','r')

impt_pdb = []
for line in f1:
    if line[:4] in [x[:4] for x in fasta.keys()]:
        impt_pdb +=[line[:-1],]
    else:
        print line
    
