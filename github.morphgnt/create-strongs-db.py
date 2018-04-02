import xml.etree.ElementTree as ET

import os.path
import sqlite3

tree = ET.parse('strongs-dictionary-xml/strongsgreek.xml')
root = tree.getroot()

db_name = 'strongs.db'
if os.path.isfile(db_name):
   os.remove(db_name)

db  = sqlite3.connect(db_name)
cur = db.cursor()
cur.execute("""create table strongs_greek (
  nr   integer not null primary key,
  word text    not null
)""")

cur.execute("""create table strongs_greek_see (
  nr         integer not null,
  nr_greek   integer,
  nr_hebrew  integer
)""")

for entry in root.findall('entries/entry'):

    greek      =     entry.find('./greek')
    if greek is not None:
       strongs_no = int(entry.findtext('./strongs'))
       greek_unicode = greek.attrib['unicode']

       cur.execute('insert into strongs_greek(nr, word) values (?, ?)', (strongs_no, greek_unicode))

       for see in entry.findall("./see/[@language='GREEK']"):
           cur.execute('insert into strongs_greek_see(nr, nr_greek) values (?, ?)', (strongs_no, int(see.attrib['strongs'])))

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
