import json
import spacy

from normalize_keywords import normalize
from tqdm import tqdm

#nlp = spacy.load('en_core_sci_scibert')
nlp = spacy.load('en_core_web_trf')

def main():

    with open('raw/tac_abstracts.json') as infile:
        data = json.load(infile)

        for article in tqdm(data):
            text = article['abstract']
            doc = nlp(text)
            new_doc = ' '.join((token.lemma_ for token in doc if
                token.lemma_.strip()))

            article['abstract'] = new_doc

        with open('processed/tac_abstracts_normalized.json', 'w') as outfile:

            json.dump(data, outfile)

if __name__ == "__main__":

    main()
