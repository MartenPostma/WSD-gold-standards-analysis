'''
goal is to convert the semcor16
into the following format
DOCUMENT_ID LEMMA.IDENTIFIER KEY1 KEY2 KEYN
'''
import os
import glob

cwd = os.getcwd()

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
                        iden = doc_id + '.' + str(counter)
                        output = '{doc_id} {lemma}.{iden} {sense_key}\n'.format(**locals())
                        outfile.write(output)





