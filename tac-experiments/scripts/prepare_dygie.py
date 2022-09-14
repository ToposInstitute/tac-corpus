import json
import spacy

from tqdm import tqdm

nlp = spacy.load('en_core_sci_scibert')

def main():

    with open('raw/tac_abstracts.json') as infile:
        data = json.load(infile)

    with open('processed/tac_dygiepp.json', 'w') as outfile:
        for abstract in tqdm(data):
            sentences = []
            doc = nlp(abstract['abstract'])
            for sentence in doc.sents:
                hyphenated = False
                tokens = []
                for token in sentence:
                    if token.text.strip() == '':
                        continue
                    if token.text == '-':
                        tokens[-1] += token.text
                        hyphenated = True
                    elif token.text and hyphenated:
                        tokens[-1] += token.text
                        hyphenated = False
                    elif token.text:
                        tokens.append(token.text)
                if len(tokens) > 1:
                    sentences.append(tokens)

            json_string = json.dumps({
                'doc_key': abstract['url'],
                'dataset': 'scierc',
                'sentences': sentences,
                'ner': [[] for i in range(len(sentences))],
                'relations': [[] for i in range(len(sentences))],
            })
            outfile.write('%s\n' % json_string)

if __name__ == "__main__":

    main()
