import argparse
import json
import pytextrank
import requests
import spacy

from parmenides_tac import SimpleParser
from tqdm import tqdm

OT_URL = 'https://nlab.opentapioca.org/api/annotate'

if __name__ == "__main__":
    #nlp = spacy.load('en_core_sci_scibert')
    nlp = spacy.load('en_core_web_trf')
    nlp.add_pipe('textrank')

parser = argparse.ArgumentParser(description='Get base keywords')
parser.add_argument('targets', nargs='+', choices=['textrank', 'parmenides',
    'opentapioca', 'dygie', 'dygie_tac', 'author', 'nlab', 'nps'])

def extract(extractors):

    with open('raw/tac_abstracts.json') as infile:

        data = json.load(infile)

        if 'textrank' in extractors:
            keywords = extract_textrank(data)
            write_keywords_sorted(keywords, 'processed/textrank.txt')
        if 'parmenides' in extractors:
            keywords = extract_parmenides(data)
            write_keywords_sorted(keywords, 'processed/parmenides.txt')
        if 'opentapioca' in extractors:
            keywords = extract_opentapioca(data)
            write_keywords_sorted(keywords, 'processed/opentapioca.txt')
        if 'dygie' in extractors:
            keywords = extract_dygie(data)
            write_keywords_sorted(keywords, 'processed/dygie.txt')
        if 'dygie_tac' in extractors:
            keywords = extract_dygie(data, filename='raw/tac_dygiepp_trained.jsonl')
            write_keywords_sorted(keywords, 'processed/dygie_tac.txt')
        if 'author' in extractors:
            keywords = extract_author_keywords(data)
            write_keywords_sorted(keywords, 'processed/author.txt')
        if 'nlab' in extractors:
            keywords = extract_nlab_keywords(data)
            write_keywords_sorted(keywords, 'processed/nlab.txt')
        if 'nps' in extractors:
            keywords = extract_nps(data)
            write_keywords_sorted(keywords, 'processed/nps.txt')

def extract_author_keywords(data):

    print("Processing author keywords")
    keywords = set()
    for article in tqdm(data):
        for keyword in article['keywords']:
            keywords.add(keyword)

    print("Found %d keywords" % len(keywords))
    return keywords

def extract_nlab_keywords(data):

    print("Processing nlab keywords")
    keywords = set()
    with open('raw/nlab_plain.json') as infile:
        data = json.load(infile)
        for article in tqdm(data):
            keywords.add(article['title'])

    print("Found %d keywords" % len(keywords))
    return keywords

def extract_nps(data):

    print("Processing NPs")
    keywords = set()

    for article in tqdm(data):
        abstract = article['abstract']
        doc = nlp(abstract)
        for i in range(1, len(doc)):
            prev_token = doc[i - 1]
            this_token = doc[i]

            if prev_token.pos_ == 'ADJ' and this_token.pos_ == 'NOUN':
                result = (prev_token.text + ' ' + this_token.text).lower()
                if '$' in result or '\\' in result or result.startswith('-'):
                    continue
                if '^' in result or result.endswith('-'):
                    continue
                keywords.add(prev_token.text + ' ' + this_token.text)
            if this_token.pos_ == 'compound':
                keywords.add(prev_token.text + ' ' + this_token.text)

    print("Found %d keywords" % len(keywords))
    return keywords

def extract_textrank(data):

    print("Processing with TextRank")
    keywords = set()
    for article in tqdm(data):
        abstract = article['abstract']
        doc = nlp(abstract)
        for phrase in doc._.phrases:
            keywords.add(phrase.text.strip())

    print("Found %d keywords" % len(keywords))
    return keywords

def extract_parmenides(data):

    print("Processing with Parmenides")
    keywords = set()
    parser = SimpleParser()
    for article in tqdm(data):
        abstract = article['abstract']
        for phrase in parser(abstract):
            keywords.add(str(phrase).strip())

    print("Found %d keywords" % len(keywords))
    return keywords

def extract_opentapioca(data):

    print("Processing with OpenTapioca")
    keywords = set()
    for article in tqdm(data):
        abstract = article['abstract']
        result = requests.post(OT_URL, data={'query': abstract})
        result_data = result.json()
        for annotation in result_data.get('annotations', []):
            text = result_data['text'][annotation['start']:annotation['end']]
            keywords.add(text.strip())

    print("Found %d keywords" % len(keywords))
    return keywords

def extract_dygie(data, filename='raw/tac_dygiepp.jsonl'):

    print("Processing with DyGIE++")
    keywords = set()
    with open(filename) as infile:
        for line in infile:
            document = json.loads(line)
            sentences = document['sentences']
            for i in range(len(sentences)):
                sentence = sentences[i]
                predicted_ner = document['predicted_ner'][i]
                for prediction in predicted_ner:
                    start = prediction[0]
                    end = prediction[1] + 1
                    phrase = ' '.join(sentence[start:end])
                    if phrase.strip():
                        keywords.add(phrase.strip())

    print("Found %d keywords" % len(keywords))
    return keywords

def write_keywords_sorted(keywords, filename):

    sorted_keywords = sorted(keywords)

    with open(filename, 'w', encoding="utf-8") as outfile:
        for keyword in sorted_keywords:
            outfile.write("%s\n" % keyword)

def main():

    options = parser.parse_args()

    extract(options.targets)

if __name__ == "__main__":

    main()
