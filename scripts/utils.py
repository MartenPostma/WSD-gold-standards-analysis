from . import wordnet_utils


def compute_perc_correct(lijst):
    """

    :param list lijst: list of booleans
    :rtype: float
    :return: percentage correct
    """
    if not lijst:
        return 0.0

    correct = sum(lijst)
    num_instances = len(lijst)

    perc_correct = correct / num_instances

    return perc_correct

def analyze_line(line, competition, sense_rank_d):
    """
    analyze one line of a semeval gold standard and return:
    1. identifier
    2. lemma
    3. pos
    4. sense_rank gold keys (lowest if there is more than one sensekey)
    5. sensekeys

    :param str line: one line of a semeval gold standard
    :param str competition: check global variable 'competitions'
    from module 'configuration' for info on available competitions
    :param collections.defaultdict sense_rank_d: mapping from wordnet
    sensekey to senserank

    :rtype: tuple
    :return: (succes, (identifier, lemma, pos, sense_rank (int), mfs, sensekeys)
    """
    id1, id2, *keys = line.strip().split()
    mfs_lfs = 'mfs'

    if competition == 'sem2015-aw':
        keys = [key[3:]
                for key in keys
                if key.startswith('wn:')]

    if any([keys == ['U'],
            '%' not in line,
            not keys]):
        return (False, ('', '', '', '', '', ''))

    # pos and lemma info
    lemma, pos = wordnet_utils.determine_lemma_pos(keys)

    if competition in {'se2-ls',
                        'se3-ls',
                        'sem2007-aw',
                        'semcor16',
                        'reuters',
                        'wordnet30'}:
        lemma = id2.split('.')[0]

    # sense rank info
    sense_rank = 0
    sense_ranks = [sense_rank_d[key]
                   for key in keys
                   if key in sense_rank_d]
    if sense_ranks:
        sense_rank = min(sense_ranks)

        if sense_rank >= 2:
            mfs_lfs = 'lfs'
    identifier = id2


    return (True, (identifier, lemma, pos, sense_rank, mfs_lfs, keys))