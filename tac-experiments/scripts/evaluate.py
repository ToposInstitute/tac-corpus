import argparse

from extract_keywords import get_keywords
from markdownTable import markdownTable

parser = argparse.ArgumentParser(description='Evaluate keywords')
parser.add_argument('gold', nargs='+', choices=['textrank', 'parmenides',
    'opentapioca', 'dygie', 'author', 'nlab', 'nps'])
parser.add_argument('--predictions', '-p', nargs='+', choices=['textrank',
    'parmenides', 'opentapioca', 'dygie', 'dygie_tac', 'author', 'nlab', 'nps'])

def get_gold(options):

    keywords = set()

    if 'textrank' in options:
        keywords = keywords | get_keywords('processed/textrank_extractive.txt')
    if 'parmenides' in options:
        keywords = keywords | \
            get_keywords('processed/parmenides_extractive.txt')
    if 'opentapioca' in options:
        keywords = keywords | \
            get_keywords('processed/opentapioca_extractive.txt')
    if 'dygie' in options:
        keywords = keywords | get_keywords('processed/dygie_extractive.txt')
    if 'author' in options:
        keywords = keywords | get_keywords('processed/author_extractive.txt')
    if 'nlab' in options:
        keywords = keywords | get_keywords('processed/nlab_extractive.txt')
    if 'nps' in options:
        keywords = keywords | get_keywords('processed/nps_extractive.txt')

    return keywords

def get_predictions(options):

    predictions = {}

    if 'textrank' in options:
        predictions['textrank'] = \
            get_keywords('processed/textrank_extractive.txt')
    if 'parmenides' in options:
        predictions['parmenides'] = \
            get_keywords('processed/parmenides_extractive.txt')
    if 'opentapioca' in options:
        predictions['opentapioca'] = \
            get_keywords('processed/opentapioca_extractive.txt')
    if 'dygie' in options:
        predictions['dygie'] = get_keywords('processed/dygie_extractive.txt')
    if 'dygie_tac' in options:
        predictions['dygie_tac'] = get_keywords('processed/dygie_tac_extractive.txt')
    if 'author' in options:
        predictions['author'] = get_keywords('processed/author_extractive.txt')
    if 'nlab' in options:
        predictions['nlab'] = get_keywords('processed/nlab_extractive.txt')
    if 'nps' in options:
        predictions['nps'] = get_keywords('processed/nps_extractive.txt')

    return predictions

def add_results(results, name, predicted, gold):

    tp = len(predicted & gold)
    fp = len(predicted - gold)
    fn = len(gold - predicted)

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f = 2 * precision * recall / (precision + recall)

    results[name] = {
        'True Positives': '%d' % tp,
        'False Positives': '%d' % fp,
        'False Negatives': '%d' % fn,
        'Precision': '%1.2f' % precision,
        'Recall': '%1.2f' % recall,
        'F1': '%1.2f' % f,
    }

def evaluate(predictions, gold, names):

    results = {}

    for name, prediction in sorted(list(predictions.items()), key=lambda x:
            x[0]):
        add_results(results, name, prediction, gold)

    with open('results/results.md', 'a') as outfile:
        outfile.write("%s\n" % '+'.join(names))
        outfile.write('-' * len('+'.join(names)) + '\n\n')
        outfile.write('|Metric|%s|\n' % '|'.join(results.keys()))
        outfile.write('|------|%s|\n' % '|'.join('-' * len(res) for res in
            results.values()))
        outfile.write('|True Positives|%s|\n' % '|'.join(res['True Positives'] for
            res in results.values()))
        outfile.write('|False Positives|%s|\n' % '|'.join(res['False Positives'] for
            res in results.values()))
        outfile.write('|False Negatives|%s|\n' % '|'.join(res['False Negatives'] for
            res in results.values()))
        outfile.write('|Precision|%s|\n' % '|'.join(res['Precision'] for res in
            results.values()))
        outfile.write('|Recall|%s|\n' % '|'.join(res['Recall'] for res in
            results.values()))
        outfile.write('|F1|%s|\n' % '|'.join(res['F1'] for res in
            results.values()))
        outfile.write("\n\n")

def main():

    options = parser.parse_args()

    gold = get_gold(options.gold)
    predictions = get_predictions(options.predictions)

    evaluate(predictions, gold, options.gold)

if __name__ == "__main__":

    main()
