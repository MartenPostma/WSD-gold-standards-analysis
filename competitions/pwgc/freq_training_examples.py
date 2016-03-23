from collections import defaultdict
import pickle


training_freq = defaultdict(int)

with open('answers') as infile:
    for line in infile:
        id1, id2, *keys = line.strip().split()

        if any([keys == ['U'],
        '%' not in line,
        not keys]):
            continue


        for key in keys:
            training_freq[key] += 1


with open('freq_training_examples.pickle', 'wb') as outfile:
    pickle.dump(training_freq, outfile)
