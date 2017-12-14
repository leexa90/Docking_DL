import os

import numpy as np
cmd.remove('resn WAT')
cmd.remove('resn Cl-')
cmd.remove('hydrogens')
cmd.split_states('*')
for i in range(1,202):

    i = (4-len(str(i)))*'0' + str(i)
    cmd.select('resi 1-87 and cartoon_%s'%i)
    cmd.select('(byres (sele) around 5 and cartoon_%s) or sele' %i)
    cmd.save(i+'.pdb','sele')
    cmd.delete('sele')

