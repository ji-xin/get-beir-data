# Obtain Target Domain (BEIR) Data

This repo is based on https://github.com/beir-cellar/beir and is used to obtain target domain data for https://github.com/ji-xin/modir.

We use `trec-covid` as the target domain dataset as an example. Other "ordinary" datasets (nfcorpus, nq, hotpotqa, fiqa, touche, quora, dbpedia, scidocs, fever, climatefever, scifact) can also be processed in the same way (check the table at the bottom of the page for their BEIR-names).

For other datasets, check [special datasets](#special-datasets).

### Step 1
Create a new conda environment and install from source:

`pip install -e .`

### Step 2
First, install ElasticSearch server and run it. And then,

`cd examples/retrieval/evaluation/lexical`, and run:

`python evaluate_bm25.py trec-covid`

It will automatically download the dataset and do BM25 evaluation.

### Step 3
Go back to repo root and `cd beir-data`, run:

`python format.py trec-covid` and `python generate_triples_simple.py trec-covid`.

### Step 4
Copy the folder `marco-format` and the file `triples.simple.tsv` from `beir-data/trec-covid` to the `data/treccovid` folder inside the `modir` repo.


## Special Datasets


Special dataset 1 - `arguana`: replace step 3 with

`cd beir-data && python arguana_format.py arguana`

Special dataset 2 - `cqadupstack`:

Run the first 2 steps.
The second step will fail, but it will download the data we need.
After that, `cd beir-data && bash cqa.sh`.
Then go back to modir's repo and preprocess each of the subsets.
Use `cqadupstack/cqa-all/triples.simple.tsv` for training and the preprocessed data of any of the subsets for validation.

Special dataset 3 - `bioasq`:

Download into `beir-data/bioasq/external_data`, and then run

`cd beir-data/bioasq && python special_preprocess.py`

Your own datasets: the idea of processing them is as follows.

First, process them into "marco-format". It's the tsv format the msmarco uses. If not sure, try with `trec-covid` first, and then check `trec-covid/marco-format`.

And then go back to the `modir` repo and run preprocess from there, similar to step 4.

## Available Datasets from BEIR

| Dataset   | Website| BEIR-Name | Queries  | Documents | Avg. Docs/Q | Download |
| -------- | -----| ---------| ----------- | ---------| ---------| ------------| 
| MSMARCO    | [Homepage](https://microsoft.github.io/msmarco/)| ``msmarco`` |  6,980   |  8.84M     |    1.1 | [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/msmarco.zip) |  
| TREC-COVID |  [Homepage](https://ir.nist.gov/covidSubmit/index.html)| ``trec-covid``| 50|  171K| 493.5 | [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/trec-covid.zip) | 
| NFCorpus   | [Homepage](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/) | ``nfcorpus``  |  323     |  3.6K     |  38.2 | [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nfcorpus.zip) |
| BioASQ     | [Homepage](http://bioasq.org) | ``bioasq``|  500    |  14.91M    |  8.05 | No | 
| NQ         | [Homepage](https://ai.google.com/research/NaturalQuestions) | ``nq``|  3,452   |  2.68M  |  1.2 | [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nq.zip) | 
| HotpotQA   | [Homepage](https://hotpotqa.github.io) | ``hotpotqa``|  7,405   |  5.23M  |  2.0 | [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/hotpotqa.zip)  |
| FiQA-2018  | [Homepage](https://sites.google.com/view/fiqa/) | ``fiqa``    | 648     |  57K    |  2.6 | [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/fiqa.zip)  | 
| Signal-1M(RT) | [Homepage](https://research.signal-ai.com/datasets/signal1m-tweetir.html)| ``signal1m`` |  97   |  2.86M  |  19.6 | No |
| TREC-NEWS  | [Homepage](https://trec.nist.gov/data/news2019.html) | ``trec-news``    | 57    |  595K    |  19.6 | No |
| ArguAna    | [Homepage](http://argumentation.bplaced.net/arguana/data) | ``arguana`` | 1,406     |  8.67K    |  1.0 | [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/arguana.zip)  |
| Touche-2020| [Homepage](https://webis.de/events/touche-20/shared-task-1.html) | ``webis-touche2020``| 49     |  382K    |  49.2 |  [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/webis-touche2020.zip) |
| CQADupstack| [Homepage](http://nlp.cis.unimelb.edu.au/resources/cqadupstack/) | ``cqadupstack``|  13,145 |  457K  |  1.4 |  [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/cqadupstack.zip) |
| Quora| [Homepage](https://www.quora.com/q/quoradata/First-Quora-Dataset-Release-Question-Pairs) | ``quora``|  10,000     |  523K    |  1.6 |  [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/quora.zip) | 
| DBPedia | [Homepage](https://github.com/iai-group/DBpedia-Entity/) | ``dbpedia-entity``| 400    |  4.63M    |  38.2 | [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/dbpedia-entity.zip) | 
| SCIDOCS| [Homepage](https://allenai.org/data/scidocs) | ``scidocs``|  1,000     |  25K    |  4.9 |  [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scidocs.zip) | 
| FEVER| [Homepage](http://fever.ai) | ``fever``|  6,666     |  5.42M    |  1.2|  [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/fever.zip)  | 
| Climate-FEVER| [Homepage](http://climatefever.ai) | ``climate-fever``|  1,535     |  5.42M |  3.0 |  [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/climate-fever.zip)  |
| SciFact| [Homepage](https://github.com/allenai/scifact) | ``scifact``|  300     |  5K    |  1.1 |  [Link](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scifact.zip)  |
