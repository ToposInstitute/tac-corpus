from parmenides.conf import settings
from parmenides.document import Document, Section
from parmenides.extract import Extractor
from parmenides.utils import (cleanup, get_documents, import_class, 
        import_function, init)

class SimpleExtractor(Extractor):

    def extract(self, tree):

        for subtree in tree.subtrees():
            if subtree.term:
                yield subtree

class SimpleParser:

    def __init__(self, settings_dict=None):

        default_settings = {
            'EXTRACTOR': SimpleExtractor,
            #'DEFAULT_LANGUAGE': 'en_core_sci_scibert',
            'DEFAULT_LANGUAGE': 'en_core_web_trf',
            'TERM_FILTER': lambda term: len(term) < 6,
        }

        if settings_dict:
            default_settings.update(settings_dict)

        init(dictionary=default_settings)

        self.processor = import_class(settings.PROCESSOR)()

    def __del__(self):

        cleanup()

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
