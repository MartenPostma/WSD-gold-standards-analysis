'''
goal is to convert the reuters corpus
into the following format
DOCUMENT_ID LEMMA.IDENTIFIER KEY1 KEY2 KEYN

following
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.150.682&rep=rep1&type=pdf

Koeling et al. [2005] did not clarify the method to select the
“correct” sense, and we decided to choose the sense chosen
by the majority of taggers. In case of ties we discarded the
occurrence from the test set.
'''
from collections import defaultdict
import operator

input_path = 'hlt2005releasev2/domainhltGS/gold_standard_clean.txt'
data = {}

with open(input_path) as infile:
    for line in infile:
        split = line.strip().split()
        identifier, sense_key = split[1], split[3]

        if any(['%' not in sense_key,
                sense_key == 'record%1:10:02::__record%1:21:00::']):
            continue

        if identifier not in data:
            data[identifier] = defaultdict(int)

        data[identifier][sense_key] += 1

identifiers = {}

for identifier,info in data.items():
    max_key, max_value = max(info.items(), key=operator.itemgetter(1))

    values = list(info.values())
    if values.count(max_value) == 1:
        identifiers[identifier] = max_key


with open('answers','w') as outfile:
    for identifier, sense_key in identifiers.items():
        doc_id = identifier.split('.')[2] + '.' + identifier.split('.')[3]
        output = '{doc_id} {identifier} {sense_key}\n'.format(**locals())
        outfile.write(output)

