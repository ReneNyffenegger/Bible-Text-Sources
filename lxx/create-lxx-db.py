#!/bin/python
# vi: foldmarker=_{,_} foldmethod=marker
# # -*- coding: utf-8 -*-


import importlib.util
import os
import re


class verse_alignment:
      def __init__(self): #_{
          self.f = open('../github.eliranwong/LXX-Rahlfs-1935/01_wordlist_unicode/alignment_with_OSSP/E-verse.csv')
          self.next_book     ='?'
          self.next_verse_no = 0
          self.next_chap_no  = 0
          self.next_verse()
          self.next_verse()
      #_}

#     def next_verse(self):
#         self.word_from = self.word_till

      def next_verse(self): #_{
          word_to_verse_l = self.f.readline()
          m = re.search('(\d+)\t\d+\t「(\w+) (\d+):(\d+)」', word_to_verse_l)

          if not m:
             raise Exception('word_to_verse_l: {:s}'.format(word_to_verse_l))

          self.word_till = int(m[1]) - 1

          self.book     = self.next_book
          self.chap_no  = self.next_chap_no
          self.verse_no = self.next_verse_no

#         self.word_from = self.next_word_from - 1
#         self
#         self.next_verse_word_from = int(m[1])
          self.next_book      =     m[2]
          self.next_chap_no   = int(m[3])
          self.next_verse_no  = int(m[4])
      #_}


def load_text():
    v = verse_alignment()
    words = open('../github.eliranwong/LXX-Rahlfs-1935/01_wordlist_unicode/text_accented.csv')

    words_l = words.readline()
    while words_l: #_{
      m = re.search('(\d+)\t\d+\t(\w+)', words_l)
      if not m:
         raise Exception('words_l')

      word_no = int(m[1])
      if word_no > v.word_till:
         v.next_verse()

      print('{:20s} {:4s} {:3d}:{:3d} {:d}'.format(m[2], v.book, v.chap_no, v.verse_no, word_no))

      words_l = words.readline()

    #_}

spec   = importlib.util.spec_from_file_location('?', '../lib/DBTranslation.py')
dbTrx  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dbTrx)


db_file_name = 'lxx.db'
if os.path.isfile(db_file_name):
   os.remove(db_file_name)


db_lxx = dbTrx.db(db_file_name)
db_lxx.create_schema()


load_text()

db_lxx.create_indices()
# db_lxx.cur.execute('commit')
