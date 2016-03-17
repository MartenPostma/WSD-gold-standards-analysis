#stdlib
import os

#installed or created modules
import pandas as pd
from IPython.display import display, HTML

competitions = {'se2-ls': { 'wn_version': '171',
                            'fullname' : 'SensEval 2 English lexical sample task',
                            'answers_downloaded_from' : 'http://www.hipposmond.com/senseval2/',
                            'answers_downloaded_at' : '16-3-2016',
                            'paper' : 'http://aclweb.org/anthology/S01-1004',
                            'bibtex' : 'http://aclanthology.info/papers/english-lexical-sample-task-description.bib'},
                'se2-aw': { 'wn_version': '171',
                            'fullname' : 'SensEval 2 English all words task',
                            'answers_downloaded_from' : 'http://www.hipposmond.com/senseval2/',
                            'answers_downloaded_at' : '16-3-2016',
                            'paper' : 'http://aclweb.org/anthology/S01-1005',
                            'bibtex' : 'http://aclanthology.info/papers/english-tasks-all-words-and-verb-lexical-sample.bib'},
                'se3-aw': { 'wn_version': '171',
                            'fullname' : 'The English all words task',
                            'answers_downloaded_from' : 'http://www.senseval.org/senseval3/data.html',
                            'answers_downloaded_at' : '18-3-2016',
                            'paper' : 'http://aclweb.org/anthology/W04-0811',
                            'bibtex' : 'http://aclanthology.info/papers/the-english-all-words-task.bib'},
}

def show_possibilities():
    """
    show user possible competitions
    """
    information = {}
    for competition,value in competitions.items():
        information[competition] = value['paper']

    df = pd.DataFrame.from_dict({'categories': list(information.keys()),
                                 'values': list(information.values())})

    display(df)


def get_relevant_paths(competition):
    '''
    returns dict of paths that are relevant for the analyses
    for all-words (aw) competitions and lexical sample competitions (ls)
    
    :param str competition: competition to analyze. options include:
    'se2-ls',
    
    :rtype: dict
    :return: dict mapping to relevant paths
    '''
    main_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    wn_version = competitions[competition]['wn_version']
    wordnet_path = os.path.join(main_dir,
                                'wordnets',
                                'index.sense.%s' % wn_version)

    log_path = os.path.join(main_dir,'scripts','cache',competition)
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
                                'key')

    info = dict(wordnet_path=wordnet_path, log_path=log_path,
                sense_rank_path=sense_rank_path, polysemy_path=polysemy_path,
                answers_path=answers_path)
    info.update(competitions[competition])
    return info
