# do `conda activate beir` before running this

dataset=${1}
old_dir=$PWD

# special preprocessing for bioasq
if [[ $dataset = bioasq ]]; then
    cd $dataset
    python special_preprocess.py
    cd ..
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}/marco-format

else
    # download the dataset from BEIR and run BM25
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}
    rm -f ${dataset}.zip

    # create "marco-format" for this dataset, so it can be processed by ANCE
    python format.py ${dataset}
fi

# create tiny version if necessary
if [[ $dataset = bioasq ]]; then
    python build_tiny.py bioasq tinybioasq 500
    tiny_dataset=tinybioasq
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${tiny_dataset}/marco-format
elif [[ $dataset = dbpedia-entity ]]; then
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}/marco-format
    python build_tiny.py ${dataset} tinydbpedia 200 # will change this to 500 later
    tiny_dataset=tinydbpedia
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${tiny_dataset}/marco-format
elif [[ $dataset = nq ]]; then
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}/marco-format
    python build_tiny.py ${dataset} tinynq 100
    tiny_dataset=tinynq
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${tiny_dataset}/marco-format
elif [[ $dataset = hotpotqa ]]; then
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}/marco-format
    python build_tiny.py ${dataset} tinyhotpotqa 100
    tiny_dataset=tinyhotpotqa
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${tiny_dataset}/marco-format
fi

# create the "triples" file for domain adaptation
python generate_triples_simple.py ${dataset}
if [ -n "$tiny_dataset" ]; then
    echo $tiny_dataset
    exit 0
    python generate_triples_simple.py ${tiny_dataset}
fi

# ANCE's preprocessing
cd ~/projects/ANCE-working/ANCE/data
source ~/miniconda3/etc/profile.d/conda.sh  # otherwise we can't activate another conda env
conda activate ance
bash data_preprocess_beir.sh ${old_dir}/${dataset}
if [ -n "$tiny_dataset" ]; then
    bash data_preprocess_beir.sh ${old_dir}/${tiny_dataset}
fi
