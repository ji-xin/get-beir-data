root="cqadupstack"
old_dir=$PWD

all="cqa-all"
mkdir -p ${root}/${all}
rm -rf ${root}/${all}/*

dss=`ls ${root}`
for ds in $dss; do
    if [[ ! $ds = $all ]]; then
        echo $ds
        python format.py ${root}/${ds}
        python generate_triples_simple.py ${root}/${ds}
        cat ${root}/${ds}/triples.simple.tsv >> ${root}/${all}/triples.simple.tsv
    fi
done

cd ~/projects/ANCE-working/ANCE/data
source ~/miniconda3/etc/profile.d/conda.sh  # otherwise we can't activate another conda env
conda activate ance
for ds in $dss; do
    if [[ ! $ds = $all ]]; then
        bash data_preprocess_beir.sh ${old_dir}/${root}/${ds}
    fi
done

cd ${old_dir}/${root}/${all}
ln -s ../tex/preprocessed_data ./preprocessed_data

