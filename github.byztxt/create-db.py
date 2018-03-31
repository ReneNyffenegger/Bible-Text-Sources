import re
import sys
import sqlite3
import os.path

books = [
  {'nm': 'MT'  , 'abbr': 'mt'   },
  {'nm': 'MR'  , 'abbr': 'mk'   },
  {'nm': 'LU'  , 'abbr': 'lu'   },
  {'nm': 'JOH' , 'abbr': 'joh'  },
  {'nm': 'AC'  , 'abbr': 'apg'  },
  {'nm': 'RO'  , 'abbr': 'roem' },
  {'nm': '1CO' , 'abbr': '1kor' },
  {'nm': '2CO' , 'abbr': '2kor' },
  {'nm': 'GA'  , 'abbr': 'gal'  },
  {'nm': 'EPH' , 'abbr': 'eph'  },
  {'nm': 'PHP' , 'abbr': 'phil' },
  {'nm': 'COL' , 'abbr': 'kol'  },
  {'nm': '1TH' , 'abbr': '1thes'},
  {'nm': '2TH' , 'abbr': '2thes'},
  {'nm': '1TI' , 'abbr': '1tim' },
  {'nm': '2TI' , 'abbr': '2tim' },
  {'nm': 'TIT' , 'abbr': 'tit'  },
  {'nm': 'PHM' , 'abbr': 'phim' },
  {'nm': 'HEB' , 'abbr': 'hebr' },
  {'nm': 'JAS' , 'abbr': 'jak'  },
  {'nm': '1PE' , 'abbr': '1petr'},
  {'nm': '2PE' , 'abbr': '2petr'},
  {'nm': '1JO' , 'abbr': '1joh' },
  {'nm': '2JO' , 'abbr': '2joh' },
  {'nm': '3JO' , 'abbr': '3joh' },
  {'nm': 'JUDE', 'abbr': 'jud'  },
  {'nm': 'RE'  , 'abbr': 'offb' },
]

db_name = 'BP5.db'
if os.path.isfile(db_name):
   os.remove(db_name)

db  = sqlite3.connect(db_name)
cur = db.cursor()
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
  txt  text not null,
  no   integer not null
)""")

book_order = 1
for book in books:

    cur.execute('insert into book values(?, ?)', (book['abbr'], book_order))
    book_order += 1

    with open('byzantine-majority-text/parsed/' + book['nm'] + '.BP5') as b: book_text = b.read()
#   print (book_text)
#   print(b['nm'])
    verses = re.split("\n\\s+", book_text)
#   print(verses[0])

    prev_chapt_no = 0

    word_no = 1

    v=0
    for verse_ in verses:
        v += 1
        try:
          verse = re.sub('^ *', '' , verse_)
          verse = re.sub('\s+', ' ', verse )
#         print (verse)
          match = re.search('^(\d+):(\d+) ?(.*)', verse)
          chapt_no = int(match.group(1))
          verse_no = int(match.group(2))
          verse_txt=     match.group(3)


          if chapt_no == prev_chapt_no:

             if verse_no != prev_verse_no + 1:
                raise Exception('!')


          elif chapt_no == prev_chapt_no + 1:
              prev_chapt_no = chapt_no

              if verse_no != 1:
                 raise Exception('!')

          else:
              raise Exception('! ' + book['nm'] + ': chapt_no = ' + str(chapt_no) + ', verse_no = ' + str(verse_no) + ', prev_chapt_no = ' + str(prev_chapt_no) + ', prev_verse_no = ' + str(prev_verse_no))


#         print (str(chapt_no) + ', ' + str(verse_no))

          prev_verse_no = verse_no

#         cur.execute('insert into verse values(?, ?, ?, ?)', (book['abbr'], chapt_no, verse_no, verse_txt))
          cur.execute('insert into verse (b, c, v, txt) values (?, ?, ?, ?)', (book['abbr'], chapt_no, verse_no, verse_txt))

          rowid_verse = cur.lastrowid

          words = re.findall('(\w+ (?:\d+ )+{[^}]+} *)', verse_txt)
          for word in words:
              cur.execute('insert into word (v, txt, no) values (?,?,?)', (rowid_verse, word, word_no))
              word_no += 1

    


        except BaseException as e:
          print('! Oops ' + str(e) + ' in ' + book['nm'] + ', verse_ = ' + verse_ + ', v = ' + str(v))
          sys.exit(1)

    
#   break

cur.execute('commit')
