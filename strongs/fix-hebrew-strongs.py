#!/usr/bin/python
import re

H = {}

def load_word_hash():
    global H
    f = open('strongs-numbers/github.eliranwong/BHS-Strong-no/Strong_no_dictionary/SECEx/unique_lexeme.csv')

    l = f.readline()
    while l:


        l_ = l.rstrip('\n')

        m = re.search('H(\d+)\t([^_]*)(_\d+)?', l_)

        if m:
           H[m[1]] = m[2]
           

        l = f.readline()

def fix(lang):
    global H
    fi = open('strongs-numbers/hebrew-{:s}.@.pre'.format(lang))
    fo = open('strongs-numbers/hebrew-{:s}.@'    .format(lang), 'w')

    l = fi.readline()
    while l:
       
       m = re.search('^(A|H) @ (\d+) @ ([^@]+) @ (.*)', l)

       if m:
          fo.write(m[1] + ' @ ' + m[2] + ' @ ' + H[m[2]] + ' @ ' + m[4] + '\n')
       else:
          fo.write(l)


       l = fi.readline()



load_word_hash()
fix('en')
fix('de')
