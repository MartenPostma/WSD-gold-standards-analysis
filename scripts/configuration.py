# stdlib
import os
import ast
from . import wordnet_utils as utils

with open('competitions.txt') as infile:
    competitions = ast.literal_eval(infile.read())


def show_possibilities():
    """
    show user possible competitions
    """
    information = {}
    for competition, value in competitions.items():
        information[competition] = value['paper']

    # df = pd.DataFrame.from_dict({'categories': list(information.keys()),
    #                             'values': list(information.values())})

    # display(df)
    utils.print_dict(information)


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
