import os
import re
import math

from collections import Counter


STOPWORDS = set([x.strip() for x in
                 open(os.path.join(os.path.dirname(__file__),
                                   'stopwords')).readlines()])


class WordCount(object):
    """WordCount generates a frequency table of words in a given text.

    Attributes:
        max_words: An integer indicating the word limit in the frequency table.
        regexp: A string specifying the regex for tokenizing the text.

    >>> from wordcount import WordCount
    >>> wc = WordCount().generate("Hello, how are you? How old are you?")
    """
    def __init__(self, max_words=100, regexp=r"\w+[\w']+"):
        """Inits WordCount with word limit and regex for tokenizing text"""
        self.max_words = max_words
        self.regexp = regexp
        self._raw_text = ''

    def generate(self, text):
        """This creates the frequency of the word counts from the given text"""
        self._raw_text = text
        tokenized = self._tokenize(text)
        frequencies = Counter(tokenized).most_common(self.max_words)
        # scale the word count to max 10, for font-size display
        max_wc = frequencies[0][1]
        wordcount_ = [(word, self._size(wc, max_wc)) for word, wc in
                      frequencies.items()]
        return wordcount_

    def _size(word_count, max_wc):
        return int(math.ceil(10 * word_count/max_wc))

    def _tokenize(self, text):
        text = re.compile(self.regexp).findall(text)
        return [x for x in text.split() if x not in STOPWORDS]
