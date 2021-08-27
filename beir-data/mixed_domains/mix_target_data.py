import os

input_domains = ['tinybioasq', 'trec-covid']
output_name = 'BioCovid'

os.makedirs(output_name, exist_ok=True)
input_lines = []
for domain in input_domains:
    input_fname = f'../{domain}/triples.simple.tsv'

    with open(input_fname) as fin:
        input_lines.append(fin.readlines())


# Make sure each input domain has the same contribution to the mixed dataset
# Repeat some input domains if necessary
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

