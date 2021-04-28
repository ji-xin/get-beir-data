import os
import sys
import random

dataset = sys.argv[1]
in_folder = os.path.join(dataset, 'marco-format')
out_folder = dataset

# each triple is a query and two random documents

queries = []
documents = []
with open(os.path.join(in_folder, 'queries.tsv')) as fin:
    for line in fin:
        qid, query = line.strip().split('\t')
        queries.append(query)

with open(os.path.join(in_folder, 'collection.tsv')) as fin:
    for line in fin:
        docid, document = line.strip().split('\t')
        documents.append(document)

if len(documents)%2 != 0:
    # make it even
    documents.pop()


def generate_triples(queries, documents, in_folder, out_folder):
    query_count = 0
    document_count = 0
    query_finish = False
    document_finish = False
    with open(os.path.join(out_folder, 'triples.simple.tsv'), 'w') as fout:
        while not (query_finish and document_finish):
            print(f'{queries[query_count]}\t{documents[document_count]}\t{documents[document_count+1]}', file=fout)
            query_count += 1
            document_count += 2
            if query_count == len(queries):
                query_finish = True
                query_count = 0
            if document_count == len(documents):
                document_finish = True
                document_count = 0


generate_triples(queries, documents, in_folder, out_folder)

