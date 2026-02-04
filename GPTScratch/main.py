# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import urllib.request
import re
import torch
from DataLoader import create_dataloader_v1
from SimpleTokenizerV1 import SimpleTokenizer# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/main/ch02/01_main-chapter-code/the-verdict.txt"
    filepath = "the-verdict.txt"
    urllib.request.urlretrieve(url, filepath)

    with open("the-verdict.txt", 'r',encoding="utf-8") as f:
        raw_text = f.read()
   # print(raw_text[:99])
   # print("total no of character", len(raw_text))
    preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
    preprocessed = [item.strip() for item in preprocessed if item.strip()]
   # print(len(preprocessed))
   # print(preprocessed[:30])
    all_words = sorted(set(preprocessed))
    all_words.extend(["<|endoftext|>","<|unk|>"])
   # print(len(all_words))
    vocab = {token:integer for integer, token in enumerate(all_words)}
    tokenizer=SimpleTokenizer(vocab)
    enc_text=tokenizer.encode(raw_text)
    enc_sample=enc_text[:100]


    
    print(len(enc_text))
    context_size=4
    x = enc_text[:context_size]
    y = enc_text[1:context_size+1]
    for i in range(1,context_size+1):
        context = enc_sample[:i]
        desired = enc_sample[i]
        print(context,"------>",desired)
        print(tokenizer.decode(context),"------>",tokenizer.decode([desired]))

    vocab_size=50257
    output_dim=256
    max_length=4
    dataloader=create_dataloader_v1(raw_text,batch_size=8,max_length=max_length,stride=max_length,shuffle=False)
    data_iter = iter(dataloader)
    inputs,targets = next(data_iter)
    print("Token id's",inputs)
    print("Input Shape",inputs.shape)
    print("Target id's",targets)
    token_embedding_layer=torch.nn.Embedding(vocab_size,output_dim)
    token_embeddings=token_embedding_layer(inputs)






