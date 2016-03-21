# stdlib
import os

# installed or created modules
import pandas as pd
from IPython.display import display

competitions = {'se2-ls': {'wn_version': '171',
                           'fullname': 'SensEval 2 English lexical sample task',
                           'answers_downloaded_from': 'http://www.hipposmond.com/senseval2/',
                           'answers_downloaded_at': '16-3-2016',
                           'paper': 'http://aclweb.org/anthology/S01-1004',
                           'bibtex': 'http://aclanthology.info/papers/english-lexical-sample-task-description.bib'},
                'se2-aw': {'wn_version': '171',
                           'fullname': 'SensEval 2 English all words task',
                           'answers_downloaded_from': 'http://www.hipposmond.com/senseval2/',
                           'answers_downloaded_at': '16-3-2016',
                           'paper': 'http://aclweb.org/anthology/S01-1005',
                           'bibtex': 'http://aclanthology.info/papers/english-tasks-all-words-and-verb-lexical-sample.bib'},
                'se3-aw': {'wn_version': '171',
                           'fullname': 'The English all words task',
                           'answers_downloaded_from': 'http://www.senseval.org/senseval3/data.html',
                           'answers_downloaded_at': '18-3-2016',
                           'paper': 'http://aclweb.org/anthology/W04-0811',
                           'bibtex': 'http://aclanthology.info/papers/the-english-all-words-task.bib'},
                'se3-ls': {'wn_version': '171',
                           'fullname': 'The English lexical sample task',
                           'answers_downloaded_from': 'http://www.senseval.org/senseval3/data.html',
                           'answers_downloaded_at': '18-3-2016',
                           'paper': 'http://aclweb.org/anthology/W04-0807',
                           'bibtex': 'http://aclanthology.info/papers/the-senseval-3-english-lexical-sample-task.bib'},
                'sem2007-aw': {'wn_version': '21',
                               'fullname': 'SemEval-2007 Task-17: English Lexical Sample, SRL and All Words',
                               'answers_downloaded_from': 'https://github.com/rubenIzquierdo/wsd_corpora/tree/master/semeval2007_task17_allwords',
                               'answers_downloaded_at': '18-3-2016',
                               'paper': 'http://aclweb.org/anthology/S07-1016',
                               'bibtex': 'http://aclanthology.info/papers/semeval-2007-task-17-english-lexical-sample-srl-and-all-words.bib'},
                'sem2013-aw': {'wn_version': '30',
                               'fullname': 'Multilingual Word Sense Disambiguation',
                               'answers_downloaded_from': 'https://www.cs.york.ac.uk/semeval-2013/task12.html',
                               'answers_downloaded_at': '18-3-2016',
                               'paper': 'http://aclweb.org/anthology/S13-2040',
                               'bibtex': 'http://aclanthology.info/papers/semeval-2013-task-12-multilingual-word-sense-disambiguation.bib'},
                'sem2015-aw': {'wn_version': '30',
                               'fullname': 'Multilingual All-Words Sense Disambiguation and Entity Linking',
                               'answers_downloaded_from': 'http://alt.qcri.org/semeval2015/task13/index.php?id=data-and-tools',
                               'answers_downloaded_at': '18-3-2016',
                               'paper': 'http://aclweb.org/anthology/S15-2049',
                               'bibtex': 'http://aclanthology.info/papers/semeval-2015-task-13-multilingual-all-words-sense-disambiguation-and-entity-linking.bib'},
                'semcor16': {'wn_version': '16',
                             'fullname': 'SemCor',
                             'answers_downloaded_from': 'http://web.eecs.umich.edu/~mihalcea/downloads.html#semcor',
                             'answers_downloaded_at': '18-3-2016',
                             'paper': 'http://aclweb.org/anthology/H93-1061',
                             'bibtex': 'http://aclanthology.info/papers/a-semantic-concordance.bib'},
                'pwgc': {'wn_version': '30',
                         'fullname': 'Princeton WordNet Gloss Corpus',
                         'answers_downloaded_from': 'http://wordnetcode.princeton.edu/glosstag-files/WordNet-3.0-glosstag.zip',
                         'answers_downloaded_at': '21-3-2016',
                         'paper': 'http://wordnetcode.princeton.edu/glosstag-files/Readme.txt',
                         'bibtex': 'no bibtex found'},
                'reuters': {'wn_version': '171',
                            'fullname': 'Reuters',
                            'answers_downloaded_from': 'http://www.dianamccarthy.co.uk/downloads/hlt2005releasev2.tgz',
                            'answers_downloaded_at': '21-3-2016',
                            'paper': 'http://aclweb.org/anthology/H05-1053',
                            'bibtex': 'http://aclanthology.info/papers/domain-specific-sense-distributions-and-predominant-sense-acquisition.bib'},
                'wordnet30': {'wn_version': '30',
                            'fullname': 'Wordnet version 3.0',
                            'answers_downloaded_from': 'http://wordnetcode.princeton.edu/3.0/WordNet-3.0.tar.gz',
                            'answers_downloaded_at': '21-3-2016',
                            'paper': 'http://aclweb.org/anthology/H94-1111',
                            'bibtex': 'http://aclanthology.info/papers/wordnet-a-lexical-database-for-english-h94-1111.bib'}
                }


def show_possibilities():
    """
    show user possible competitions
    """
    information = {}
    for competition, value in competitions.items():
        information[competition] = value['paper']

    df = pd.DataFrame.from_dict({'categories': list(information.keys()),
                                 'values': list(information.values())})

    display(df)


def get_relevant_paths(competition):
    """
    returns dict of paths that are relevant for the analyses
    for all-words (aw) competitions and lexical sample competitions (ls)

    :param str competition: competition to analyze. see global 'competitions'
    in 'configuration.py' for all options

    :rtype: dict
    :return: dict mapping to relevant paths
    """
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    wn_version = competitions[competition]['wn_version']
    wordnet_path = os.path.join(main_dir,
                                'wordnets',
                                'index.sense.%s' % wn_version)

    log_path = os.path.join(main_dir, 'scripts', 'cache', competition)
    sense_rank_path = os.path.join(main_dir,
                                   'scripts',
                                   'cache',
                                   wn_version + '.' + 'sense_rank')

    polysemy_path = os.path.join(main_dir,
                                 'scripts',
                                 'cache',
                                 wn_version + '.' + 'polysemy')

    answers_path = os.path.join(main_dir,
                                'competitions',
                                competition,
                                'answers')

    info = dict(wordnet_path=wordnet_path, log_path=log_path,
                sense_rank_path=sense_rank_path, polysemy_path=polysemy_path,
                answers_path=answers_path)
    info.update(competitions[competition])
    return info
