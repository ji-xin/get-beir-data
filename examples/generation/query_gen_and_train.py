from beir import util, LoggingHandler
from beir.datasets.data_loader import GenericDataLoader
from beir.generation import QueryGenerator as QGen
from beir.generation.models import QGenModel
from beir.retrieval import models
from beir.retrieval.train import TrainRetriever
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES
from beir.datasets.read_from_marco_format import read_from_marco_format
from sentence_transformers import losses

import pathlib, os, sys
import logging

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

logger = logging.getLogger(__name__)


if os.path.exists(sys.argv[1]) and 'marco-format' in sys.argv[1]:
    dataset = sys.argv[1].split('/')[-2]
    data_path = pathlib.Path(sys.argv[1]).parent
    logger.info(f"Loading {dataset} directly from marco-format. It's gonna take a while.")
    corpus, queries, qrels = read_from_marco_format(sys.argv[1])
    use_dev = False

else:
    #### Download nfcorpus.zip dataset and unzip the dataset
    dataset = sys.argv[1]
    url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset)

    out_dir = os.path.join(
        pathlib.Path(__file__).absolute().parent.parent.parent,
        "beir-data"
    )
    data_path = os.path.join(out_dir, dataset)
    if not os.path.exists(data_path):
        data_path = util.download_and_unzip(url, out_dir)
    else:
        logger.info(f"{dataset} already downloaded")

    use_dev = os.path.exists(os.path.join(data_path, "qrels", "dev.tsv"))

    #### Provide the data_path where the dataset has been downloaded and unzipped
    # corpus = GenericDataLoader(data_path).load_corpus()
    corpus, test_queries, test_qrels = GenericDataLoader(data_folder=data_path).load(split="test")



##############################
#### 1. Query-Generation  ####
##############################


#### Model Loading 
model_path = "BeIR/query-gen-msmarco-t5-base-v1"
generator = QGen(model=QGenModel(model_path))

#### Query-Generation using Nucleus Sampling (top_k=25, top_p=0.95) ####
#### https://huggingface.co/blog/how-to-generate
#### Instead of prefix, we use a separate folder
prefix = ""
gen_data_path = os.path.join(data_path, "genq")
os.makedirs(gen_data_path, exist_ok=True)

#### Generating 3 questions per passage. 
#### Reminder the higher value might produce lots of duplicates
ques_per_passage = 5
max_corpus_size = 500000  # 500k
capped_corpus = {k:v for k,v in list(corpus.items())[:max_corpus_size]}


#### Generate queries per passage from docs in corpus and save them in data_path
generator.generate(capped_corpus, output_dir=gen_data_path, ques_per_passage=ques_per_passage,
                   prefix=prefix)
exit(0)  # we only need generated queries for now

################################
#### 2. Train Dense-Encoder ####
################################


#### Training on Generated Queries ####
train_corpus, gen_queries, gen_qrels = GenericDataLoader(gen_data_path, prefix=prefix).load(split="train")
#### Please Note - not all datasets contain a dev split, comment out the line if such the case
if use_dev:
    dev_corpus, dev_queries, dev_qrels = GenericDataLoader(data_path).load(split="dev")

#### Provide any sentence-transformers model path
model_name = "bert-base-uncased"
retriever = TrainRetriever(model_name=model_name, batch_size=32)

#### Prepare training samples
train_samples = retriever.load_train(train_corpus, gen_queries, gen_qrels)
train_dataloader = retriever.prepare_train(train_samples, shuffle=True)
train_loss = losses.MultipleNegativesRankingLoss(model=retriever.model)

#### Prepare dev evaluator
if use_dev:
    ir_evaluator = retriever.load_ir_evaluator(dev_corpus, dev_queries, dev_qrels)
else:
    #### If no dev set is present evaluate using dummy evaluator
    ir_evaluator = retriever.load_dummy_evaluator()

#### Provide model save path
model_save_path = os.path.join(pathlib.Path(__file__).parent.absolute(), "output", f"{model_name}-GenQ-{dataset}")
os.makedirs(model_save_path, exist_ok=True)

#### Configure Train params
num_epochs = 1
evaluation_steps = 5000
warmup_steps = int(len(train_samples) * num_epochs / retriever.batch_size * 0.1)

retriever.fit(train_objectives=[(train_dataloader, train_loss)], 
                evaluator=ir_evaluator, 
                epochs=num_epochs,
                output_path=model_save_path,
                warmup_steps=warmup_steps,
                evaluation_steps=evaluation_steps,
                use_amp=True)


################################
#### 3. Eval Dense-Encoder ####
################################

test_model = DRES(models.SentenceBERT(model_save_path))
test_retriever = EvaluateRetrieval(test_model, score_function="cos_sim")  # SBERT requires cos
results = test_retriever.retrieve(corpus, test_queries)
ndcg, _map, recall, precision = test_retriever.evaluate(test_qrels, results, test_retriever.k_values)
