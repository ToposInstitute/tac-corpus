# Evaluates several keyword extraction methods against gold/silver standards

import argparse
import csv
import json
import os
import pytextrank
import spacy

from collections import defaultdict
from parmenides.conf import settings
from parmenides.document import Document, Section
from parmenides.extract import Extractor
from parmenides.utils import (cleanup, get_documents, import_class,
        import_function, init)
from tqdm import tqdm

# A set of words that are optionally removed from the results of
# Parmenides-based extractors
STOP_WORDS = set(['in', 'a', 'to', 'this', 'the', 'with', 'from', 'on',
        'for','whose', 'of', 'as', 'such', 'each', 'some', 'not', 'like',
        'let', 'ii', 'are', 'is', 'an', 'we', 'et', 'it', 'our', 'and',
        'these', 'al']
)

nlp = spacy.load('en_core_web_trf')
nlp.add_pipe('textrank')

parser = argparse.ArgumentParser(
    description="Experiments on terminology extraction"
)
parser.add_argument('--text', '-t', nargs='*', action='store',
    help="parse predictions from a text file", type=str,
)
parser.add_argument('--text-gold', '-T', nargs='*', action='store',
    help="parse gold from a text file", type=str,
)
parser.add_argument('--csv-gold', '-C', nargs='*', action='store',
    help="parse gold from a CSV file", type=str,
)
parser.add_argument('--textrank', '-r', nargs='*', action='store',
    help="parse predictions using textrank", type=str,
)

def normalize(keyword):

    doc = nlp(keyword.strip())
    new_keyword = ' '.join((token.lemma_ for token in doc))
    return new_keyword.lower()

def main():

    options = parser.parse_args()

    gold = set()
    gold_separated = defaultdict(set)
    predicted = defaultdict(set)

    # GOLD
    if options.csv_gold:
        for filename in options.csv_gold:
            basename = os.path.basename(filename)
            rootname = os.path.splitext(basename)[0]
            print("Parsing gold CSV: %s" % filename)
            with open(filename, newline='') as infile:
                reader = csv.reader(infile)
                for row in tqdm(reader):
                    if row[0]:
                        keyword = normalize(row[0])
                        gold.add(keyword)
                        gold_separated[rootname].add(keyword)

    if options.text_gold:
        for filename in options.text_gold:
            basename = os.path.basename(filename)
            rootname = os.path.splitext(basename)[0]
            print("Parsing gold text: %s" % filename)
            with open(filename) as infile:
                for line in tqdm(infile):
                    keyword = normalize(line)
                    gold.add(keyword)
                    gold_separated[rootname].add(keyword)

    # PREDICTIONS
    if options.text:
        for filename in options.text:
            print("Parsing text predictions: %s" % filename)
            basename = os.path.basename(filename)
            rootname = os.path.splitext(basename)[0]
            with open(filename) as infile:
                for line in tqdm(infile):
                    if phrase_filter(line):
                        continue
                    predicted[rootname].add(normalize(line.strip()))

    if options.textrank:
        count = 0
        for filename in options.textrank:
            print("Parsing textrank predictions: %s" % filename)
            count += 1
            with open(filename) as infile:
                data = json.load(infile)
                for article in tqdm(data):
                    abstract = article['text']
                    doc = nlp(abstract)
                    for phrase in doc._.phrases:
                        phrase_string = phrase.text
                        keyword = normalize(phrase_string)
                        predicted['textrank-%d' % count].add(keyword)

    for name, evaluation in predicted.items():
        show_results(name, evaluation, gold)

    for name, keywords in predicted.items():
        with open(name + '.keywords', 'w') as outfile:
            for keyword in keywords:
                outfile.write(keyword + '\n')

    for name, keywords in gold_separated.items():
        with open(name + '.keywords', 'w') as outfile:
            for keyword in keywords:
                outfile.write(keyword + '\n')

def phrase_filter(phrase):

    phrase = phrase.strip()

    words = phrase.split()

    if '\\' in phrase or '$' in phrase:
        return True
    if not phrase[0].isalnum():
        return True
    if not phrase[-1].isalnum():
        return True
    if len(phrase) == 1:
        return True
    if words[0] in STOP_WORDS:
        return True
    if words[-1] in STOP_WORDS:
        return True
    if len(words) > 5:
        return True

    return False

def show_results(name, predicted, gold):

    tp = len(predicted & gold)
    fp = len(predicted - gold)
    fn = len(gold - predicted)

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f = 2 * precision * recall / (precision + recall)

    print("%s True Positives: %d" % (name, tp))
    print("%s False Positives: %d" % (name, fp))
    print("%s False Negatives: %d" % (name, fn))
    print("%s Precision: %1.2f" % (name, precision))
    print("%s Recall: %1.2f" % (name, recall))
    print("%s F1: %1.2f" % (name, f))

if __name__ == "__main__":

    main()
