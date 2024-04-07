import pickle
cs=pickle.load(open('consensus.pic','rb'))
COR=0
TOT=0
for dic in cs:
    def parse(st):
        p=""
        for c in st:
            if not c.isdigit():
                continue
            p+=c
        return int(p)
    now_ans=parse(dic['CONSENSUS'][-4:])
    if dic['GT']==now_ans:
        COR+=1
    TOT+=1
print(COR/TOT)
