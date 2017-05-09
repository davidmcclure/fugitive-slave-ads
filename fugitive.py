

import attr
import scandir
import re
import os

from textblob import TextBlob
from cached_property import cached_property
from collections import Counter

def scan_paths(root, pattern):
    """Given a top-level directory and path regex, generate paths recursively.
    """
    for root, dirs, files in scandir.walk(root):
        for name in files:
            if not pattern or re.search(pattern, name):
                yield os.path.join(root, name)

class Ad(dict):

    @classmethod
    def from_file(cls, path):
        """Load ad from text file.
        """
        with open(path) as fh:
            return cls.from_text(fh.read())

    @classmethod
    def from_text(cls, text):
        """Parse an ad text string.
        """
        fields = []

        for line in text.splitlines():

            split = line.find(':')

            key = line[:split]
            val = line[split+1:].strip()

            fields.append((key, val))

        return cls(fields)

    @cached_property
    def transcript_blob(self):
        """Spin up a cached blob on `Transcript`.
        """
        return TextBlob(self['Transcript']) if 'Transcript' in self else None


@attr.s
class Corpus:

    path = attr.ib()

    def paths(self):
        """Generate ad paths.
        """
        return scan_paths(self.path, '\.txt')

    def ads(self):
        """Generate ad instances.
        """
        for path in self.paths():
            ad = Ad.from_file(path)
            if ad.transcript_blob:
                yield ad
            print(path)

    def count_pos(self, *tags):
        """For a given POS tag, get word counts.
        """
        counts = Counter()

        for ad in self.ads():
            for token, pos in ad.transcript_blob.tags:
                if pos in tags:
                    counts[token.lower()] += 1

        return counts
