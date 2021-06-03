import os
import sys

"""
Use BM25 to retrieve top200 documents for all queries (~80k in total)
these documents together constitute the collection of tinydbpedia
"""

queries = {}
documents = {}
qrels = {}
rel_pids = set()  # top50 documents from BM25, plus all from qrels

in_folder = "../dbpedia-entity/marco-format"
out_folder = "./marco-format"
os.makedirs(out_folder, exist_ok=True)

with open(os.path.join(in_folder, 'queries.tsv')) as fin:
    for line in fin:
        qid, query = line.strip().split('\t')
        qid = int(qid)
        queries[qid] = query

with open(os.path.join(in_folder, 'qrels.tsv')) as fin:
    for line in fin:
        qid, _, pid, rel = line.strip().split('\t')
        qid, pid, rel = int(qid), int(pid), int(rel)
        assert qid in queries
        if qid not in qrels:
            qrels[qid] = {}
        qrels[qid][pid] = rel
        if rel > 0:
            rel_pids.add(pid)

with open(os.path.join(in_folder, 'runs.bm25.txt')) as fin:
    for line in fin:
        qid, _, pid, rank, score, _ = line.strip().split(' ')
        qid, pid, rank = int(qid), int(pid), int(rank)
        assert qid in queries
        if rank <= 200:
            rel_pids.add(pid)

with open(os.path.join(in_folder, 'collection.tsv')) as fin:
    for line in fin:
        pid, doc = line.strip().split('\t')
        pid = int(pid)
        if pid in rel_pids:
            documents[pid] = doc

with open(os.path.join(out_folder, 'collection.tsv'), 'w') as fout:
    for pid, doc in documents.items():
        print(f'{pid}\t{doc}', file=fout)

with open(os.path.join(out_folder, 'queries.tsv'), 'w') as fout:
    for qid, query in queries.items():
        print(f'{qid}\t{query}', file=fout)

with open(os.path.join(out_folder, 'qrels.tsv'), 'w') as fout:
    for qid, query_rel in qrels.items():
        for pid, rel in query_rel.items():
            if qid in queries and pid in rel_pids:
                print(f'{qid}\t0\t{pid}\t{rel}', file=fout)

