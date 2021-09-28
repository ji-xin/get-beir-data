import json
import os
import sys

out_folder = 'marco-format'
os.makedirs(out_folder, exist_ok=True)

def strip_spaces(s_in):
    return s_in.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ').strip()

qid2queries = {}
with open('genq-queries.jsonl') as fin:
    for line in fin:
        jsonl = json.loads(line)
        qid = jsonl['_id']
        query = strip_spaces(jsonl['text'].replace('\t', ' '))
        qid2queries[qid] = query


did2document = {}
with open('merged_collection/marco-format/collection.tsv') as fin:
    for line in fin:
        did, document = line.strip().split('\t')
        did2document[did] = document


qid2qmid = {}
count = 0  # queries
used_did = set()
with open(os.path.join('genq-qrels', 'train.tsv')) as fin:
    with open(os.path.join(out_folder, 'qrels.tsv'), 'w') as fout:
        for line_idx, line in enumerate(fin):
            if line_idx == 0:
                continue
            qid, did, score = line.strip().split('\t')
            if qid not in qid2qmid:
                qid2qmid[qid] = count
                count += 1
            print(f'{qid2qmid[qid]}\t0\t{did}\t{score}', file=fout)
            used_did.add(did)


with open(os.path.join(out_folder, 'queries.tsv'), 'w') as fout:
    for qid, qmid in qid2qmid.items():
        print(f'{qmid}\t{qid2queries[qid]}', file=fout)

with open(os.path.join(out_folder, 'qid2qmid.tsv'), 'w') as fout:
    for k, v in qid2qmid.items():
        print(f'{k}\t{v}', file=fout)

used_did = list(used_did)
used_did.sort(key=lambda x: int(x))
with open(os.path.join(out_folder, 'collection.tsv'), 'w') as fout:
    for did in used_did:
        print(f'{did}\t{did2document[did]}', file=fout)
