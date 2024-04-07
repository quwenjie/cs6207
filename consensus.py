import pickle
from openai import OpenAI
import random
FILES=["Llama-2-7b-chat-hf.ans","falcon-7b-instruct.ans","vicuna1.5.ans","llama1.ans","alpaca.ans"]

client = OpenAI()
content="Summarize and only reach consensus and output one number, and omit the discrepancy in the provided numbers"
ANS=[[],[],[],[],[]]
GT=[]
for i,f in enumerate(FILES):
    ans=pickle.load(open(f,"rb"))
    P=0.35
    for xx,ours,ours_ in ans:
        if random.random()>=P:
            ANS[i].append(ours_)
        else:
            ANS[i].append(ours)
    for _,_,gt in ans:
        GT.append(gt)
CONSENSUS=[]
for i in range(100):
    content_now=f"{content} Information1:{ANS[0][i]} \n Information2:{ANS[1][i]} \n Information3:{ANS[2][i]} \n Information4:{ANS[3][i]} \n Information5:{ANS[4][i]} \n"
    print(content_now)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": content_now},
    ]
    )
    respond=response.choices[0].message.content
    print(respond)
    CONSENSUS.append({"GT":GT[i],"CONSENSUS":respond})
pickle.dump(CONSENSUS,open("consensus.pic","wb"))