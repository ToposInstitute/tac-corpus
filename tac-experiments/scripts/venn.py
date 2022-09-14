import argparse
import matplotlib.pyplot as plt

from extract_keywords import get_keywords
from functools import reduce
from more_itertools import powerset
from supervenn import supervenn

parser = argparse.ArgumentParser(description='Construct a visualization')
parser.add_argument('targets', nargs='+', choices=['textrank', 'parmenides',
    'opentapioca', 'dygie', 'author', 'nlab', 'nps'])
parser.add_argument('--min-width', '-m', type=int, default=50)
parser.add_argument('--ratio', '-r', type=float)
parser.add_argument('--output', '-o', default='visualizations/supervenn.png')

def build_sets(targets):

    sets = {}

    if 'textrank' in targets:
        sets['textrank'] = get_keywords('processed/textrank_extractive.txt')
    if 'parmenides' in targets:
        sets['parmenides'] = \
                get_keywords('processed/parmenides_extractive.txt')
    if 'opentapioca' in targets:
        sets['opentapioca'] = \
                get_keywords('processed/opentapioca_extractive.txt')
    if 'dygie' in targets:
        sets['dygie'] = get_keywords('processed/dygie_extractive.txt')
    if 'author' in targets:
        sets['author'] = get_keywords('processed/author_extractive.txt')
    if 'nlab' in targets:
        sets['nlab'] = get_keywords('processed/nlab_extractive.txt')
    if 'nps' in targets:
        sets['nps'] = get_keywords('processed/nps_extractive.txt')

    return sets

def combine(set1, set2):

    name1, set1 = set1
    name2, set2 = set2

    return (name1 + '+' + name2, set1 & set2)

def combine_union(set1, set2):

    name1, set1 = set1
    name2, set2 = set2

    return (name1 + '+' + name2, set1 | set2)

MAPPING = {
    'textrank': 'TextRank',
    'nlab': 'NLab Titles',
    'author': 'Author Keywords',
    'dygie': 'DyGIE++',
    'opentapioca': 'OpenTapioca',
    'parmenides': 'Parmenides',
    'nps': 'Simple Noun Phrases',
}

def map_label(label):

    return MAPPING[label]

def powerset_complement(sequence):

    sequence = list(sequence)

    x = len(sequence)
    for i in range(1 << x):
        yield ([sequence[j] for j in range(x) if (i & (1 << j))], 
                [sequence[j] for j in range(x) if not (i & (1 << j))])

def main():

    options = parser.parse_args()

    sets = build_sets(options.targets)
    combinations = powerset_complement(sets.items())

    for (combination, complement) in combinations:
        if len(combination) >= 1:
            (name, combined_set) = reduce(combine, combination)
            combo_names = [x[0] for x in combination]
            if len(complement) >= 1:
                compl_names = [x[0] for x in complement]
                (_, complement_set) = reduce(combine_union, complement)
                combined_set = combined_set - complement_set
            with open(name + '.txt', 'w') as outfile:
                for item in combined_set:
                    outfile.write(item + '\n')
            #print("%s (%d elements)" % (name, len(combined_set)))
            #count = 0
            #for item in combined_set:
            #    print("\t%s" % item)
            #    count += 1
            #    if count >= 15:
            #        break

    labels = list(map(map_label, sets.keys()))
    sets = list(sets.values())

    plt.figure(figsize=(18, 9))

    supervenn(sets, labels, side_plots='right',
            min_width_for_annotation=options.min_width,
            chunks_ordering='size', widths_minmax_ratio=options.ratio)

    plt.xlabel("Terms")
    plt.ylabel("Method")

    plt.savefig(options.output)

if __name__ == "__main__":

    main()
