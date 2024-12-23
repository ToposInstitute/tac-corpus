import json
import re
import subprocess

from bs4 import BeautifulSoup
from spacy_conll import init_parser
from tqdm import tqdm

MODEL = "en_core_web_trf"

nlp = init_parser(MODEL, "spacy", include_headers=True)

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

    result = re.sub('\s+', ' ', soup.get_text(strip=True))

    return result

def main():

    with open('tac.conll', 'w') as outfile:
        with open('tac_metadata.json') as infile:
            data = json.load(infile)

            doc_id = 0
            sent_id = 0
            for article in tqdm(data):
                content = article['abstract']
                content = filter_mathml(content).strip()
                doc_id += 1

                if not content:
                    continue

                doc = nlp(content)

                outfile.write("# doc_id = %d\n" % doc_id)

                for span in doc._.conll:
                    if ''.join([token['form'] for token in span]).strip() == "":
                        continue
                    sent_id += 1
                    span_string = " ".join(map(
                        lambda x: str(x['form']).replace('\t', '\\t')\
                                .replace('\n', '\\n')\
                                .replace('\r', '\\r')\
                                .replace(' ', '\\s'),
                        [token for token in span]
                    ))
                    outfile.write("# sent_id = %d\n" % sent_id)
                    outfile.write("# text = %s\n" % span_string)
                    for token in span:
                        token_conll_str = "\t".join(map(
                            lambda x: str(x).replace('\t', '\\t')\
                                    .replace('\n', '\\n')\
                                    .replace('\r', '\\r')\
                                    .replace(' ', '\\s'),
                            token.values(),
                        )) + "\n"
                        outfile.write(token_conll_str)
                    outfile.write("\n")
                outfile.write("\n")

if __name__ == "__main__":

    main()
