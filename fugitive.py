

from textblob import TextBlob
from cached_property import cached_property


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
        return TextBlob(self['Transcript'])


class Corpus:

    def __init__(self, path):
        self.path = path
