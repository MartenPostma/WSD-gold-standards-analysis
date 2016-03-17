from . import analysis

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, HTML

def compare_basic_stats(competitions,basic_stat):
    """

    :param list competition: competitions to analyze. see global 'competitions'
    in 'configuration.py' for all options

    :param str basic_stats: options include: 'num_of_instances',
    'num_of_different_lemmas', 'mfs_baseline', 'type_token_ratio'
    """
    x = []
    y = []

    for competition in competitions:

        instance = analysis.WSD_analysis(competition)
        y_value = getattr(instance,basic_stat)

        x.append(competition)
        y.append(y_value)

    df = pd.DataFrame.from_dict({'competitions': x,
                                 'values': y})

    sns.set_style('whitegrid')
    ax = sns.barplot(x="competitions", y="values", data=df)
    x_label = 'competition'
    y_label = basic_stat
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title("Comparison of competitions %s for %s" % (' '.join(competitions),
                                                           basic_stat))
    plt.legend(loc=7)

def compare_properties(competitions,category,rel_freq=False,pos_independent=False):
    """
    plot comparison of competitions for : sense_rank | polysemy | pos

    :param list competition: competitions to analyze. see global 'competitions'
    in 'configuration.py' for all options

    :param str category: sense_rank | polysemy | pos

    :param bool rel_freq: if rel_freq is set to True,
        the relative frequencies instead of the absolute values

    :param bool pos_independent: [only needed for polysemy graphs]
        if set to True, the polysemy is the sum
        of the polysemy for all pos in wordnet for a lemma, else the polysemy
        is calculated for a specific pos (from the gold standard)
    """

    x_values = []
    y_values = []
    hue_values = []

    for competition in competitions:

        instance = analysis.WSD_analysis(competition)

        if category == 'polysemy':
            instance.prepare_plot_polysemy(rel_freq,pos_independent)
        elif category == 'sense_rank':
            instance.prepare_plot_sense_ranks(rel_freq)
        elif category == 'pos':
            instance.prepare_plot_pos(rel_freq)

        x_values.extend(instance.x)
        y_values.extend(instance.y)
        labels = [instance.competition for _ in instance.x]
        hue_values.extend(labels)

    df = pd.DataFrame.from_dict({'x_values': x_values,
                                 'y_values': y_values,
                                 'hue_values' : hue_values})

    sns.set_style('whitegrid')
    ax = sns.barplot(x="x_values", y="y_values", hue='hue_values', data=df)
    x_label = instance.x_label
    y_label = instance.y_label
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title("Comparison of competitions %s for %s" % (' '.join(competitions),
                                                           category))
    plt.legend(loc=7)
