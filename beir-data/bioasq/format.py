import json
import os

out_dir = "marco-format"
os.makedirs(out_dir, exist_ok=True)

# documents
did2dmid = {}
count = 0
with open(os.path.join(out_dir, "collection.tsv"), 'w') as fout:
    with open("additional_passages.tsv") as fin:
        for line in fin:
            try:
                did, title, body = line.strip().split('\t')
                text = title+' '+body
            except ValueError:
                did, body = line.strip().split('\t')
                text = body
            if did in did2dmid:
                continue
            did2dmid[did] = count
            print(f'{count}\t{text}', file=fout)
            count += 1

    with open("allMeSH_2020.json", encoding="ISO-8859-1") as fin:
        jsonf = json.load(fin)
        for article in jsonf["articles"]:
            did, title, body = article["pmid"], article["title"], article["abstractText"]
            if did in did2dmid:
                continue
            did2dmid[did] = count
            if title is not None and body is not None:
                text = title+' '+body
            elif title is None:
                text = body
            elif body is None:
                text = title
            else:
                raise ValueError("Both title and body are empty")
            text = text.replace('\n', ' ').replace('\t', ' ')
            print(f'{count}\t{text}', file=fout)
            count += 1

with open(os.path.join(out_dir, "did2dmid.tsv"), 'w') as fout:
    for did, dmid in did2dmid.items():
        print(f'{did}\t{dmid}', file=fout)


# query
in_dir = "Task8BGoldenEnriched"
qid2qmid = {}
qid2reldoc = {}  # use marcoid here
count = 0
with open(os.path.join(out_dir, "queries.tsv"), 'w') as fout:
    for fname in os.listdir(in_dir):
        with open(os.path.join(in_dir, fname)) as fin:
            jsonf = json.load(fin)
            for question in jsonf['questions']:
                qid2qmid[question['id']] = count
                print(f'{count}\t{question["body"]}', file=fout)

                rel_doc_list = []
                for rel_doc in question['documents']:
                    rel_doc_list.append(did2dmid[rel_doc.split('/')[-1]])
                qid2reldoc[count] = rel_doc_list

                count += 1

with open(os.path.join(out_dir, "qid2qmid.tsv"), 'w') as fout:
    for qid, qmid in qid2qmid.items():
        print(f'{qid}\t{qmid}', file=fout)

# qrel
with open(os.path.join(out_dir, "qrels.tsv"), 'w') as fout:
    for qid, rel_doc_list in qid2reldoc.items():
        for rel_doc in rel_doc_list:
            print(f'{qid}\t0\t{rel_doc}\t1', file=fout)
