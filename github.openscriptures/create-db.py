#!/bin/python
# vi: foldmarker=_{,_} foldmethod=marker

import re
import os
import sqlite3
import xml.etree.ElementTree as ET

db_name = 'wlc.db'
if os.path.isfile(db_name):
   os.remove(db_name)

db  = sqlite3.connect(db_name)
cur = db.cursor()

books = [ #_{
  {'nm': 'Gen'  , 'abbr': '1mo'   },
  {'nm': 'Exod' , 'abbr': '2mo'   },
  {'nm': 'Lev'  , 'abbr': '3mo'   },
  {'nm': 'Num'  , 'abbr': '4mo'   },
  {'nm': 'Deut' , 'abbr': '5mo'   },
  {'nm': 'Josh' , 'abbr': 'jos'   },
  {'nm': 'Judg' , 'abbr': 'ri'    },
  {'nm': 'Ruth' , 'abbr': 'rt'    },
  {'nm': '1Sam' , 'abbr': '1sam'  },
  {'nm': '2Sam' , 'abbr': '2sam'  },
  {'nm': '1Kgs' , 'abbr': '1koe'  },
  {'nm': '2Kgs' , 'abbr': '2koe'  },
  {'nm': '1Chr' , 'abbr': '1chr'  },
  {'nm': '2Chr' , 'abbr': '2chr'  },
  {'nm': 'Ezra' , 'abbr': 'esr'   },
  {'nm': 'Neh'  , 'abbr': 'neh'   },
  {'nm': 'Esth' , 'abbr': 'est'   },
  {'nm': 'Job'  , 'abbr': 'hi'    },
  {'nm': 'Ps'   , 'abbr': 'ps'    },
  {'nm': 'Prov' , 'abbr': 'spr'   },
  {'nm': 'Eccl' , 'abbr': 'koh'   },
  {'nm': 'Song' , 'abbr': 'hl'    },
  {'nm': 'Isa'  , 'abbr': 'jes'   },
  {'nm': 'Jer'  , 'abbr': 'jer'   },
  {'nm': 'Lam'  , 'abbr': 'kla'   },
  {'nm': 'Ezek' , 'abbr': 'hes'   },
  {'nm': 'Dan'  , 'abbr': 'dan'   },
  {'nm': 'Hos'  , 'abbr': 'hos'   },
  {'nm': 'Joel' , 'abbr': 'joe'   },
  {'nm': 'Amos' , 'abbr': 'am'    },
  {'nm': 'Obad' , 'abbr': 'ob'    },
  {'nm': 'Jonah', 'abbr': 'jon'   },
  {'nm': 'Mic'  , 'abbr': 'mi'    },
  {'nm': 'Nah'  , 'abbr': 'nah'   },
  {'nm': 'Hab'  , 'abbr': 'hab'   },
  {'nm': 'Zeph' , 'abbr': 'zeph'  },
  {'nm': 'Hag'  , 'abbr': 'hag'   },
  {'nm': 'Zech' , 'abbr': 'sach'  },
  {'nm': 'Mal'  , 'abbr': 'mal'   },
] #_}

def create_db_schema(): #_{
    cur.execute('create table book (abbr text primary key, ord integer not null)')
    cur.execute("""create table verse(
  id  integer not null primary key,
  b   text not null references book,
  c   integer not null,
  v   integer not null,
  txt text null
)""")

    cur.execute("""create table word (
  v integer not null references verse,
  txt     text    not null,
  strongs text    not null, -- G\d\d\d\d
  parsed  text    not null,
  no   integer    not null
)""")

    cur.execute("""create view word_v as
  select
    v.b         ,
    v.c         ,
    v.v         ,
    v.id  v_id  ,
    w.txt word  ,
    w.strongs   ,
    w.parsed    ,
    w.no
  from
    verse v join
    word  w on v.id = w.v
  order by
    w.no
""")

#_}
    

def load_book(book, book_order): #_{

    cur.execute('insert into book values(?, ?)', (book['abbr'], book_order))

    ns = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'

    xml  = ET.parse('morphhb/wlc/' + book['nm'] + '.xml')
    root = xml.getroot()
    osisText = root.find(ns + "osisText")
    book     = osisText.find(ns+"div[@type='book']")

    word_no = 0

    c = 0
    for chapter in book.findall(ns + 'chapter'): #_{
        c += 1

        v = 0
        for verse in chapter.findall(ns + 'verse'):
            v += 1

#           cur.execute('insert into verse (b, c, v, txt) values (?, ?, ?, ?)', (book['abbr'], c, v, 'todo: verse text'))

            for elem in verse.findall('*'): #_{
#               if elem.tag not in [ns + 'w', ns + 'seg', ns + 'note']:
#                  raise Exception('word.tag: ' + elem.tag)

                if   elem.tag == ns + 'w':
                     pass
                elif elem.tag == ns + 'seg':


                     if elem.attrib['type'] not in ['x-samekh', 'x-sof-pasuq', 'x-paseq', 'x-pe', 'x-maqqef', 'x-reversednun']:
                        print (elem.attrib['type'])
#                       raise Exception('elem.type = ' + elem.attrib['type'])

#               print(word.tag)
#               lemma = word.attrib['lemma']
#               lemma = re.sub(r'\D', '', lemma)
#               print (lemma)

            #_}

#           print(str(c) + ':' + str(v))

            w = 0

    #_}

#_}


create_db_schema()

book_order = 0
for book in books:
    book_order += 1
    load_book(book, book_order)

cur.execute('commit')
