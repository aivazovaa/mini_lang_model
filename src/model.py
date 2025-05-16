import torch.nn as nn
import torch
class CodeGenerator(nn.Module):
    def __init__(self,vocab_size,emb_dim=128,hidden_dim=256,pad_idx=0):
        super().__init__()
        self.emb=nn.Embedding(vocab_size,emb_dim,padding_idx=pad_idx)
        self.lstm=nn.LSTM(emb_dim,hidden_dim,num_layers=1,batch_first=True)
        self.fc=nn.Linear(hidden_dim,vocab_size)
    def forward(self,x):
        emb=self.emb(x)
        out,_=self.lstm(emb)
        return self.fc(out[:,-1,:])
