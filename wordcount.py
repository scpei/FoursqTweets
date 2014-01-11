#!/usr/bin/python

# python si-601-lab-5.py input.txt
# Some codes used courtesy of Dr. Yuhang Wang.

from mrjob.job import MRJob
import re
from operator import itemgetter, attrgetter

WORD_RE = re.compile(r"[\w]+")

class BiGramFreqCount(MRJob):
  DEFAULT_OUTPUT_PROTOCOL = 'raw_value'
  ### input: self, in_key, in_value
  def mapper(self, _, line):
    words = WORD_RE.findall(line)
    #words = line.split()
    for word in words:
      yield(word.lower(), 1)
  
  ### input: self, in_key from mapper, in_value from mapper
  def reducer(self, key, values):
    yield (key, sum(values))
    #yield (key, sum(values)).sort(key=lambda x:x[1],reverse=True)

if __name__ == '__main__':
  BiGramFreqCount.run()

