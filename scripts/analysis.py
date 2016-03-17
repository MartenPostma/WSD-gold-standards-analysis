#stdlib
import pickle
import os
from collections import defaultdict

import warnings
warnings.filterwarnings("ignore")

#created or installed modules
from . import configuration
from . import wordnet_utils as utils

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, HTML

class WSD_analysis:
    """
    class to provide information about a WSD competition:
    1. meta data
    2. basic stats
    3. MFS bias
    4. sense rank vs (relative) frequency
    5. polysemy vs (relative) frequency

    :param str competition: competition to analyze. options include:
    'se2-ls',
    """
    def __init__(self,competition):
        self.competition = competition
        self.info = configuration.get_relevant_paths(self.competition)

        self.load_sense_rank_dict()
        self.load_polysemy_dict()
        self.process()

    def metadata(self):
        """
        report metadata from competition

        """
        information = {'competition': self.competition,
                       'wordnet_version' : self.info['wn_version'],
                       'answers_downloaded_from' : self.info['answers_downloaded_from'],
                       'date_of_downloading' : self.info['answers_downloaded_at'],
                       'paper' : self.info['paper'],
                       'bibtex' : self.info['bibtex']}

        df = pd.DataFrame.from_dict({'categories': list(information.keys()),
                                     'values': list(information.values())})

        display(df)

    def basic_stats(self):
        """
        print basic stats about competition

        """
        information = {'competition': self.competition,
                       'num_of_instances' : self.num_instances,
                       'num_of_different_lemmas' : len(self.data),
                       'MFS baseline' : round(self.mfs_baseline,2),
                       'type_token_ratio': round(self.type_token_ratio,2)}

        df = pd.DataFrame.from_dict({'categories': list(information.keys()),
                                     'values': list(information.values())})

        display(df)


    def load_sense_rank_dict(self):
        """
        load sense rank dict from cache if existing
        else compute it and save it in cache
        """
        index_sense = self.info['wordnet_path']
        if os.path.exists(self.info['sense_rank_path']):
            self.sense_rank_d = pickle.load(open(self.info['sense_rank_path'],
                                                 'rb'))

        else:
            self.sense_rank_d = utils.get_sense_rank_dict(index_sense)
            with open(self.info['sense_rank_path'],'wb') as outfile:
                pickle.dump(self.sense_rank_d,outfile)

    def load_polysemy_dict(self):
        """
        load polysemy dict from cache if existing
        else compute it and save it in cache
        """
        index_sense = self.info['wordnet_path']
        if os.path.exists(self.info['polysemy_path']):
            self.polysemy_d = pickle.load(open(self.info['polysemy_path'],
                                                 'rb'))

        else:
            self.polysemy_d = utils.load_lemma_pos2offsets(index_sense)
            with open(self.info['polysemy_path'],'wb') as outfile:
                pickle.dump(self.polysemy_d,outfile)

    def process(self):
        """
        process answer file from sval competition:
        1. obtain sense rank distribution
        2. [todo]: obtain polysemy distribution
        3. [todo]: pos distribution

        """
        self.num_instances = 0
        self.data = {}
        self.sense_ranks = defaultdict(int)

        self.polysemy_all = defaultdict(int)
        self.polysemy = defaultdict(int)
        self.pos_d = defaultdict(int)

        with open(self.info['answers_path']) as infile:
            for line in infile:

                #lemma info
                #the variables id1 and id2 are so general because the information
                #in those fields are not the same for all competitions
                id1,id2,*keys = line.strip().split()

                if keys == ['U']:
                    continue

                self.num_instances += 1

                #pos and lemma info
                lemma, pos = utils.determine_lemma_pos(keys)

                if self.competition == 'se2-ls':
                    lemma = id2.split('.')[0]

                if lemma not in self.data:
                    self.data[lemma] = defaultdict(int)

                #sense rank info
                sense_rank = 0
                sense_ranks = [self.sense_rank_d[key]
                               for key in keys
                               if key in self.sense_rank_d]
                if sense_ranks:
                    sense_rank = min(sense_ranks)

                #polysemy info
                pol = self.polysemy_d[(lemma,pos)]
                pol_all = self.polysemy_d[(lemma,'all')]

                self.data[lemma][sense_rank] += 1
                self.sense_ranks[sense_rank] += 1
                self.pos_d[pos] += 1
                self.polysemy[pol] += 1
                self.polysemy_all[pol_all] += 1

        self.mfs_baseline = 100 * (self.sense_ranks[1]/self.num_instances)
        self.type_token_ratio = self.num_instances/len(self.data)

    def rel_freq(self,list_of_freqs):
        """
        given list of frequencies, return return relative frequencies

        >>> rel_freq([1,2,3,4])
        [10, 20, 30, 40]

        :param list list_of_freqs: list of numbers

        :rtype: list
        :return: list of relative frequencies
        """
        total = sum(list_of_freqs)
        return [100 * (freq/total)
                for freq in list_of_freqs]

    def plot_sense_ranks(self,rel_freq=False):
        """
        plot sense rank distribution

        :param bool rel_freq: if rel_freq is set to True,
        the relative frequencies instead of the absolute values
        """
        x = list(self.sense_ranks.keys())
        y = list(self.sense_ranks.values())
        if rel_freq:
            y = self.rel_freq(y)

        df = pd.DataFrame.from_dict({'rel_freq': y,
                                     'sense_rank_classes': x})


        sns.set_style('whitegrid')
        ax = sns.barplot(x="sense_rank_classes", y="rel_freq", data=df)
        x_label = 'sense rank'
        y_label = 'frequency'
        if rel_freq:
            y_label = 'relative frequency (%)'

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title("Distribution per sense rank (%s)" % self.competition)
        plt.legend(loc=7)

    def plot_pos(self,rel_freq=False):
        """
        plot pos distribution

        :param bool rel_freq: if rel_freq is set to True,
        the relative frequencies instead of the absolute values
        """
        x = list(self.pos_d.keys())
        y = list(self.pos_d.values())
        if rel_freq:
            y = self.rel_freq(y)

        df = pd.DataFrame.from_dict({'rel_freq': y,
                                     'pos': x})


        sns.set_style('whitegrid')
        ax = sns.barplot(x="pos", y="rel_freq", data=df)
        x_label = 'part of speech'
        y_label = 'frequency'
        if rel_freq:
            y_label = 'relative frequency (%)'

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title("Distribution per part of speech (%s)" % self.competition)
        plt.legend(loc=7)


    def plot_polysemy(self,rel_freq=False,pos_independent=False):
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

        x = list(info.keys())
        y = list(info.values())
        if rel_freq:
            y = self.rel_freq(y)

        df = pd.DataFrame.from_dict({'rel_freq': y,
                                     'polysemy': x})



        sns.set_style('whitegrid')
        plt.figure(figsize=(16, 8))
        ax = sns.barplot(x="polysemy", y="rel_freq", data=df)
        x_label = 'polysemy'
        y_label = 'frequency'
        if rel_freq:
            y_label = 'relative frequency (%)'

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        if pos_independent:
            ax.set_title("Distribution per polysemy class (pos independent,%s)" % self.competition)
        else:
            ax.set_title("Distribution per polysemy class (pos specific, %s)" % self.competition)

        plt.legend(loc=7)