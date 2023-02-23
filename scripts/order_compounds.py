import csv
import requests
import time

from bs4 import BeautifulSoup
from tqdm import tqdm

def main():

    with open("mwe/candidates.xml") as infile:
        soup = BeautifulSoup(infile, "xml")

        with open('mwe/candidates.csv', 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=[
                'ngram', 
                'frequency',
            ])
            writer.writeheader()

            results = []

            for cand in tqdm(soup.find_all('cand')):
                lemmas = [w['lemma'] for w in cand.ngram.find_all('w')]
                if any([len(x) == 1 for x in lemmas]):
                    continue
                candidate = ' '.join(lemmas)
                if candidate.startswith('-'):
                    continue
                frequency = int(cand.ngram.freq['value'])

                results.append({
                    'ngram': candidate,
                    'frequency': frequency,
                })

            sorted_results = sorted(results, key=lambda x: x['frequency'],
                    reverse=True)

            for result in sorted_results:
                writer.writerow(result)

if __name__ == "__main__":

    main()
