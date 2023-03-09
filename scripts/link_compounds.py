import csv
import requests
import time

from bs4 import BeautifulSoup
from tqdm import tqdm

from SPARQLWrapper import SPARQLWrapper, JSON

sparql_query = """
SELECT distinct ?item WHERE {
    ?item ?label "%s"@en.
}
"""

ENDPOINT = "https://query.wikidata.org/sparql"
#ENDPOINT = "https://wikidata.org/w/api.php?action=query&list=search&format=json&srsearch=%s"
#OT_URL = "https://nlab.opentapioca.org/api/annotate"

HEADERS = {
    'User-Agent': 'parmesan/0.1',
}

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
                    query = sparql_query % surface

                    while True:
                        try:
                            result = requests.post(
                                ENDPOINT, 
                                data={'query': query, 'format': 'json'}, 
                                headers=HEADERS,
                            )
                            if result.status_code == 429:
                                print("Too many requests. Waiting.")
                                print(result.headers['retry-after'])
                                time.sleep(result.headers['retry-after'])
                                continue

                            json = result.json()
                        except Exception as e:
                            print(surface)
                            print(e)
                            print(result)
                            break

                        for item in json['results']['bindings']:
                            link = item['item']['value']
                            links.append(link)

                        break

                writer.writerow({
                    'candidate': candidate,
                    'frequency': frequency,
                    'links': ';'.join(links)
                })

if __name__ == "__main__":

    main()
