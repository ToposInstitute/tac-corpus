import argparse
import spacy

from get_keywords import write_keywords_sorted
from tqdm import tqdm

#nlp = spacy.load('en_core_sci_scibert')
nlp = spacy.load('en_core_web_trf')

STOP_WORDS = {'in', 'a', 'to', 'this', 'the', 'with', 'from', 'on', 'for',
        'whose', 'of', 'as', 'such', 'each', 'some', 'not', 'like', 'let',
        'ii', 'are', 'is', 'an', 'we', 'et', 'it', 'our', 'and', 'these', 'al'}

parser = argparse.ArgumentParser(description='Normalize keywords')
parser.add_argument('targets', nargs='+', choices=['textrank', 'parmenides',
    'opentapioca', 'dygie', 'dygie_tac', 'author', 'nlab', 'nps'])

def normalize(keyword):

    doc = nlp(keyword.strip())
    new_keyword = ' '.join((token.lemma_ for token in doc if
        token.lemma_.strip()))
    return new_keyword.lower().strip()

def phrase_filter(phrase):

    words = phrase.split()

    if len(phrase) == 0:
        return False
    if '\\' in phrase or '$' in phrase:
        return False
    if not phrase[0].isalnum():
        return False
    if not phrase[-1].isalnum():
        return False
    if len(phrase) == 1:
        return False
    if words[0] in STOP_WORDS:
        return False
    if words[-1] in STOP_WORDS:
        return False
    if len(words) > 5:
        return False

    return True

def normalize_file(filename):

    new_keywords = set()
    with open(filename) as infile:
        keywords = (line for line in tqdm(infile))
        for new_keyword in filter(phrase_filter, map(normalize, keywords)):
            new_keywords.add(new_keyword)

    return new_keywords

def normalize_files(targets):

    if 'textrank' in targets:
        print("Processing textrank")
        keywords = normalize_file('processed/textrank.txt')
        write_keywords_sorted(keywords, 'processed/textrank_normalized.txt')
    if 'parmenides' in targets:
        print("Processing parmenides")
        keywords = normalize_file('processed/parmenides.txt')
        write_keywords_sorted(keywords, 'processed/parmenides_normalized.txt')
    if 'opentapioca' in targets:
        print("Processing opentapioca")
        keywords = normalize_file('processed/opentapioca.txt')
        write_keywords_sorted(keywords, 'processed/opentapioca_normalized.txt')
    if 'dygie' in targets:
        print("Processing DyGIE++")
        keywords = normalize_file('processed/dygie.txt')
        write_keywords_sorted(keywords, 'processed/dygie_normalized.txt')
    if 'dygie_tac' in targets:
        print("Processing DyGIE++ (TAC Trained")
        keywords = normalize_file('processed/dygie_tac.txt')
        write_keywords_sorted(keywords, 'processed/dygie_tac_normalized.txt')
    if 'author' in targets:
        print("Processing author keywords")
        keywords = normalize_file('processed/author.txt')
        write_keywords_sorted(keywords, 'processed/author_normalized.txt')
    if 'nlab' in targets:
        print("Processing nlab keywords")
        keywords = normalize_file('processed/nlab.txt')
        write_keywords_sorted(keywords, 'processed/nlab_normalized.txt')
    if 'nps' in targets:
        print("Processing NPs")
        keywords = normalize_file('processed/nps.txt')
        write_keywords_sorted(keywords, 'processed/nps_normalized.txt')

def main():

    options = parser.parse_args()
    normalize_files(options.targets)

if __name__ == "__main__":

    main()
