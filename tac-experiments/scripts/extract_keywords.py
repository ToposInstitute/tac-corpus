import argparse
import re
import json

from get_keywords import write_keywords_sorted
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Extract keywords from text')
parser.add_argument('targets', nargs='+', choices=['textrank', 'parmenides',
    'opentapioca', 'dygie', 'dygie_tac', 'author', 'nlab', 'nps'])

def extract_keywords(phrases, documents):

    new_phrases = set()

    for phrase in tqdm(phrases):
        for document in documents:
            if re.search(r'\b' + re.escape(phrase) + r'\b',
                    document['abstract']):
                new_phrases.add(phrase)
                break

    return new_phrases

def get_keywords(filename):

    keywords = set()
    with open(filename) as infile:
        for line in infile:
            keywords.add(line.strip())

    return keywords

def main():

    options = parser.parse_args()

    with open('processed/tac_abstracts_normalized.json') as infile:
        documents = json.load(infile)

    if 'textrank' in options.targets:
        print("Processing textrank")
        keywords = get_keywords('processed/textrank_normalized.txt')
        keywords = extract_keywords(keywords, documents)
        write_keywords_sorted(keywords, 'processed/textrank_extractive.txt')
    if 'parmenides' in options.targets:
        print("Processing parmenides")
        keywords = get_keywords('processed/parmenides_normalized.txt')
        keywords = extract_keywords(keywords, documents)
        write_keywords_sorted(keywords, 'processed/parmenides_extractive.txt')
    if 'opentapioca' in options.targets:
        print("Processing OpenTapioca")
        keywords = get_keywords('processed/opentapioca_normalized.txt')
        keywords = extract_keywords(keywords, documents)
        write_keywords_sorted(keywords, 'processed/opentapioca_extractive.txt')
    if 'dygie' in options.targets:
        print("Processing DyGIE++")
        keywords = get_keywords('processed/dygie_normalized.txt')
        keywords = extract_keywords(keywords, documents)
        write_keywords_sorted(keywords, 'processed/dygie_extractive.txt')
    if 'dygie_tac' in options.targets:
        print("Processing DyGIE++ (TAC)")
        keywords = get_keywords('processed/dyige_tac_normalized.txt')
        keywords = extract_keywords(keywords, documents)
        write_keywords_sorted(keywords, 'processed/dygie_tac_extractive.txt')
    if 'author' in options.targets:
        print("Processing author keywords")
        keywords = get_keywords('processed/author_normalized.txt')
        keywords = extract_keywords(keywords, documents)
        write_keywords_sorted(keywords, 'processed/author_extractive.txt')
    if 'nlab' in options.targets:
        print("Processing nlab keywords")
        keywords = get_keywords('processed/nlab_normalized.txt')
        keywords = extract_keywords(keywords, documents)
        write_keywords_sorted(keywords, 'processed/nlab_extractive.txt')
    if 'nps' in options.targets:
        print("Processing NPs")
        keywords = get_keywords('processed/nps_normalized.txt')
        keywords = extract_keywords(keywords, documents)
        write_keywords_sorted(keywords, 'processed/nps_extractive.txt')

if __name__ == "__main__":

    main()
