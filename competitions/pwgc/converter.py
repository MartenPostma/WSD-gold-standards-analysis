'''
goal is to convert the princeton wordnet gloss corpus
into the following format
DOCUMENT_ID LEMMA.IDENTIFIER KEY1 KEY2 KEYN
'''

#lemma is of format: "great%1|great%3"
#focus on 'gloss' and 'ex' elements
#there can be more than one sense key

#gunzip WordNet-3.0.gz before running this script

from lxml import etree
from collections import defaultdict
import gzip

sw_template = 'synset/gloss/{category}/wf[@tag="man"]'
mw_template = 'synset/gloss/{category}/cf/glob[@tag="man"]'
basedir = 'WordNet-3.0/glosstag/merged'
basenames = ['adj.xml.gz', 'adv.xml.gz','noun.xml.gz','verb.xml.gz']
paths = [ (basename[:-4], '/'.join([basedir,basename]))
          for basename in basenames]
categories = ['def','ex']


stats = defaultdict(int)

with open('answers','w') as outfile:
    for doc_id, path in paths:
        doc = etree.parse(gzip.open(path))
        for category in categories:
            for template in [sw_template,mw_template]:
                xpath_expr = template.format(**locals())
                for el in doc.xpath(xpath_expr):

                    iden = el.get('id')
                    sensekeys = [id_el.get('sk')
                                 for id_el in el.iterfind('id')]

                    if not sensekeys:
                        continue


                    key_string = ' '.join(sensekeys)
                    output = '{doc_id} {iden} {key_string}\n'.format(**locals())
                    outfile.write(output)

                    stats[(category,template)] += 1

for key,value in stats.items():
    print(key,value)

print('totat: %s' % sum(stats.values()))







