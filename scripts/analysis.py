# created or installed modules
from . import configuration
from . import wordnet_utils
from . import utils
import pickle
import os
from collections import defaultdict
from functools import lru_cache
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
from math import log
from scipy import stats
import warnings

warnings.filterwarnings("ignore")
import seaborn as sns


@lru_cache()
class WsdAnalysis:
    """
    class to provide information about a WSD competition:
    1. meta data
    2. basic stats
    3. MFS bias
    4. sense rank vs (relative) frequency
    5. polysemy vs (relative) frequency

    :param str competition: competition to analyze. see global 'competitions'
    in 'configuration.py' for all options
    :param bool exclude_mfs: if set to True, all mfs instances are ignored
    in the analysis
    """

    def __init__(self, competition, exclude_mfs=False):
        self.competition = competition
        self.exclude_mfs = exclude_mfs

        self.info = configuration.get_relevant_paths(self.competition)
        self.gold = {}

        self.sense_rank_d = self.load_sense_rank_dict()
        self.polysemy_d = self.load_polysemy_dict()
        self.iden2lemma = self.load_lexelt()

        self.num_instances = 0
        self.data = {}
        self.sense_ranks = defaultdict(int)
        self.polysemy_all = defaultdict(int)
        self.polysemy = defaultdict(int)
        self.pos_d = defaultdict(int)

        self.process()

        self.mfs_baseline = 100 * (self.sense_ranks[1] / self.num_instances)
        self.avg_num_instances_per_lemma = self.num_instances / len(self.data)
        self.num_of_different_lemmas = len(self.data)
        self.avg_pol_all = wordnet_utils.avg_polysemy(self.polysemy_all)
        self.avg_pol = wordnet_utils.avg_polysemy(self.polysemy)

    def load_lexelt(self):
        """
        every competition should have a file with:
        identifier SPACE lemma.pos

        :rtype: dict
        :return: mapping from identifier -> lemma.pos
        """
        iden2lemma = {}
        if os.path.exists(self.info['lexelt']):
            with open(self.info['lexelt']) as infile:
                for line in infile:
                    identifier, lemma_pos = line.strip().split()
                    iden2lemma[identifier] = lemma_pos

        return iden2lemma

    def metadata(self):
        """
        report metadata from competition

        """
        information = {'competition': self.competition,
                       'wordnet_version': self.info['wn_version'],
                       'answers_downloaded_from': self.info[
                           'answers_downloaded_from'],
                       'date_of_downloading': self.info[
                           'answers_downloaded_at'],
                       'paper': self.info['paper'],
                       'bibtex': self.info['bibtex']}

        # df = pd.DataFrame.from_dict({'categories': list(information.keys()),
        #                             'values': list(information.values())})

        # display(df)
        wordnet_utils.print_dict(information)

    def basic_stats(self):
        """
        print basic stats about competition

        """
        information = dict(competition=self.competition,
                           num_of_instances=self.num_instances,
                           num_of_different_lemmas=len(self.data),
                           MFS_baseline=round(self.mfs_baseline, 2),
                           avg_num_instances_per_lemma=round(
                               self.avg_num_instances_per_lemma, 2),
                           avg_polysemy_all=round(self.avg_pol_all, 2),
                           avg_polysemy=round(self.avg_pol, 2))

        df = pd.DataFrame.from_dict({'categories': list(information.keys()),
                                     'values': list(information.values())})

        display(df)

    def load_sense_rank_dict(self):
        """
        load sense rank dict from cache if existing
        else compute it and save it in cache

        :rtype: dict
        :rtype: mapping wordnet key -> sense rank
        """
        index_sense = self.info['wordnet_path']
        if os.path.exists(self.info['sense_rank_path']):
            sense_rank_d = pickle.load(open(self.info['sense_rank_path'],
                                            'rb'))

        else:
            sense_rank_d = wordnet_utils.get_sense_rank_dict(index_sense)
            with open(self.info['sense_rank_path'], 'wb') as outfile:
                pickle.dump(sense_rank_d, outfile)

        return sense_rank_d

    def load_polysemy_dict(self):
        """
        load polysemy dict from cache if existing
        else compute it and save it in cache

        :rtype: collections.defaultdict
        :return: mapping of (lemma,pos) to number of offsets they refer to
        """
        index_sense = self.info['wordnet_path']
        if os.path.exists(self.info['polysemy_path']):
            polysemy_d = pickle.load(open(self.info['polysemy_path'],
                                          'rb'))

        else:
            polysemy_d = wordnet_utils.load_lemma_pos2offsets(index_sense)
            with open(self.info['polysemy_path'], 'wb') as outfile:
                pickle.dump(polysemy_d, outfile)

        return polysemy_d

    def process(self):
        """
        process answer file from sval competition:
        1. obtain sense rank distribution
        2. obtain polysemy distribution
        3. pos distribution

        """          
        with open(self.info['answers_path']) as infile:
            for line in infile:

                succes, (identifier, lemma, \
                pos, sense_rank, mfs_lfs, keys) = utils.analyze_line(line,
                                                                 self.competition,
                                                                 self.sense_rank_d)

                self.gold[identifier] = {'keys': keys,
                                         'mfs_lfs': mfs_lfs,
                                         'sense_rank': sense_rank,}

                if not succes:
                    continue

                # polysemy info
                pol = self.polysemy_d[(lemma, pos)]
                pol_all = self.polysemy_d[(lemma, 'all')]

                if all([self.exclude_mfs,
                        sense_rank == 1]):
                    continue

                if lemma not in self.data:
                    self.data[lemma] = defaultdict(int)

                self.num_instances += 1
                self.data[lemma][sense_rank] += 1
                self.sense_ranks[sense_rank] += 1
                self.pos_d[pos] += 1
                self.polysemy[pol] += 1
                self.polysemy_all[pol_all] += 1



    def prepare_plot_sense_ranks(self, rel_freq=False):
        """
        plot sense rank distribution

        :param bool rel_freq: if rel_freq is set to True,
        the relative frequencies instead of the absolute values
        """
        self.x = []
        self.y = []
        for key, value in sorted(self.sense_ranks.items()):
            self.x.append(key)
            self.y.append(value)

        if rel_freq:
            self.y = wordnet_utils.rel_freq(self.y)

        self.df = pd.DataFrame.from_dict({'rel_freq': self.y,
                                          'sense_rank_classes': self.x})

        self.x_label = 'sense rank'
        self.y_label = 'frequency'
        if rel_freq:
            self.y_label = 'relative frequency (%)'

        self.title = "Distribution per sense rank (%s)" % self.competition

    def prepare_plot_pos(self, rel_freq=False):
        """
        plot pos distribution

        :param bool rel_freq: if rel_freq is set to True,
        the relative frequencies instead of the absolute values
        """
        self.x = []
        self.y = []
        for key, value in sorted(self.pos_d.items()):
            self.x.append(key)
            self.y.append(value)

        if rel_freq:
            self.y = wordnet_utils.rel_freq(self.y)

        self.df = pd.DataFrame.from_dict({'rel_freq': self.y,
                                          'pos': self.x})

        self.x_label = 'part of speech'
        self.y_label = 'frequency'
        if rel_freq:
            self.y_label = 'relative frequency (%)'

        self.title = "Distribution per part of speech (%s)" % self.competition

    def prepare_plot_polysemy(self, rel_freq=False, pos_independent=False):
        """
        plot pos distribution

        :param bool rel_freq: if rel_freq is set to True,
        the relative frequencies instead of the absolute values
        :param bool pos_independent: if set to True, the polysemy is the sum
        of the polysemy for all pos in wordnet for a lemma, else the polysemy
        is calculated for a specific pos (from the gold standard)
        """
        info = self.polysemy
        if pos_independent:
            info = self.polysemy_all

        self.x = []
        self.y = []
        for key, value in sorted(info.items()):
            self.x.append(key)
            self.y.append(value)

        if rel_freq:
            self.y = wordnet_utils.rel_freq(self.y)

        df = pd.DataFrame.from_dict({'rel_freq': self.y,
                                     'polysemy': self.x})

        # set class attributes
        if pos_independent:
            self.title = "Distribution per polysemy class (pos independent,%s)" % self.competition
        else:
            self.title = "Distribution per polysemy class (pos specific, %s)" % self.competition

        self.x_label = 'polysemy'
        self.y_label = 'frequency'
        if rel_freq:
            self.y_label = 'relative frequency (%)'

        self.df = df

    def plot(self,
             category,
             rel_freq=False,
             pos_independent=False,
             log_it=False):
        """
        create plots, which makes use of the following class attributes:
        1. x_label
        2. y_label
        3. df
        4. title

        :param str category: sense_rank | pos | polysemy

        :param bool rel_freq: if rel_freq is set to True,
        the relative frequencies instead of the absolute values

        :param bool pos_independent: [only needed for polysemy graphs]
        if set to True, the polysemy is the sum
        of the polysemy for all pos in wordnet for a lemma, else the polysemy
        is calculated for a specific pos (from the gold standard)

        :param bool log_it: logarithm of a number is plotted instead of the
        absolute number itself

        """
        if category == 'polysemy':
            self.prepare_plot_polysemy(rel_freq, pos_independent)
            color = 'y'
        elif category == 'sense_rank':
            self.prepare_plot_sense_ranks(rel_freq)
            color = 'b'
        elif category == 'pos':
            self.prepare_plot_pos(rel_freq)
            color = 'g'

        plt.figure(figsize=(16, 8))
        sns.set_style('whitegrid')

        if all([log_it,
                category in {'polysemy', 'sense_rank'}]):
            self.log_x = []
            self.log_y = []
            for x_value, y_value in zip(self.x, self.y):
                if x_value:
                    self.log_x.append(log(x_value))
                    self.log_y.append(log(y_value))

            ax = sns.pointplot(x=self.log_x,
                               y=self.log_y,
                               data=self.df)

            slope, intercept, r_value, p_value, std_err = stats.linregress(
                self.log_x,
                self.log_y)

            r_squared = pow(r_value, 2)

            debug = False
            if debug:
                print()
                print('r-squared:" %s' % r_squared)
                print('p-value: %s' % p_value)

            ax.set_title('log of ' + self.title)

            ax.set_xlabel('log of ' + self.x_label)
            ax.set_ylabel('log of ' + self.y_label)


            # return r_squared, self.y, self.df

        else:

            ax = sns.barplot(x=self.x, y=self.y, data=self.df,
                             color=color)

            ax.set_title(self.title)

            ax.set_xlabel(self.x_label)
            ax.set_ylabel(self.y_label)

            plt.legend(loc=7)



