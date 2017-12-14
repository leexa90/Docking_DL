import os
import pandas as pd
import numpy as np

pdb_files= sorted([x for x in os.listdir('data') if 'pdb' in x and '0' in x])

f1 = open('data/0001.pdb','r')
columns=['atom','atom_num','atom_type','resi','resi_num','X','Y','Z','-','--','atom','line']

data1 =pd.DataFrame(columns=columns)

def get_box(x,y,z,data):
    temp = []
    data = data[ (data['X'] >x ) & (data['X'] < x +9.6 )]
    data = data[ (data['Y'] >y ) & (data['Y'] < y +9.6)]
    data = data[ (data['Z'] >z ) & (data['Z'] < z +9.6)]    
    for i in range(len(data)):
        if data.iloc[i]['X'] > x and data.iloc[i]['X'] < x + 9.6 and \
           data.iloc[i]['Y'] > y and data.iloc[i]['Y'] < y + 9.6 and \
           data.iloc[i]['Z'] > z and data.iloc[i]['Z'] < z + 9.6 :
            temp += [data.iloc[i].values,]
    new = pd.DataFrame(temp,columns=columns)
    new['X'] = np.round(10*(new['X']-x),0).astype(np.int32)
    new['Y'] = np.round(10*(new['Y']-y),0).astype(np.int32)
    new['Z'] = np.round(10*(new['Z']-z),0).astype(np.int32)
    return new

    
dictt = {}
all_data = {}
for name in pdb_files:
    
    f1 = open('data/%s'%name,'r')
    temp =[]
    for line in f1:
        if 'ATOM' in line and len(line)>=20:
            temp += [line.split()+[line,],]
    temp = pd.DataFrame(temp,columns=columns)
    temp[['X','Y','Z']] = temp[['X','Y','Z']].values.astype(np.float32)
    temp[['X','Y','Z']] = temp[['X','Y','Z']] - np.mean(temp[['X','Y','Z']].values,0)
    dictt[name] = temp
    Bmin = np.min(temp[['X','Y','Z']].values,0)
    Bmax = np.max(temp[['X','Y','Z']].values,0)
    print name, Bmax-Bmin,
    Bmin = map(int,Bmin)
    Bmax = map(int,Bmax)
    print Bmin,Bmax

    for i in range(Bmin[0]+1,Bmax[0]-1,5)[:-1]:
        for j in range(Bmin[1]+1,Bmax[1]-1,5)[:-1]:
            for k in range(Bmin[2]+1,Bmax[2]-1,5)[:-1]:     
                temp2 = get_box(i,j,k,temp)
                if len(temp2) >= 20:
                    all_data[name+'%s_%s_%s'%(i,j,k)] = temp2
                    if len(all_data) %100==0:
                        print len(all_data)
if True:
    for i in all_data:
        if '0001.pdb' in i:
            f1=open(i,'w')
            for line in all_data[i]['line'].values:
                f1.write(line)
            f1.write('END\n');f1.close()
