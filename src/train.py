import torch,torch.nn as nn
from torch.utils.data import DataLoader,TensorDataset
from torch.nn.utils.rnn import pad_sequence
from dataset import create_dataset
from model import CodeGenerator
from vocab import VOCAB

def train():
    X,Y=create_dataset()
    X=pad_sequence(X,batch_first=True,padding_value=VOCAB['<PAD>'])
    Y=torch.tensor(Y)
    ds=DataLoader(TensorDataset(X,Y),batch_size=64,shuffle=True)
    model=CodeGenerator(vocab_size=len(VOCAB),pad_idx=VOCAB['<PAD>'])
    opt=torch.optim.Adam(model.parameters(),lr=0.001)
    crit=nn.CrossEntropyLoss(ignore_index=VOCAB['<PAD>'])
    for epoch in range(10):
        total=0
        for xb,yb in ds:
            opt.zero_grad()
            out=model(xb)
            loss=crit(out,yb)
            loss.backward()
            opt.step()
            total+=loss.item()
        print(f"Epoch {epoch+1}, loss={total/len(ds):.4f}")
    torch.save(model.state_dict(),'model.pt')
    return model
