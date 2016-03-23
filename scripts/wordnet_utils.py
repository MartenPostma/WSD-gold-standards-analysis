# stdlib
from functools import lru_cache
from collections import defaultdict


def get_sense_rank_dict(path_to_index_sense):
    """
    create mapping sense key -> sense rank
    casuistical%3:01:01:: 03053657 1 0 -> casuistical%3:01:01:: -> 1

    :param str path_to_index_sense: wordnet index sense file

    :rtype: dict
    :rtype: mapping wordnet key -> sense rank
    """
    sense_ranks = {}
    with open(path_to_index_sense) as infile:
        for line in infile:
            key, offset, sqr, freq = line.strip().split()
            sense_ranks[key] = int(sqr)

    return sense_ranks


def load_lemma_pos2offsets(path_to_index_sense):
    """
    given with index.sense from wordnet distributions such as
    casuistical%3:01:01:: 03053657 1 0

    this function returns a dictionary mapping (lemma,pos)
    to number the offsets they can refer to.

    :param str path_to_index_sense: path to wordnet index.sense file

    :rtype: collections.defaultdict
    :return: mapping of (lemma,pos) to number of offsets they refer to
    """
    lemmapos2offsets = defaultdict(int)
    with open(path_to_index_sense) as infile:
        for line in infile:
            key, offset, sqr, freq = line.strip().split()
            lemma, pos = get_lemma_pos_of_sensekey(key)

            if pos != 'u':
                lemmapos2offsets[(lemma, pos)] += 1
                lemmapos2offsets[(lemma, 'all')] += 1

    return lemmapos2offsets


def determine_lemma_pos(list_of_sensekeys):
    """

    :param list list_of_sensekeys: list of wordnet sensekeys

    :rtype: str
    :return: n | v  | a | r | u
    """
    lemma_pos_values = [get_lemma_pos_of_sensekey(sense_key)
                        for sense_key in list_of_sensekeys]
    lemmas, pos_values = zip(*lemma_pos_values)

    if len(set(lemmas)) == 1:
        lemma = lemmas[0]
    else:
        lemma = min(lemmas, key=len)

    set_pos_values = set(pos_values)
    if 'u' in set_pos_values:
        set_pos_values.remove('u')

    if len(set(set_pos_values)) == 1:
        pos = pos_values[0]
    else:
        pos = 'u'

    return lemma, pos


@lru_cache()
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


def rel_freq(list_of_freqs):
    """
    given list of frequencies, return return relative frequencies

    .. doctest::
        >>> rel_freq([1, 2, 3, 4])
        [10, 20, 30, 40]

    :param list list_of_freqs: list of numbers

    :rtype: list
    :return: list of relative frequencies
    """
    total = sum(list_of_freqs)
    return [100 * (freq / total)
            for freq in list_of_freqs]


def avg_polysemy(polysemy_dict):
    """
    compute average polysemy

    .. doctest::
        >>> avg_polysemy(defaultdict(int, {1: 2, 2: 2}))
        1.5

    :param collections.defaultdict polysemy_dict: mapping from polysemy class
    to number of instances in that class

    :rtype: float
    :return: average polysemy
    """
    numerator = sum([key * value for key, value in polysemy_dict.items()])
    denominator = sum(polysemy_dict.values())

    return numerator / denominator


def print_dict(d):
    """

    :param dict d: a dictionary
    """
    longest_key = max(d, key=len)

    length = len(longest_key) + 1

    for key, value in d.items():
        space = ' ' * (length - len(key))

        print(key + space + '| ' + value)
