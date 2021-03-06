import random
from beir import util, LoggingHandler
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.lexical import BM25Search as BM25

from beir.datasets.read_from_marco_format import read_from_marco_format

import pathlib, os, sys
import logging

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout


if os.path.exists(sys.argv[1]) and 'marco-format' in sys.argv[1]:
    # After directly evaluating marco-formatted trec-covid,
    # it seems that merging corpus title and text has a negative impact
    # therefore we will use the original implementation for BM25
    # instead of doing BM25 on the marco-formatted one
    SAVE_BM25_RESULTS = True
    dataset = sys.argv[1][1:].replace('/', '__')
    corpus, queries, qrels = read_from_marco_format(sys.argv[1])
else:
    #### Download and unzip the dataset
    SAVE_BM25_RESULTS = False
    dataset = sys.argv[1]
    url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset)
    out_dir = os.path.join(pathlib.Path(__file__).absolute().parent.parent.parent.parent.parent,
                           "beir-data")
    data_path = os.path.join(out_dir, dataset)
    if not os.path.exists(os.path.join(data_path, 'corpus.jsonl')):
        data_path = util.download_and_unzip(url, out_dir)

    #### Provide the data_path where the dataset has been downloaded and unzipped
    corpus, queries, qrels = GenericDataLoader(data_path).load(split="test")

#### Provide parameters for elastic-search
hostname = "localhost"
index_name = dataset
initialize = True # True, will delete existing index with same name and reindex all documents
model = BM25(index_name=index_name, hostname=hostname, initialize=initialize)
retriever = EvaluateRetrieval(model)

#### Retrieve dense results (format of results is identical to qrels)
results = retriever.retrieve(corpus, queries)
if SAVE_BM25_RESULTS:
    with open(os.path.join(sys.argv[1], 'runs.bm25.txt'), 'w') as fout:
        for qid, q_list in results.items():
            for rank, (pid, score) in enumerate(q_list.items()):
                print(f'{qid} Q0 {pid} {rank+1} {score} BM25', file=fout)
    os.system(f"python count_hole.py {os.path.join(sys.argv[1], 'runs.bm25.txt')} {os.path.join(sys.argv[1], 'qrels.tsv')}")

#### Evaluate your retrieval using NDCG@k, MAP@K ...
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
exit(0)

#### Retrieval Example ####
query_id, scores_dict = random.choice(list(results.items()))
print("Query : %s\n" % queries[query_id])

scores = sorted(scores_dict.items(), key=lambda item: item[1], reverse=True)
for rank in range(10):
    doc_id = scores[rank][0]
    print("Doc %d: %s [%s] - %s\n" % (rank+1, doc_id, corpus[doc_id].get("title"), corpus[doc_id].get("text")))
