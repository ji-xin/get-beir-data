import json
import os

out_dir = "marco-format"
os.makedirs(out_dir, exist_ok=True)

# documents
did2dmid = {}
count = 0
with open(os.path.join(out_dir, "collection.tsv"), 'w') as fout:
    with open("allMeSH_2019.json", encoding="ISO-8859-1") as fin:
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
in_dir = "Task7BGoldenEnriched"
qid2qmid = {}
qid2reldoc = {}  # use marcoid here
unseen_documents = []
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
                    doc_pubmed_id = rel_doc.split('/')[-1]
                    if doc_pubmed_id not in did2dmid:
                        unseen_documents.append(doc_pubmed_id)
                    else:
                        rel_doc_list.append(did2dmid[doc_pubmed_id])
                qid2reldoc[count] = rel_doc_list

                count += 1

with open("unseen_documents.txt", 'w') as fout:
    for doc in unseen_documents:
        print(doc, file=fout)

with open(os.path.join(out_dir, "qid2qmid.tsv"), 'w') as fout:
    for qid, qmid in qid2qmid.items():
        print(f'{qid}\t{qmid}', file=fout)

# qrel
with open(os.path.join(out_dir, "qrels.tsv"), 'w') as fout:
    for qid, rel_doc_list in qid2reldoc.items():
        for rel_doc in rel_doc_list:
            print(f'{qid}\t0\t{rel_doc}\t1', file=fout)
