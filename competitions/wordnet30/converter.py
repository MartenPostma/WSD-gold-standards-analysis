"""
goal is to convert the reuters corpus
into the following format
DOCUMENT_ID LEMMA.IDENTIFIER KEY1 KEY2 KEYN
"""


input_path = 'index.sense'
doc_id = 'wordnet30'


with open('answers', 'w') as outfile:
    with open(input_path) as infile:
        for counter,line in enumerate(infile):
            sense_key, offset, srq, freq = line.strip().split()
            lemma = sense_key.split('%')[0]
            identifier = lemma + '.' + doc_id + '.' + str(counter)
            output = '{doc_id} {identifier} {sense_key}\n'.format(**locals())
            outfile.write(output)

