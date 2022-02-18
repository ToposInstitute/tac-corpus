import json

from tqdm import tqdm
from parmenides.conf import settings
from parmenides.document import Document, Section
from parmenides.extract import Extractor
from parmenides.utils import (cleanup, get_documents, import_class,
        import_function, init)
from tqdm import tqdm

class SimpleExtractor(Extractor):
    """
    A simple Parmenides terminology extractor.
    """

    def extract(self, tree):

        for subtree in tree.subtrees():
            if subtree.term:
                yield subtree

class SimpleParser:
    """
    A simple Parmenides-based parser that iterates over extracted terms in the
    text.
    """

    def __init__(self, settings_dict=None):

        default_settings = {
            'EXTRACTOR': SimpleExtractor,
            'DEFAULT_LANGUAGE': 'en_core_web_trf',
            'TERM_FILTER': lambda term: len(term) < 6,
        }

        if settings_dict:
            default_settings.update(settings_dict)

        init(dictionary=default_settings)

        self.processor = import_class(settings.PROCESSOR)()

    def __del__(self):

        try:
            cleanup()
        except ImportError:
            pass

    def __call__(self, text):

        results = self.parse(text)

        for result in results:
            if result is None:
                continue

            yield result

    def parse(self, text):

        document = Document(
            identifier=None,
            title=None,
            sections=[Section('Main', text)],
            collections=['parmenides'],
        )

        return self.processor.process(document)

    def parse_sentence(self, text):

        return next(self.parse(text))

def main():

    ot_keywords = set()
    dygie_keywords = set()
    randr_keywords = set()

    parser = SimpleParser()

    with open('articles.json') as infile:
        data = json.load(infile)
        for article in tqdm(data):
            for tag in article['tags']:
                if tag['source'] == 'opentapioca':
                    keyword = tag['text']
                    ot_keywords.add(keyword)
                elif tag['source'] == 'dygiepp':
                    keyword = tag['text']
                    dygie_keywords.add(keyword)

            text = article['text']
            terms = parser(text)

            for tree in terms:
                tree_string = str(tree)
                randr_keywords.add(tree_string)

    with open('ot_keywords.txt', 'w') as outfile:
        for keyword in ot_keywords:
            outfile.write("%s\n" % keyword.strip())

    with open('dygiepp_keywords.txt', 'w') as outfile:
        for keyword in dygie_keywords:
            outfile.write("%s\n" % keyword.strip())

    with open('randr_keywords.txt', 'w') as outfile:
        for keyword in randr_keywords:
            outfile.write("%s\n" % keyword.strip())

if __name__ == "__main__":

    main()
