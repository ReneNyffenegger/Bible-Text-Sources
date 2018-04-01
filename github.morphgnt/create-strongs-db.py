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
cur.execute("""create table strongs (
  nr   integer not null primary key,
  word text    not null
)""")

for entry in root.findall('entries/entry'):

    greek      =     entry.find('./greek')
    if greek is not None:
       strongs_no = int(entry.findtext('./strongs'))
       greek_unicode = greek.attrib['unicode']
       cur.execute('insert into strongs(nr, word) values (?, ?)', (strongs_no, greek_unicode))

cur.execute('commit')
