import os
import sys
import random

in_folders = sorted([x for x in os.listdir('../..') if 'cqa' not in x and 'merged_collection' not in x])
out_folder = "marco-format"
os.makedirs(out_folder, exist_ok=True)

collection = []
for ds in in_folders:
    with open(os.path.join('../..', ds, 'marco-format', 'collection.tsv')) as fin:
        for line in fin:
            _, doc = line.strip().split('\t')
            collection.append(doc)
random.shuffle(collection)

with open(os.path.join(out_folder, 'collection.tsv'), 'w') as fout:
    for i, doc in enumerate(collection):
        print(f'{i}\t{doc}', file=fout)

with open(os.path.join(out_folder, 'queries.tsv'), 'w') as fout:
    print("0\tDUMMY QUERY", file=fout)

with open(os.path.join(out_folder, 'qrels.tsv'), 'w') as fout:
    print("0\t0\t0\t1", file=fout)
