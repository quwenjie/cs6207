import numpy as np
import random
import pickle
DATASET=[]
for j in range(100):
    p_add=0.75
    p_multi=0.25
    num=str(random.randint(1,10))
    for i in range(8):
        s=random.random()
        if s>p_add+p_multi:
            break
        if s<p_add:
            num=num+"+"+str(random.randint(1,10))
        else:
            num=num+"*"+str(random.randint(1,10))
        if i==2:
            p_add*=0.6
            p_multi*=0.6
    DATASET.append((num,eval(num)))
pickle.dump(DATASET,file=open("formula.dat","wb"))
