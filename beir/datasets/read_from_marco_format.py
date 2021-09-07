import os

def read_from_marco_format(path):
    corpus = {}
    with open(os.path.join(path, 'collection.tsv')) as fin:
        for line in fin:
            did, document = line.strip().split('\t')
            corpus[did] = {"title": "", "text": document}

    queries = {}
    with open(os.path.join(path, 'queries.tsv')) as fin:
        for line in fin:
            qid, query = line.strip().split('\t')
            queries[qid] = query

    qrels = {}
    with open(os.path.join(path, 'qrels.tsv')) as fin:
        for line in fin:
            qid, _, did, score = line.strip().split('\t')
            if qid not in qrels:
                qrels[qid] = {}
            qrels[qid][did] = int(score)

    return corpus, queries, qrels

