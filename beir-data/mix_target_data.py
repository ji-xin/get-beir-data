import os

input_domains = ['trec-covid', 'dbpedia-entity', 'robust04']
output_name = 'tcdbrb'

os.makedirs(output_name, exist_ok=True)
input_lines = []
for domain in input_domains:
    if domain == 'robust04':
        input_fname = '/mnt/robust04/triples.simple.tsv'
    else:
        input_fname = f'{domain}/triples.simple.tsv'

    with open(input_fname) as fin:
        input_lines.append(fin.readlines())

finished = [0 for _ in range(len(input_domains))]
which_domain = 0
domain_pointers = [0 for _ in range(len(input_domains))]
domain_lens = [len(input_lines[i]) for i in range(len(input_domains))]
with open(os.path.join(output_name, 'triples.simple.tsv'), 'w') as fout:
    while sum(finished) < len(input_domains):
        if domain_pointers[which_domain] == domain_lens[which_domain]:
            finished[which_domain] = 1
            domain_pointers[which_domain] = 0
        fout.write(input_lines[which_domain][domain_pointers[which_domain]])
        domain_pointers[which_domain] += 1
        which_domain = (which_domain + 1) % len(input_domains)

