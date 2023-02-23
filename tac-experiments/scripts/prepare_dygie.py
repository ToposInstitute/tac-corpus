import json
import re
import spacy
import subprocess

from bs4 import BeautifulSoup
from tqdm import tqdm

nlp = spacy.load('en_core_web_trf')

def filter_mathml(text):

    content = """
\\documentclass{standalone}
\\usepackage{amsmath,amssymb}

\\begin{document}

%s

\\end{document}
    """ % text

    xml = subprocess.run(['latexml', '-'], input=content, capture_output=True,
            encoding='UTF-8').stdout

    soup = BeautifulSoup(xml, "xml")

    result = re.sub('\s+', ' ', soup.get_text())

    return result

def main():

    with open('raw/tac_abstracts.json') as infile:
        data = json.load(infile)

    with open('processed/tac_dygiepp.json', 'w') as outfile:
        for abstract in tqdm(data):
            sentences = []
            content = filter_mathml(abstract['abstract'])
            doc = nlp(content)
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
