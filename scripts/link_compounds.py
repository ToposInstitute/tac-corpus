import csv
import requests
import time

from bs4 import BeautifulSoup
from tqdm import tqdm

ENDPOINT = "https://wikidata.org/w/api.php?action=query&list=search&format=json&srsearch=%s"
#OT_URL = "https://nlab.opentapioca.org/api/annotate"

def main():

    with open("mwe/candidates.xml") as infile:
        soup = BeautifulSoup(infile, 'xml')

        with open('mwe/links.csv', 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=[
                'candidate',
                'frequency',
                'links',
            ])
            writer.writeheader()

            for cand in tqdm(soup.find_all('cand')):
                candidate = ' '.join([w['lemma'] for w in cand.ngram.find_all('w')])
                if candidate.startswith('-'):
                    continue
                frequency = cand.ngram.freq['value']
                links = []

                for ngram in cand.occurs.find_all('ngram'):
                    surface = ' '.join([w['surface'] for w in
                        ngram.find_all('w')])

                    while True:
                        #result = requests.post(OT_URL, data={'query': surface})
                        try:
                            result = requests.post(ENDPOINT % surface)
                            if result.status_code == 503:
                                print("Server overloaded")
                                time.sleep(5)
                                continue
                            result_data = result.json()
                            break
                        except:
                            print("Other error. Retrying.")
                            time.sleep(5)
                    for annotation in result_data['query']['search']:
                        links.append("wikidata.org/wiki/%s" % annotation['title'])
                    #for annotation in result_data.get('annotations', []):
                    #    for tag in annotation.get('tags', []):
                    #        links.append("wikidata.org/wiki/%s" % tag['id'])

                writer.writerow({
                    'candidate': candidate,
                    'frequency': frequency,
                    'links': ';'.join(links)
                })

if __name__ == "__main__":

    main()
