from conllu import parse_incr
from tqdm import tqdm

def main():

    noun = set()
    propn = set()

    with open("tac.conll") as infile:
        for tokenlist in tqdm(parse_incr(infile)):
            for token in tokenlist:
                if token['upos'] == 'NOUN':
                    noun.add(token['lemma'])
                if token['upos'] == 'PROPN':
                    propn.add(token['lemma'])

    with open('noun.txt', 'w') as outfile:
        for token in sorted(noun):
            outfile.write("%s\n" % token)

    with open('propn.txt', 'w') as outfile:
        for token in sorted(propn):
            outfile.write("%s\n" % token)

if __name__ == "__main__":

    main()
