'''
goal is to convert the semcor30
into the following format
DOCUMENT_ID LEMMA.IDENTIFIER KEY1 KEY2 KEYN
'''
import os
import glob
from collections import defaultdict
import pickle

cwd = os.getcwd()
training_freq = defaultdict(int)


with open('answers','w') as outfile:
    for folder in ['brown1','brown2','brownv']:
        folder_path = os.path.join(cwd,
                                   folder,
                                   'tagfiles')
        for path in glob.glob(folder_path+'/br*'):
            with open(path) as infile:
                doc_id = os.path.basename(path)
                for counter,line in enumerate(infile):
                    if all([line.startswith('<wf'),
                            'lexsn' in line]):

                        relevant = line.split('>')[0]

                        info = {item.split('=')[0]: item.split('=')[1]
                                 for item in relevant.split(' ')
                                 if '=' in item}

                        lemma = info['lemma']
                        sense_key = info['lemma'] + '%' + info['lexsn']

                        training_freq[sense_key] += 1

                        iden = doc_id + '.' + str(counter)
                        output = '{doc_id} {lemma}.{iden} {sense_key}\n'.format(**locals())
                        outfile.write(output)


with open('freq_training_examples.pickle', 'wb') as outfile:
    pickle.dump(training_freq, outfile)



