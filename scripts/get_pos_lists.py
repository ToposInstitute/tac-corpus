import csv
import requests
import time

from collections import defaultdict
from conllu import parse_incr
from tqdm import tqdm

OT_URL = "https://nlab.opentapioca.org/api/annotate"

def main():

    noun = defaultdict(int)
    propn = defaultdict(int)

    with open("tac.conll") as infile:
        for tokenlist in tqdm(parse_incr(infile)):
            for token in tokenlist:
                lemma = token['lemma'].lower()
                if len(lemma) < 2:
                    continue
                if token['upos'] == 'NOUN':
                    noun[lemma] += 1
                if token['upos'] == 'PROPN':
                    propn[lemma] += 1

    with open('noun.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        for (token, frequency) in tqdm(sorted(noun.items(), key=lambda x: x[1],
                reverse=True)):

            while True:
                result = requests.post(OT_URL, data={'query': token})
                if result.status_code == 503:
                    print("Server overloaded.")
                    time.sleep(5)
                    continue
                result_data = result.json()
                break
            urls = []
            for annotation in result_data.get('annotations', []):
                for tag in annotation.get('tags', []):
                    urls.append("wikidata.org/wiki/%s" % tag['id'])
            writer.writerow([token, frequency, ';'.join(urls)])

    with open('propn.txt', 'w') as outfile:
        for (token, frequency) in tqdm(sorted(propn.items(), key=lambda x: x[1],
                reverse=True)):
            outfile.write("%s,%d\n" % (token, frequency))

if __name__ == "__main__":

    main()
