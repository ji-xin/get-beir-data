import os
import sys
import random

dataset = sys.argv[1]
in_folder = os.path.join(dataset, 'marco-format')
out_folder = dataset

# generate triples of query; pos_doc; neg_doc
# the choice of neg_doc makes sure all documents are included

queries = {}
documents = {}
with open(os.path.join(in_folder, 'queries.tsv')) as fin:
    for line in fin:
        qid, query = line.strip().split('\t')
        queries[int(qid)] = query

with open(os.path.join(in_folder, 'collection.tsv')) as fin:
    for line in fin:
        docid, document = line.strip().split('\t')
        documents[int(docid)] = document

qrels = {}  # qid: [ [rel_docs], [irrel_docs] ]
with open(os.path.join(in_folder, 'qrels.tsv')) as fin:
    for line in fin:
        qid, _, docid, rel = line.strip().split('\t')
        qid, docid, rel = int(qid), int(docid), int(rel)
        if qid not in qrels:
            qrels[qid] = [[], []]
        if rel>0:
            qrels[qid][0].append(docid)
        else:
            qrels[qid][1].append(docid)

def generate_triples(queries, qrels, documents, in_folder, out_folder):
    unseen_documents = set(documents.keys())
    prev_unseen_count = len(unseen_documents)
    rounds = 0
    finish = False
    with open(os.path.join(out_folder, 'triples.train.tsv'), 'w') as fout:
        while not finish:
            print('Round', rounds, len(unseen_documents), 'unseen docs left',
                  prev_unseen_count-len(unseen_documents), 'unseen docs reduced')
            prev_unseen_count = len(unseen_documents)
            rounds += 1
            for q_count, (qid, (rel_docs, irrel_docs)) in enumerate(qrels.items()):
                k_irrel = 0
                for rel_doc in rel_docs:
                    unseen_documents.discard(rel_doc)
                    while k_irrel < len(irrel_docs) and irrel_docs[k_irrel] not in unseen_documents:
                        k_irrel += 1
                    if k_irrel < len(irrel_docs):
                        unseen_documents.discard(irrel_docs[k_irrel])
                        neg_doc = irrel_docs[k_irrel]
                        k_irrel += 1
                    else:
                        if len(unseen_documents) == 0:
                            finish = True
                            break
                        random_doc = unseen_documents.pop()
                        unseen_documents.discard(random_doc)
                        neg_doc = random_doc
                        
                    print(f'{queries[qid]}\t{documents[rel_doc]}\t{documents[neg_doc]}',
                          file=fout)

#import cProfile
#cProfile.run("generate_triples(queries, qrels, documents, in_folder, out_folder)")
generate_triples(queries, qrels, documents, in_folder, out_folder)

