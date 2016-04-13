from scripts import utils
from scripts import analysis
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display

class Score:
    """
    class to score output from a semeval competition and
    visualize the performance with respect to sense rank and mfs

    """
    def __init__(self, *args, competition='sem2013-aw'):
        self.gold_instance = analysis.WsdAnalysis(competition)
        self.competition = competition
        self.results = {}

        for system_name, system_path in args:
            system = self.load(system_path)
            self.score_system(system_name, system)

        self.load_into_data_frame()

    def load(self, system_path):
        """
        load mapping from identifier to sensekeys from system output

        :param str system_path: path to system output from a semeval competition
        """
        system = {}
        with open(system_path) as infile:
            for line in infile:
                succes, (identifier, lemma, pos, \
                sense_rank, mfs, keys) = utils.analyze_line(line,
                                                            self.competition,
                                                            self.gold_instance.sense_rank_d)


                if succes:
                    system[identifier] = keys

        return system

    def score_system(self, system_name, system):
        """
        The following steps are executed and
        1. precision
        2. recall
        3. percentage attempted
        4. mapping 'list_attempted' -> list of Trues and Falses
        5. mapping 'list_scored_instances' -> list of Trues and Falses
        6. mapping 'performance_sense_ranks' -> 'sense_rank' -> list of Trues and Falses
        7. mapping 'mfs_lfs' -> 'mfs | lfs' -> list of Trues and Falses

        :param str system_name: name of system run
        :param dict system: mapping identifier to sensekeys
        """
        self.results[system_name] = {
            'list_attempted': [],
            'list_scored_instances': [],
            'performance_sense_ranks': defaultdict(list),
            'mfs_lfs': defaultdict(list)
        }

        for identifier, info in self.gold_instance.gold.items():
            attempted = False
            correct = False
            gold_keys = info['keys']
            sense_rank = info['sense_rank']
            if sense_rank >= 10:
                sense_rank = '10>'
            sense_rank = str(sense_rank)

            mfs_lfs = info['mfs_lfs']

            if identifier in system:
                attempted = True
                correct = any([system_key in gold_keys
                               for system_key in system[identifier]])

            self.results[system_name]['list_attempted'].append(attempted)
            self.results[system_name]['list_scored_instances'].append(correct)
            self.results[system_name]['performance_sense_ranks'][sense_rank].append(correct)
            self.results[system_name]['mfs_lfs'][mfs_lfs].append(correct)

        num_correct = sum(self.results[system_name]['list_scored_instances'])
        num_attempted = len(self.results[system_name]['list_attempted'])
        num_instances = len(self.gold_instance.gold)
        precision = 100 * (num_correct / num_attempted)
        recall = 100 * (num_correct /  num_instances)
        perc_attempted = 100 * (num_attempted / num_instances)

        self.results[system_name]['precision'] = precision
        self.results[system_name]['recall'] = recall
        self.results[system_name]['perc_attempted'] = perc_attempted


    def load_into_data_frame(self):
        """

        load data frames
        """
        the_sense_rank_classes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10>']
        the_mfs_lfs_classes = ['mfs', 'lfs']

        sense_ranks_classes = []
        sense_ranks_performance = []
        mfs_lfs_classes = []
        mfs_lfs_performance = []
        system_labels_sense_ranks = []
        system_labels_mfs_lfs = []


        for system_name, result in self.results.items():

            # update sense rank info
            sense_ranks_classes.extend(the_sense_rank_classes)
            system_labels_sense_ranks.extend([system_name for _ in range(len(the_sense_rank_classes))])

            for sense_rank in the_sense_rank_classes:
                num_correct = sum(result['performance_sense_ranks'][sense_rank])
                num_instances = len(result['performance_sense_ranks'][sense_rank])

                if num_correct:
                    perf_sense_rank_class = 100 * (num_correct / num_instances)

                else:
                    perf_sense_rank_class = 0.0
                sense_ranks_performance.append(perf_sense_rank_class)

            # update mfs info
            mfs_lfs_classes.extend(the_mfs_lfs_classes)
            system_labels_mfs_lfs.extend([system_name for _ in range(len(the_mfs_lfs_classes))])

            for mfs_or_lfs in the_mfs_lfs_classes:
                num_correct = sum(result['mfs_lfs'][mfs_or_lfs])
                num_instances = len(result['mfs_lfs'][mfs_or_lfs])

                if num_correct:
                    perf_mfs_lfs_class = 100 * (num_correct / num_instances)

                else:
                    perf_mfs_lfs_class = 0.0
                mfs_lfs_performance.append(perf_mfs_lfs_class)

        self.df_rank = pd.DataFrame.from_dict({
            'sense_ranks_classes': sense_ranks_classes,
            'sense_ranks_performance': sense_ranks_performance,
            'system_labels': system_labels_sense_ranks})

        self.df_mfs = pd.DataFrame.from_dict({
            'mfs_lfs_classes': mfs_lfs_classes,
            'mfs_lfs_performance': mfs_lfs_performance,
            'system_labels': system_labels_mfs_lfs})

    def general_results(self):
        """
        show general results
        """
        system_names = []
        precision = []
        recall = []
        perc_attempted = []

        for system_name, result in self.results.items():

            system_names.append(system_name)
            precision.append(round(result['precision'],2))
            recall.append(round(result['recall'],2))
            perc_attempted.append(result['perc_attempted'])

        self.df_results = pd.DataFrame.from_dict({
            '1. system': system_names,
            '2. precision': precision,
            '3. recall': recall,
            '4. % attempted': perc_attempted})

        display(self.df_results)


    def plot_mfs_lfs_performance(self):
        """

        """
        sns.set_style('whitegrid')
        ax = sns.barplot(x="mfs_lfs_classes", y="mfs_lfs_performance",
                         hue='system_labels', data=self.df_mfs)
        x_label = 'MFS or LFS'
        y_label = '% correct'
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title("% Correct for MFS or LFS")
        plt.legend(loc=7)


    def plot_sense_rank_performance(self):
        """

        """
        sns.set_style('whitegrid')
        ax = sns.barplot(x="sense_ranks_classes", y="sense_ranks_performance",
                         hue='system_labels', data=self.df_rank)
        x_label = '% correct per sense rank'
        y_label = '% correct'
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title("% Correct per sense rank")
        plt.legend(loc=7)

