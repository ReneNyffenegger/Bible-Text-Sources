import os.path
import sqlite3
import textwrap

class db:
    def __init__(self, db_file_name): #_{

#       self.db_file_name = db_file_name
        db  = sqlite3.connect(db_file_name)
        self.cur = db.cursor()

    #_}
 
    def create_schema(self): #_{

#       if os.path.isfile(db_file_name):
#          os.remove(db_file_name)


        self.cur.execute('create table book (abbr text primary key, ord integer not null)')
    
        self.cur.execute(textwrap.dedent("""\
    create table verse(
      id  integer not null primary key,
      b   text not null references book,
      c   integer not null,
      v   integer not null,
      txt text null
    )"""))
    
        self.cur.execute(textwrap.dedent("""\
    create table word (
      v integer not null references verse,
      txt     text    not null,
      lemma   text    not null,    -- was: strongs text    not null, -- G\d\d\d\d / H\d\d\d\d / L\d\d\d\d\d
      parsed  text    not null,
      order_  integer not null
    )"""))
    
        self.cur.execute(textwrap.dedent("""\
    create view word_v as
      select
        v.b         ,
        v.c         ,
        v.v         ,
        v.id  v_id  ,
        w.txt word  ,
        w.lemma     , -- w.strongs   ,
        w.parsed    ,
        w.order_
      from
        verse v join
        word  w on v.id = w.v
      order by
        w.order_
    """))
        #_}

    def create_indices(self): #_{
        self.cur.execute('create index ix_word_v on word(v)')
    #_}
