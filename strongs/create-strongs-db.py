#!/usr/bin/python

import sys
import os.path
import re

import sqlite3
import xml.etree.ElementTree as ET

tree = ET.parse('github.morphgnt/strongs-dictionary-xml/strongsgreek.xml')
root = tree.getroot()

db_name = 'strongs.db'
if os.path.isfile(db_name):
   os.remove(db_name)

db  = sqlite3.connect(db_name)
cur = db.cursor()

cur.execute("""create table strongs (
  nr       text    not null primary key, -- G\d\d\d\d or H\d\d\d\d
  word     text    not null,
  text_de  text    not null
)""")

cur.execute("""create table strongs_see (
  nr_1       text not null references strongs,
  nr_2       text not null references strongs,
  unique (nr_1, nr_2)
)""")


strongs_de_f = open('strongs-numbers/greek-de.@')
l = strongs_de_f.readline()
cur_strongs_de_nr = 1

gerhard_kautz_f = open('strongs-numbers/Gerhard-Kautz/translation-de.txt')
gerhard_kautz_strongs_nr = 0

last_strongs_nr = 0


def extract_gerhard_kautz_I(t):
    t = re.sub(r'\bI\.\)<br>', 'I.) ', t)
    m = re.search(r'\bI\.\) *([^<]*)', t)
    if not m:
       return None

    r = re.sub(r'\bintr\.: *', '', m[1])
    r = re.sub(r'\bsubst\.: *', '', r)
    r = re.sub(r'\bsubst\. *', '', r)
    r = re.sub(r'\bPtz\. *', '', r)
    r = re.sub(r'\bPräs\. *', '', r)
    r = re.sub(r'\bPass\.: *', '', r)
    r = re.sub(r'\bPl\.: *', '', r)
    r = re.sub(r'\badj\.: *', '', r)
    r = re.sub(r'\badj\.: *', '', r)
    r = re.sub(r'\bd\. *', '', r)
    r = re.sub(r'\bübertr.: *', '', r)
    r = re.sub(r'\bMed\. *', '', r)
    r = re.sub(r'\btr\.: *', '', r)
    r = re.sub(r'\bzeitl\.: *', '', r)
    r = re.sub(r'\bAkt\.: *', '', r)
    r = re.sub(r'\bInf\.: *', '', r)
    r = re.sub(r'^ *: *', '', r)
    return r

for entry in root.findall('entries/entry'):

    text_de = ''
    while True:
    
        l = strongs_de_f.readline()
        if not l:
           cur_strongs_de_nr = next_strongs_de_nr
           break
    
        m = re.search('^(\d+) *@', l)
        if m:
           next_strongs_de_nr = int(m[1])
#          print('next_strongs_de_nr: {:d}'.format(next_strongs_de_nr))
           if cur_strongs_de_nr != next_strongs_de_nr - 2:
              print('! next_strongs_de_nr: {:d}, cur_strongs_de_nr: {:d}'.format(next_strongs_de_nr, cur_strongs_de_nr))
    
           cur_strongs_de_nr = next_strongs_de_nr -1
           break
        else:
           text_de += l

#   print ('... cur_strongs_de_nr: {:d}'.format(cur_strongs_de_nr))
#   print (text_de)
#   sys.exit(1)

    greek = entry.find('./greek')
    if greek is not None:
       strongs_nr = int(entry.findtext('./strongs'))

       if cur_strongs_de_nr != strongs_nr:
          raise Exception('cur_strongs_de_nr: {:d}, strongs_nr: {:d}'.format(cur_strongs_de_nr, strongs_nr))

       greek_unicode = greek.attrib['unicode']

       if strongs_nr < last_strongs_nr:
          print('cur_strongs_nr={:d}, strongs_nr={:d}'.format(strongs_nr, cur_strongs_nr))
          sys.exit(1)

       last_strongs_nr = strongs_nr


    #  Read next entry for Gerhard Kautz

       if gerhard_kautz_strongs_nr < strongs_nr:
          gerhard_kautz_l = gerhard_kautz_f.readline()
          gerhard_kautz_strongs_nr_, gerhard_kautz_transliteration, gerhard_kautz_rest = gerhard_kautz_l.split("\t")
          gerhard_kautz_rest = gerhard_kautz_rest.rstrip()
#         print("Read: {:s}".format(gerhard_kautz_strongs_nr_))
          gerhard_kautz_strongs_nr=int(gerhard_kautz_strongs_nr_)

       if gerhard_kautz_strongs_nr == strongs_nr:
          gerhard_kautz_I = extract_gerhard_kautz_I(gerhard_kautz_rest)
          if gerhard_kautz_I:
             print("{:d}: {:s}".format(gerhard_kautz_strongs_nr, gerhard_kautz_I))
          else:
             print("{:d}: {:s}".format(gerhard_kautz_strongs_nr, 'n/a'))
#         print("gerhard_kautz_strongs_nr: {:d}, strongd: {:d}".format(gerhard_kautz_strongs_nr, strongs_nr))

#      else:
#         print("gerhard_kautz_strongs_nr: {:d}, strongd: {:d}".format(gerhard_kautz_strongs_nr, strongs_nr))


    #  ---------------------------------

       cur.execute('insert into strongs(nr, word, text_de) values (?, ?, ?)', ('G' + str(strongs_nr).zfill(4), greek_unicode, text_de))

       strongs_derivations=entry.findall('./strongs_derivation')
       if strongs_derivations is not None:
          if   len(strongs_derivations) == 0:
               pass
          elif len(strongs_derivations) > 1:
               raise Exception('strongs_nr: {:d}, len(strongs_derivations) = {:d}'.format(strongs_nr, len(strongs_derivations)))
          else:
               for strongsref in strongs_derivations[0].findall("./strongsref[@language='GREEK']"):
#                  print(strongsref.attrib['strongs'])
                   try:
                     cur.execute('insert into strongs_see(nr_1, nr_2) values (?, ?)', ('G' + str(strongs_nr).zfill(4), 'G' + strongsref.attrib['strongs'].zfill(4) ))
                   except sqlite3.IntegrityError as e:
                     print('* Could not insert ' + str(e))

#      for see in entry.findall("./see/[@language='GREEK']"):

#      for see in entry.findall("./see/[@language='HEBREW']"):
#          print('x: ' + see.attrib['strongs'])


# TQ84's entries:
#
# δῶρον <--> χάρις
cur.execute('insert into strongs_see(nr_1, nr_2) values (?, ?)', ('G5485', 'G1435'))
cur.execute('insert into strongs_see(nr_1, nr_2) values (?, ?)', ('G1435', 'G5485')) 

#
#  select count(*), nr, nr_greek from strongs_greek_see group by nr, nr_greek having count(*) > 1;
#
# cur.execute('delete from strongs_greek_see where rowid in (select max(rowid) from strongs_greek_see group by nr, nr_greek having count(*) > 1)')

cur.execute('commit')
