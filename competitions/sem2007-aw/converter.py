'''
goal is to convert the sem2007-aw corpus from
https://github.com/rubenIzquierdo/wsd_corpora/tree/master/semeval2007_task17_allwords
(last visited at 18-3-2016)
into the following format
DOCUMENT_ID LEMMA.IDENTIFIER KEY1 KEY2 KEYN
'''
from lxml import etree

with open('answers','w') as outfile:
    for path in ['d00.naf','d01.naf','d02.naf']:
        doc = etree.parse(path)
        xml_path = 'terms/term/externalReferences/externalRef[@reftype="sense"]'

        for ext_ref_el in doc.xpath(xml_path):

            key = ext_ref_el.get('reference')
            iden = ext_ref_el.getprevious().get('reference')
            doc_id = iden.split('.')[0]
            lemma = ext_ref_el.getparent().getparent().get('lemma')
            output = '{doc_id} {lemma}.{iden} {key}\n'.format(**locals())
            outfile.write(output)
