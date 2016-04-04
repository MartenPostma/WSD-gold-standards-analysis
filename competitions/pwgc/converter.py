'''
goal is to convert the princeton wordnet gloss corpus
into the following format
DOCUMENT_ID LEMMA.IDENTIFIER KEY1 KEY2 KEYN


sensekey
    -> sentence
        -> (corpus, docsrc, instance_id)
        in this case, the corpus is 'semcor30'

'''

# lemma is of format: "great%1|great%3"
# focus on 'gloss/def' and 'gloss/ex' elements
# there can be more than one sense key

# gunzip WordNet-3.0.gz before running this script

from lxml import etree
from collections import defaultdict
import gzip
import pickle
import os

# needed: lemma, pos, sensekey, target sent

# sw_template = 'synset/gloss/{category}/wf[@tag="man"]'
# mw_template = 'synset/gloss/{category}/cf/glob[@tag="man"]'
lemma_pos = {}
output_dir = 'pwgc_lemmapos2sensekeys'

template = 'synset/gloss/{category}'
basedir = 'WordNet-3.0/glosstag/merged'
basenames = ['adj.xml.gz', 'adv.xml.gz','noun.xml.gz','verb.xml.gz']
paths = [ (basename[:-3], '/'.join([basedir,basename]))
          for basename in basenames]
categories = ['def', 'ex']

training_freq = defaultdict(int)
tokens = 0

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

with open('answers','w') as outfile:
    for docsrc, path in paths:
        doc = etree.parse(gzip.open(path))
        for category in categories:
                xpath_expr = template.format(**locals())
                for el in doc.xpath(xpath_expr):

                    if el.tag == 'def':
                        children = el.getchildren()

                    elif el.tag == 'ex':
                        children = []
                        for child_el in el.getchildren():
                            if child_el.tag == 'qf':
                                children.extend(child_el.getchildren())
                            else:
                                children.append(child_el)

                    # set default values
                    sentence = []
                    key2indices = defaultdict(set)
                    index = 0
                    mw = False

                    for index, child_el in enumerate(children):

                        tokens += 1


                        if child_el.tag == 'cf':
                            mw = True
                            glob_el = child_el.find('glob')

                            if glob_el is None:
                                token = child_el.text
                            else:
                                token = glob_el.tail

                            sentence.append(token)

                        elif child_el.tag == 'wf':
                            iden = child_el.get('id')
                            id_els = child_el.findall('id')
                            tag = child_el.get('tag')

                            if all([id_els,
                                    tag in {'auto', 'man'}]):

                                token = id_els[-1].tail

                                if tag == 'man':
                                    sensekeys = [(id_el.get('id'), id_el.get('sk'))
                                                 for id_el in id_els]
                                    lemma = id_els[0].get('lemma')

                                    for identifier, sensekey in sensekeys:

                                        training_freq[sensekey] += 1
                                        ir, pos = get_lemma_pos_of_sensekey(sensekey)

                                        instance_id = '{lemma}.{pos}.{docsrc}.{identifier}'.format(**locals())

                                        key2indices[(sensekey, pos)].add((index,
                                                                          lemma,
                                                                          instance_id,
                                                                          docsrc))

                                    key_string = ' '.join([sensekey
                                                           for (identifier, sensekey)
                                                           in sensekeys])
                                    output = '{docsrc} {iden} {key_string}\n'.format(**locals())
                                    outfile.write(output)

                            else:
                                token = child_el.text

                            sentence.append(token)

                    for (sensekey, pos), info in key2indices.items():
                        for (index, lemma, instance_id, docsrc) in info:

                            target_sent = ['<head>%s</head>' % token
                                           if this_index == index else token
                                           for this_index, token in
                                           enumerate(sentence)]

                            target_sent = ' '.join(target_sent)

                            if (lemma, pos) not in lemma_pos:
                                lemma_pos[(lemma, pos)] = defaultdict(dict)

                            identifier = ('pwgc', docsrc, instance_id)
                            lemma_pos[(lemma, pos)][sensekey][target_sent] = identifier

                    # reset variables
                    sentence = []
                    key2indices = defaultdict(set)
                    index = 0


# write all lemma_pos pickle to file
for (lemma, pos), sensekeys in lemma_pos.items():
    path = os.path.join(output_dir, lemma + '___' + pos + '.pickle')
    with open(path, 'wb') as outfile:
        pickle.dump(sensekeys, outfile)

with open('freq_training_examples.pickle', 'wb') as outfile:
    pickle.dump(training_freq, outfile)