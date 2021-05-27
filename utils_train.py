import os
import codecs
import json
import csv
import numpy as np
import torch
import glob

def save_data(domain, results, epoch, run_epoch):
    add = str(run_epoch) + '_' + str(epoch)+".utf8"
    output_file = 'train_data/' + domain + '/' + add
    with open(output_file, "w", encoding='utf8') as f:
        to_write = []
        for block in results:
            for line in block:
                to_write.append(line + "\n")
            to_write.append("\n")
        f.writelines(to_write)

def batch_generator(X, y, batch_size=128, return_idx=False, crf=True):
    for offset in range(0, X.shape[0], batch_size):
        batch_X_len=np.sum(X[offset:offset+batch_size]!=0, axis=1)
        batch_idx=batch_X_len.argsort()[::-1]
        batch_X_len=batch_X_len[batch_idx]
        batch_X_mask=(X[offset:offset+batch_size]!=0)[batch_idx].astype(np.uint8)
        batch_X=X[offset:offset+batch_size][batch_idx]
        batch_y=y[offset:offset+batch_size][batch_idx]
        batch_X = torch.autograd.Variable(torch.from_numpy(batch_X).long().cuda())
        batch_X_mask=torch.autograd.Variable(torch.from_numpy(batch_X_mask).long().cuda())
        batch_y = torch.autograd.Variable(torch.from_numpy(batch_y).long().cuda())
        if len(batch_y.size())==2 and not crf:
            batch_y=torch.nn.utils.rnn.pack_padded_sequence(batch_y, batch_X_len, batch_first=True)
        if return_idx:
            yield (batch_X, batch_y, batch_X_len, batch_X_mask, batch_idx)
        else:
            yield (batch_X, batch_y, batch_X_len, batch_X_mask)

def valid_loss(model, valid_X, valid_y, crf=True):
    model.eval()
    losses=[]
    for batch in batch_generator(valid_X, valid_y, crf=crf):
        batch_valid_X, batch_valid_y, batch_valid_X_len, batch_valid_X_mask=batch
        loss=model(batch_valid_X, batch_valid_X_len, batch_valid_X_mask, batch_valid_y)
        losses.append(loss.item())
    model.train()
    return sum(losses)/len(losses)

def generate_idx_word(fn):
    if len(fn) <= 23:
        word_idx_fn = 'data/prep_data/word_idx.json'
    else:
        word_idx_fn = 'data/prep_data_15/word_idx_15.json'
    with open(word_idx_fn) as f:
        word_idx=json.load(f)
    idx_word={}
    for key,val in word_idx.items():
        idx_word[val]=key
    return idx_word

def remove_temporary_file(domain, runs):
    path = 'train_data/' + domain + '/'
    for i in range(runs):
        delete_target = path + str(i) + '*'
        for filename in glob.glob(delete_target):
             os.remove(filename)
