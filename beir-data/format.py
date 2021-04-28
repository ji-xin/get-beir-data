import json
import os
import sys

dataset = sys.argv[1]

in_folder = dataset
out_folder = os.path.join(dataset, 'marco-format')
os.makedirs(out_folder, exist_ok=True)

def strip_spaces(s_in):
    return s_in.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ').strip()

qid2queries = {}
with open(os.path.join(in_folder, 'queries.jsonl')) as fin:
    for line in fin:
        jsonl = json.loads(line)
        qid = jsonl['_id']
        query = strip_spaces(jsonl['text'].replace('\t', ' '))
        qid2queries[qid] = query


did2dmid = {}
# did: document id, as originally in the files provided by beir
# dmid: document marco-format id, integers starting from 0

count = 0
missing = 0
with open(os.path.join(in_folder, 'corpus.jsonl')) as fin:
    with open(os.path.join(out_folder, 'collection.tsv'), 'w') as fout:
        for line in fin:
            jsonl = json.loads(line)
            did = jsonl['_id']
            document = strip_spaces((jsonl['title'] + ' ' + jsonl['text']).replace('\t', ' '))
            if len(document) == 0:
                missing += 1
                continue
            did2dmid[did] = count
            print(f'{count}\t{document}', file=fout)
            count += 1

with open(os.path.join(out_folder, 'did2dmid.tsv'), 'w') as fout:
    for k, v in did2dmid.items():
        print(f'{k}\t{v}', file=fout)
print(f'Get {count} documents, discard {missing} empty documents')


qid2qmid = {}
# qid: query id, as originally in the files provided by beir
# qmid: query marco-format id, integers starting from 0

count = 0  # for query
missing = 0
with open(os.path.join(in_folder, 'qrels', 'test.tsv')) as fin:
    with open(os.path.join(out_folder, 'qrels.tsv'), 'w') as fout:
        for line_idx, line in enumerate(fin):
            if line_idx == 0:
                continue
            qid, did, score = line.strip().split('\t')
            if qid not in qid2qmid:
                qid2qmid[qid] = count
                count += 1
            if did not in did2dmid:
                missing += 1
            else:
                print(f'{qid2qmid[qid]}\t0\t{did2dmid[did]}\t{score}', file=fout)

print(f'Get {count} queries, discard {missing} qrels with unknown document ids')

with open(os.path.join(out_folder, 'queries.tsv'), 'w') as fout:
    for qid, qmid in qid2qmid.items():
        print(f'{qmid}\t{qid2queries[qid]}', file=fout)

with open(os.path.join(out_folder, 'qid2qmid.tsv'), 'w') as fout:
    for k, v in qid2qmid.items():
        print(f'{k}\t{v}', file=fout)
