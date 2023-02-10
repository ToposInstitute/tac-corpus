from collections import defaultdict
from conllu import parse_incr
from tqdm import tqdm

def main():

    noun = defaultdict(int)
    propn = defaultdict(int)

    with open("tac.conll") as infile:
        for tokenlist in tqdm(parse_incr(infile)):
            for token in tokenlist:
                if len(token['lemma']) < 2:
                    continue
                if token['upos'] == 'NOUN':
                    noun[token['lemma'].lower()] += 1
                if token['upos'] == 'PROPN':
                    propn[token['lemma'].lower()] += 1

    with open('noun.txt', 'w') as outfile:
        for (token, frequency) in sorted(noun.items(), key=lambda x: x[1],
                reverse=True):
            outfile.write("%s,%d\n" % (token, frequency))

    with open('propn.txt', 'w') as outfile:
        for (token, frequency) in sorted(propn.items(), key=lambda x: x[1],
                reverse=True):
            outfile.write("%s,%d\n" % (token, frequency))

if __name__ == "__main__":

    main()
