from model_utils import load_model_and_tokenizer, compute_cross_entropy
import torch
import numpy as np
import argparse
import pickle
parser = argparse.ArgumentParser()
parser.add_argument('--model', help="model", type=str)  #"meta-llama/Llama-2-7b-chat-hf"
parser.add_argument('--th', help="threshold", type=float)
args = parser.parse_args()

model_path = args.model
device = "cuda"

name=model_path.split('/')[1]+'.ans'
# Load the model and tokenizer
model, tokenizer = load_model_and_tokenizer(model_path, low_cpu_mem_usage=True, 
                       use_cache=False,
                       device=device)
dat=pickle.load(file=open('formula.dat','rb'))
ANS=[]
CORRECT=0
TOTAL=0
for qn, gt_ans in dat:
    qn="What is "+qn+"="
    input_ids = tokenizer.encode(qn, return_tensors="pt").to(device)
    output = model.generate(input_ids, return_dict_in_generate=True, output_scores=True, max_length=500, num_return_sequences=1, do_sample=False)
    input_length = input_ids.shape[1]
    generated_tokens = output.sequences[:, input_length:]
    answer=tokenizer.batch_decode(generated_tokens,skip_special_tokens=True)[0]
    print("Question : ",qn, "ANS: ",answer, "GT: ",gt_ans)
    transition_scores = model.compute_transition_scores(
        output.sequences, output.scores, normalize_logits=True
    )
    LOG=0
    SUM=0
    for tok, score in zip(generated_tokens[0], transition_scores[0]):
        LOG+=score.cpu().numpy()
        SUM+=1
    PPL=    -LOG/SUM
    if PPL>args.th:
        print('detect hallucinate!')
    fd=answer[-5:].find(str(gt_ans))
    def parse(st):
        p=""
        for c in st:
            if not c.isdigit():
                continue
            p+=c
        return int(p)
    our_ans=parse(answer[-4:])
    ANS.append((answer,our_ans,gt_ans))
    if our_ans==gt_ans:
        CORRECT+=1
    TOTAL+=1
    print(TOTAL,CORRECT/TOTAL)
    pickle.dump(ANS,file=open(name,"wb"))
