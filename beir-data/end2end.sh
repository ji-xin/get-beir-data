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

# create the "triples" file for domain adaptation
python generate_triples_simple.py ${dataset}

# create tiny version if necessary
if [[ $dataset = bioasq ]]; then
    tiny_dataset=tinybioasq
    doc_per_query=500
elif [[ $dataset = dbpedia-entity ]]; then
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}/marco-format
    tiny_dataset=tinydbpedia
    doc_per_query=200
elif [[ $dataset = nq ]]; then
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}/marco-format
    tiny_dataset=tinynq
    doc_per_query=100
elif [[ $dataset = hotpotqa ]]; then
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}/marco-format
    tiny_dataset=tinyhotpotqa
    doc_per_query=100
elif [[ $dataset = fever ]]; then
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}/marco-format
    tiny_dataset=tinyfever
    doc_per_query=100
elif [[ $dataset = climate-fever ]]; then
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${dataset}/marco-format
    tiny_dataset=tinyclimatefever
    doc_per_query=100
fi

# create tinydataset if necessary
if [ -n "$tiny_dataset" ]; then
    python build_tiny.py ${dataset} ${tiny_dataset} ${doc_per_query}
    python ../examples/retrieval/evaluation/lexical/evaluate_bm25.py ${tiny_dataset}/marco-format
    
    # use the full dataset's triples file for the tiny one
    mv ${dataset}/triples.simple.tsv ${tiny_dataset}
fi

# ANCE's preprocessing
cd ~/projects/ANCE-working/ANCE/data
source ~/miniconda3/etc/profile.d/conda.sh  # otherwise we can't activate another conda env
conda activate ance
bash data_preprocess_beir.sh ${old_dir}/${dataset}
if [ -n "$tiny_dataset" ]; then
    bash data_preprocess_beir.sh ${old_dir}/${tiny_dataset}
fi
