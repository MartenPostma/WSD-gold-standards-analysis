'''
goal is to convert the semcor30
into the following format
DOCUMENT_ID LEMMA.IDENTIFIER KEY1 KEY2 KEYN
'''
import os
import glob
from collections import defaultdict
import pickle
import re

cwd = os.getcwd()
training_freq = defaultdict(int)
lemma_pos = {}
output_dir = 'semcor30_lemmapos2sensekeys'



def get_lemma_pos_of_sensekey(sense_key):
    """
    lemma and pos are determined for a wordnet sense key

    .. doctest::
        >>> get_lemma_pos_of_sensekey('life%1:09:00::')
        ('life','n')

    :param str sense_key: wordnet sense key

    :rtype: tuple
    :return: (lemma, n | v | r | a | u)
    """
    if '%' not in sense_key:
        return '', 'u'

    lemma, information = sense_key.split('%')
    int_pos = information[0]

    if int_pos == '1':
        this_pos = 'n'
    elif int_pos == '2':
        this_pos = 'v'
    elif int_pos in {'3', '5'}:
        this_pos = 'a'
    elif int_pos == '4':
        this_pos = 'r'
    else:
        this_pos = 'u'

    return lemma, this_pos

def parse_line_with_sense_key(line, doc_id):
    """
    given a line from semcor30 like this:
    <wf cmd=done pos=JJ lemma=recent wnsn=2 lexsn=5:00:00:past:00>recent</wf>

    :param str line: line from semcor
    :param str doc_id: sourc document basename

    :rtype: tuple
    :return: sensekey, output_line_semeval
    """
    relevant = line.split('>')[0]

    info = {item.split('=')[0]: item.split('=')[1]
            for item in relevant.split(' ')
            if '=' in item}

    lemma = info['lemma']
    sense_key = info['lemma'] + '%' + info['lexsn']
    irrelevant, pos = get_lemma_pos_of_sensekey(sense_key)


    iden = doc_id + '.' + str(counter)
    output = '{doc_id} {lemma}.{iden} {sense_key}\n'.format(**locals())

    return lemma, sense_key, pos, output

sentence = []
key2indices = defaultdict(set)
index = 0


with open('answers','w') as outfile:
    for folder in ['brown1','brown2','brownv']:
        folder_path = os.path.join(cwd,
                                   folder,
                                   'tagfiles')
        for path in glob.glob(folder_path+'/br*'):
            with open(path) as infile:
                doc_id = os.path.basename(path)
                for counter,line in enumerate(infile):

                    if line.startswith('<punc>'):
                        token = re.findall('<punc>(.*)</punc>', line)[0]
                        sentence.append(token)
                        index += 1


                    elif line.startswith('<wf'):
                        token = re.findall('>(.*)</wf>', line)[0]
                        sentence.append(token)
                        if all([line.startswith('<wf'),
                                'lexsn' in line]):
                            lemma, sensekey, pos, output_line = parse_line_with_sense_key(line,
                                                                                          doc_id)
                            outfile.write(output_line)
                            training_freq[sensekey] += 1
                            key2indices[(sensekey, pos)].add((index, lemma))
                        index += 1

                    elif line.startswith('<s'):
                        sent_id = line.strip()[:-1].replace('<s snum=', '')

                    elif line.startswith('</s'):
                        for (sensekey, pos), info in key2indices.items():
                            for (index, lemma) in info:

                                target_sent = ['<head>%s</head>' % token
                                               if this_index == index else token
                                               for this_index,token in enumerate(sentence)]

                                target_sent = ' '.join(target_sent)

                                if (lemma, pos) not in lemma_pos:
                                    lemma_pos[(lemma, pos)] = defaultdict(set)

                                lemma_pos[(lemma, pos)][sensekey].add(target_sent)

                        # reset variables
                        sentence = []
                        key2indices = defaultdict(set)
                        index = 0


# write all lemma_pos pickle to file
for (lemma, pos), sensekeys in lemma_pos.items():
    path = os.path.join(output_dir, lemma + '___' + pos + '.pickle')
    with open(path, 'wb') as outfile:
        pickle.dump(sensekeys, outfile)

# write frequency to file
with open('freq_training_examples.pickle', 'wb') as outfile:
    pickle.dump(training_freq, outfile)



