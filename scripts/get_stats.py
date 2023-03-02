import json
import re
import spacy
import subprocess

from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime
from spacy import displacy
from tqdm import tqdm

MODEL = 'en_core_web_trf'

nlp = spacy.load(MODEL)

class Lists:

    def __init__(self):

        self.rootless = []
        self.short = []
        self.x_cats = []
        self.dep_rels = []
        self.persons = []
        self.dates = []
        self.monies = []

    def save(self):

        with open('lists/rootless.json', 'w') as outfile:
            json.dump(self.rootless, outfile, indent=2)
        with open('lists/short.json', 'w') as outfile:
            json.dump(self.short, outfile, indent=2)
        with open('lists/x_cats.json', 'w') as outfile:
            json.dump(self.x_cats, outfile, indent=2)
        with open('lists/dep_rels.json', 'w') as outfile:
            json.dump(self.dep_rels, outfile, indent=2)
        with open('lists/persons.json', 'w') as outfile:
            json.dump(self.persons, outfile, indent=2)
        with open('lists/dates.json', 'w') as outfile:
            json.dump(self.dates, outfile, indent=2)
        with open('lists/monies.json', 'w') as outfile:
            json.dump(self.monies, outfile, indent=2)

#EXCLUDE_CATEGORIES = re.compile(
#    r'category:\W*(?:meta)|(?:empty)|(?:joke)|(?:svg)|(?:character tables)'
#)

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

    count = len(soup.find_all("Math"))

    result = re.sub('\s+', ' ', soup.get_text())

    return (result, count)

def main():

    documents = 0
    sentences = 0
    tokens = 0
    removed = 0
    lemmas = set()
    pos = defaultdict(int)
    tag = defaultdict(int)
    deps = defaultdict(int)
    compounds = 0
    entities = defaultdict(int)
    sentence_lengths = defaultdict(int)

    pos_stats = defaultdict(lambda: defaultdict(int))
    tag_stats = defaultdict(lambda: defaultdict(int))
    dep_stats = defaultdict(lambda: defaultdict(int))
    entity_stats = defaultdict(lambda: defaultdict(int))

    pos_examples = defaultdict(list)
    tag_examples = defaultdict(list)
    dep_examples = defaultdict(list)
    entity_examples = defaultdict(list)

    lists = Lists()

    with open('tac_metadata.json') as infile:

        data = json.load(infile)

        latex_count = 0

        for article in tqdm(data):

            documents += 1

            content = article['abstract']
            content, latex_increment = filter_mathml(content)
            latex_count += latex_increment

            #if EXCLUDE_CATEGORIES.search(content):
            #    removed += 1
            #    continue

            if not content:
                continue
            doc = nlp(content)

            html = displacy.render(doc, style="dep", page=True, minify="true")

            safe_title = article['title'].replace('/', '')

            #with open('visualization/%s.html' % safe_title, 'w') as outfile:
            #    outfile.write(html)

            for sentence in doc.sents:
                if not str(sentence).strip():
                    continue
                #if len(sentence) > 60:
                #    print(sentence)
                sentence_lengths[len(sentence)] += 1
                sentences += 1
                tokens += len(sentence)
                current_entity = []
                # HERE
                if 'ROOT' not in [token.dep_ for token in sentence]:
                    lists.rootless.append(str(sentence))
                if len(sentence) < 5:
                    lists.short.append(str(sentence))
                for token in sentence:
                    lemmas.add(token.lemma_)
                    pos[token.pos_] += 1
                    pos_stats[token.pos_][token.lemma_] += 1
                    if len(pos_examples[token.pos_]) < 20:
                        pos_examples[token.pos_].append({
                            'sentence': str(sentence),
                            'value': str(token),
                        })
                    if token.pos_ == 'X':
                        lists.x_cats.append({
                            'sentence': str(sentence),
                            'token': str(token),
                        })
                    tag[token.tag_] += 1
                    tag_stats[token.tag_][token.lemma_] += 1
                    if len(tag_examples[token.tag_]) < 20:
                        tag_examples[token.tag_].append({
                            'sentence': str(sentence),
                            'value': str(token),
                        })
                    deps[token.dep_] += 1
                    if token.dep_ == 'dep':
                        lists.dep_rels.append({
                            'sentence': str(sentence),
                            'tokens': [str(token), str(token.head)],
                        })
                    if token.head.i < token.i:
                        dep_stats[token.dep_][token.head.lemma_ + ' ' + token.lemma_] += 1
                    else:
                        dep_stats[token.dep_][token.lemma_ + ' ' + token.head.lemma_] += 1
                    if len(dep_examples[token.dep_]) < 20:
                        dep_examples[token.dep_].append({
                            'sentence': str(sentence),
                            'value': str(token),
                        })
                    if token.dep_ == 'compound':
                        compounds += 1
                    if token.ent_iob == 3:
                        entities[token.ent_type_] += 1
                        entity_lemma = token.lemma_
                        try:
                            i = token.nbor()
                            while i.ent_iob == 1:
                                entity_lemma += ' ' + i.lemma_
                                i = i.nbor()
                        except IndexError:
                            pass
                        entity_stats[token.ent_type_][entity_lemma] += 1
                        if token.ent_type_ == 'PERSON':
                            lists.persons.append({
                                'sentence': str(sentence),
                                'lemma': entity_lemma,
                            })
                        elif token.ent_type_ == 'DATE':
                            lists.dates.append({
                                'sentence': str(sentence),
                                'lemma': entity_lemma,
                            })
                        elif token.ent_type_ == 'MONEY':
                            lists.monies.append({
                                'sentence': str(sentence),
                                'lemma': entity_lemma,
                            })
                        if len(entity_examples[token.ent_type_]) < 20:
                            entity_examples[token.ent_type_].append({
                                'sentence': str(sentence),
                                'value': str(token),
                            })

    lists.save()

    with open('tac_compounds.tsv', 'w') as outfile:
        sorted_compounds = dict(sorted(dep_stats['compound'].items(),
            key=lambda item: item[1], reverse=True))
        for compound, count in sorted_compounds.items():
            outfile.write('%s\t%d\n' % (compound, count))

    with open('stats.json', 'w') as outfile:
        data = {
            'spacy_version': spacy.__version__,
            'spacy_model': MODEL,
            'date': str(datetime.now()),
            'corpus': 'tac',
            'documents': documents,
            'sentences': sentences,
            'sentence_lengths': dict(sorted(sentence_lengths.items(),
                key=lambda item: item[0])),
            'tokens': tokens,
            'lemmas': len(lemmas),
            'pos': pos,
            'tag': tag,
            'deps': deps,
            'compounds': compounds,
            'entities': entities,
            'removed': removed,
            'latex_expressions': latex_count,
            'pos_stats': {pos: dict(sorted(pos_stats[pos].items(), key=lambda
                item: item[1], reverse=True)[:50]) for pos in pos_stats},
            'tag_stats': {tag: dict(sorted(tag_stats[tag].items(), key=lambda
                item: item[1], reverse=True)[:50]) for tag in tag_stats},
            'dep_stats': {dep: dict(sorted(dep_stats[dep].items(), key=lambda
                item: item[1], reverse=True)[:50]) for dep in dep_stats},
            'entity_stats': {entity: dict(sorted(entity_stats[entity].items(),
                key=lambda item: item[1], reverse=True)[:50]) for entity in entity_stats},
            #'pos_examples': pos_examples,
            #'tag_examples': tag_examples,
            #'dep_examples': dep_examples,
            #'entity_examples': entity_examples,
        }

        json.dump(data, outfile, indent=2)

if __name__ == "__main__":

    main()
