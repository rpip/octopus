# -*- coding: utf-8 -*-
import os
import re
import math
import urllib2
from collections import Counter

from bs4 import BeautifulSoup, Comment


STOPWORDS = set([x.strip() for x in
                 open(os.path.join(os.path.dirname(__file__),
                                   'stopwords')).readlines()])


class WordCloud(object):
    """WordCloud generates a frequency table of words in a given text.

    Attributes:
        max_words: An integer indicating the word limit in the frequency table.
        regexp: A string specifying the regex for tokenizing the text.

    >>> from wordcloud import WordCloud
    >>> wc = WordCloud().generate("http://www.octopuslabs.com/")
    """
    def __init__(self, max_words=100, regexp=r"\w+[\w']+"):
        """Inits WordCloud with word limit and regex for tokenizing text"""
        self.max_words = max_words
        self.regexp = regexp
        self._raw_text = ''

    def generate(self, url):
        """This creates the frequency of the word counts from the given url"""
        self._raw_text = self._load_from_url(url)
        tokenized = self._tokenize(self._raw_text)
        frequencies = Counter(tokenized).most_common(self.max_words)
        # scale the word count to max 10, for font-size display
        max_wc = frequencies[0][1]
        wordcloud_ = [(word, self._size(wc, max_wc)) for word, wc in
                      frequencies]
        # return original word counts and the rescaled sizes
        return (frequencies, wordcloud_)

    def _size(self, word_count, max_wc):
        """Scale the original word count to the maximum font size"""
        return int(math.ceil(10 * word_count/max_wc))

    def _tokenize(self, text):
        """Tokenize the raw text.

        Remove stopwords from the text and splits the text into a list of words
        """
        text = map(lambda x: x.strip().lower(),
                   re.compile(self.regexp).findall(text))
        return [x for x in text if x not in STOPWORDS]

    def _load_from_url(self, url):
        "Reads the content of the URL"
        data = urllib2.urlopen(url).read()
        soup = BeautifulSoup(data, "html.parser")
        [s.extract() for s in soup(['style', 'script', '[document]', 'head',
                                    'title', 'meta'])]
        # remove comments
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]
        return soup.get_text()
