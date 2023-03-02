import csv
import sys
import time

from bs4 import BeautifulSoup
from tqdm import tqdm

def main():

    with open(sys.argv[1]) as infile:
        soup = BeautifulSoup(infile, 'xml')

        with open(sys.argv[2], 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=[
                'candidate',
                'frequency',
            ])
            writer.writeheader()

            candidates = []
            for cand in tqdm(soup.find_all('cand')):
                candidate = ' '.join([w['lemma'] for w in cand.ngram.find_all('w')])
                if candidate.startswith('-'):
                    continue
                frequency = int(cand.ngram.freq['value'])
                candidates.append({
                    'candidate': candidate,
                    'frequency': frequency,
                })

            for candidate in sorted(candidates, key=lambda x: x['frequency'],
                    reverse=True):

                writer.writerow(candidate)

if __name__ == "__main__":

    main()
