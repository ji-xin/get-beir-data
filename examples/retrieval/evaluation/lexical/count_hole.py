import sys
from collections import defaultdict

labels = defaultdict(dict) # [qid][pid] = 0/1
valid_query = set()
with open(sys.argv[2]) as fin:
    for line in fin:
        a = line.strip().split('\t')
        qid, pid, label = a[0], a[2], a[3]
        label = 0 if int(label)<=0 else 1
        labels[qid][pid] = label
        if label==1:
            valid_query.add(qid)

cuts = [5, 10, 20, 100]
total, missing = {cut: 0 for cut in cuts}, {cut: 0 for cut in cuts}

with open(sys.argv[1]) as fin:
    for line in fin:
        a = line.strip().split(' ')
        qid, pid, rank = a[0], a[2], int(a[3])
        if qid not in valid_query:
            continue
        for cut in cuts:
            if rank <= cut:
                total[cut] += 1
                if qid not in labels or pid not in labels[qid]:
                    missing[cut] += 1

for cut in cuts:
    print(f'hole@{cut}:', missing[cut]/total[cut])
