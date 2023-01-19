import json
import spacy

from TexSoup import TexSoup
from tqdm import tqdm

nlp = spacy.load('en_core_web_trf')

def main():

    with open('tac.json') as infile:

        data = json.load(infile)
        results = []
        for article in tqdm(data):
            title = article['title']
            text = article['text']
            try:
                soup = TexSoup(text, tolerance=10)
            except EOFError:
                text = text.replace('$', '')
                soup = TexSoup(text)

            text_doc = nlp(''.join(soup.text))

            for sentence in text_doc.sents:
                start = sentence.start
                indices = []
                for token in sentence:
                    if token.head.i == token.i:
                        indices.append(-1)
                    else:
                        indices.append(token.head.i - start)
                if len(sentence) > 100:
                    continue
                results.append({
                    'tokens': [token.text for token in sentence],
                    'labels': ['O' for token in sentence],
                    'heads': indices,
                    'pos': [token.pos_ for token in sentence],
                    'label': "none",
                    'dep_path': [],
                })

        with open('tac_data.json', 'w') as outfile:
            json.dump(results, outfile)

if __name__ == "__main__":

    main()
