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
cur.execute("""create table strongs_greek (
  nr       integer not null primary key,
  word     text    not null,
  text_de  text    not null
)""")

cur.execute("""create table strongs_greek_see (
  nr         integer not null,
  nr_greek   integer,
  nr_hebrew  integer
)""")


strongs_de_f = open('strongs-numbers/greek-de.@')
l = strongs_de_f.readline()
cur_strongs_de_nr = 1


last_strongs_nr = 0

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
           print('next_strongs_de_nr: {:d}'.format(next_strongs_de_nr))
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

       cur.execute('insert into strongs_greek(nr, word, text_de) values (?, ?, ?)', (strongs_nr, greek_unicode, text_de))

       for see in entry.findall("./see/[@language='GREEK']"):
           cur.execute('insert into strongs_greek_see(nr, nr_greek) values (?, ?)', (strongs_nr, int(see.attrib['strongs'])))

#      for see in entry.findall("./see/[@language='HEBREW']"):
#          print('x: ' + see.attrib['strongs'])


# TQ84's entries:
#
# δῶρον <--> χάρις
cur.execute('insert into strongs_greek_see(nr, nr_greek) values (?, ?)', (5485, 1435))
cur.execute('insert into strongs_greek_see(nr, nr_greek) values (?, ?)', (1435, 5485)) 

#
#  select count(*), nr, nr_greek from strongs_greek_see group by nr, nr_greek having count(*) > 1;
#
cur.execute('delete from strongs_greek_see where rowid in (select max(rowid) from strongs_greek_see group by nr, nr_greek having count(*) > 1)')

cur.execute('commit')
