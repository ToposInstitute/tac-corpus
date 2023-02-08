import json
import re
import spacy

from tqdm import tqdm

nlp = spacy.load('en_core_web_trf')

def main():

    with open('tac_examples.csv', 'w') as outfile:
        with open('tac_metadata.json') as infile:
            data = json.load(infile)

            for article in tqdm(data):
                content = article['abstract']

                doc = nlp(content)

                for sentence in doc.sents:
                    if len(sentence) < 6 or len(sentence) > 16:
                        continue
                    if sentence.root.pos_ not in ['VERB', 'AUX']:
                        continue

                    text = sentence.text.replace('\n', ' ').strip()
                    text = re.sub('\s+', ' ', text)

                    if '$' in text:
                        continue
                    if '\\' in text:
                        continue
                    if '_' in text:
                        continue
                    if 'http:' in text:
                        continue

                    outfile.write(
                        "%s\n" % text
                    )

if __name__ == "__main__":

    main()
