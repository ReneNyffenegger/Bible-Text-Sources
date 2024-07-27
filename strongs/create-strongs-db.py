#!/usr/bin/python3
# vi: foldmarker=_{,_} foldmethod=marker

import sys
import os.path
import re

import sqlite3
import xml.etree.ElementTree as ET

tree_greek = ET.parse('github.morphgnt/strongs-dictionary-xml/strongsgreek.xml')
root_greek = tree_greek.getroot()

db_name = 'strongs.db'
if os.path.isfile(db_name):
   os.remove(db_name)

db  = sqlite3.connect(db_name)
cur = db.cursor()

#_{ Create tables

cur.execute(r"""create table strongs (
  nr              text    not null primary key, -- G\d\d\d\d or H\d\d\d\d
  word            text    not null,
  lang            text    not null check (lang in ('G', 'H', 'A')), -- Greek, Hebrew, Aramaeic
  gerhard_kautz_I text,
  word_de         text,
  note_de         text,
  strongs_en      text    not null,
  strongs_de      text    not null,
  flag            text
)""")


# Corresponds to strongs_see
cur.execute("""create table strongs_syn ( 
  id          integer not null primary key,
  short       text    not null,
  description text    not null
)""")

# Corresponds to strongs_rel_entry
cur.execute("""create table strongs_syn_entry (
  id          integer not null references strongs_syn,
  nr          text not null references strongs
)""")


cur.execute("""create table strongs_see (
  id          integer primary key,
  description text not null
)""")

cur.execute("""create table strongs_see_entry (
  id          integer not null references strongs_see,
  nr          text not null references strongs
)""")

cur.execute("""create table strongs_noun_adj_verb (
  noun       text references strongs,
  adj        text references strongs,
  verb       text references strongs
)""")

cur.execute("""create table strongs_root (
  nr         text references strongs,
  root       text references strongs,
  unique (nr, root)
)""")

# TODO: Proabably, an index on strongs_root(root) would not hurt.

#_}

strongs_xx      = {}

for xx in ['de', 'en']:
  strongs_xx[xx] = {}
  strongs_xx[xx]['f'   ] = open('strongs-numbers/greek-{:s}.@'.format(xx), 'r', encoding='utf-8')
  strongs_xx[xx]['line'] = strongs_xx[xx]['f'].readline()
  strongs_xx[xx]['next_strongs_nr'] = 1

gerhard_kautz_f = open('strongs-numbers/Gerhard-Kautz/translation-de.txt')
gerhard_kautz_strongs_nr = 0

last_strongs_nr = 0

def read_strong(lang, nr_expected): #_{
    global strongs_xx
    ret  = strongs_xx[lang]['line']

    if nr_expected != strongs_xx[lang]['next_strongs_nr']:
        print('! nr_expected: {:d}, next_strongs_en_nr: {:d}'.format(nr_expected, strongs_xx[lang]['next_strongs_nr']))


    while True:
      strongs_xx[lang]['line'] = strongs_xx[lang]['f'].readline()

      if not strongs_xx[lang]['line']:
         return ret

      m = re.search(r'^(\d+) *@', strongs_xx[lang]['line'])
      if m:
         strongs_xx[lang]['next_strongs_nr'] = int(m[1])
         return ret
      else:
         ret += strongs_xx[lang]['line']
#_}

def extract_gerhard_kautz_I(t): #_{
    t = re.sub(r'\bI\.\)<br>', 'I.) ', t)
    m = re.search(r'\bI\.\) *([^<]*)', t)
    if not m:
       return None

    r = re.sub(r'\bintr\.: *' , '', m[1])
    r = re.sub(r'\bsubst\.: *', '', r)
    r = re.sub(r'\bsubst\. *' , '', r)
    r = re.sub(r'\bPtz\. *'   , '', r)
    r = re.sub(r'\bPräs\. *'  , '', r)
    r = re.sub(r'\bPass\.: *' , '', r)
    r = re.sub(r'\bPl\.: *'   , '', r)
    r = re.sub(r'\badj\.: *'  , '', r)
    r = re.sub(r'\badj\.: *'  , '', r)
    r = re.sub(r'\bd\. *'     , '', r)
    r = re.sub(r'\bübertr.: *', '', r)
    r = re.sub(r'\bbildl\.: *', '', r)
    r = re.sub(r'\bMed\. *'   , '', r)
    r = re.sub(r'\btr\.: *'   , '', r)
    r = re.sub(r'\bzeitl\.: *', '', r)
    r = re.sub(r'\bAkt\.: *'  , '', r)
    r = re.sub(r'\bInf\.: *'  , '', r)
    r = re.sub(r'^ *: *'      , '', r)
    return r
#_}

def update_strongs(): #_{

    raise Exception('update_strongs should not be used anymore!')

    def do_(nr, new_word):
        cur.execute('update strongs set word_de = ? where nr = ?', (new_word, nr))

    do_('G0098', 'adramytisch'                     )
    do_('G0102', 'unfähig'                         ) # akt. von Personen: unvermögend
    do_('G0235', 'sondern'                         )
    do_('G0244', 'Einmischender'                   )
    do_('G0302', '-'                               ) # Modalpartikel welche meist unübersetzbar ist; bezeichnet Handlung
    do_('G0450', 'aufstehen'                       ) # tr. (Aor.1 und Fut.Akt.): aufstellen
    do_('G0657', 'sich verabschieden'              ) # sich (als Zurückbleibender) verabschieden
    do_('G0685', 'Fluchen'                         )
    do_('G0855', 'unsichtbar'                      ) # ..er ward entschwunden, weg von ihnen...
    do_('G0868', 'entfernen'                       ) # tr. (im , Impf., Fut. und Aor1): abtrünnig machen)
    do_('G0942', 'an der andern Seite vorübergehen') # an der gegenüberliegenden (Straßenseite) vorübergehen
    do_('G0940', 'bezaubern'                       ) # jmd. verhexen
    do_('G1063', 'denn'                            )
    do_('G1174', 'gottergeben'                     ) # als Komp. (für Superl.): mehr Götter fürchtend...
    do_('G1121', 'Schrift'                         ) # Schrift-
    do_('G1473', '-'                               ) # ich (mein, mir, mich); betont: i c h (m e i n, m i r, m i c h)
    do_('G1503', 'ähneln'                          ) # Perfekt mit Präsensbedeutung: ist ähnlich...
    do_('G1519', 'in'                              ) # örtl.: hinein...in
    do_('G1537', 'aus'                             ) # aus...(heraus)
    do_('G1563', 'dort'                            ) # als Antwort auf Frage: Wo?: dort
    do_('G1565', 'jener'                           ) # ἐκεῖνος - jene (-er, -es, en, usw.)
    do_('G1608', 'rum-huren'                       ) # Aor.fem.: außergewöhnlich gehurt-Habende
    do_('G1626', 'Fehlgeburt'                      ) # εκτρωματι - verächtlich: Fehlgeburt
    do_('G1646', 'gering'                          ) # als Superl., Geringste
    do_('G1715', 'vor'                             ) # als Adv.: (nach) vorne
    do_('G1722', 'in'                              ) # örtl.: auf
    do_('G1909', 'auf'                             ) # örtl.: auf
    do_('G1276', 'überqueren'                      ) # zum jenseitigen (Ufer) queren
    do_('G2078', 'zuletzt'                         ) # ὡσπερεί - örtl.: äußerste
    do_('G2192', 'haben'                           ) # Akt. haben
    do_('G2193', 'bis'                             ) # als Konj. - solange bis...
    do_('G2228', 'oder'                            ) # trennend: oder
    do_('G2443', 'damit'                           ) # damit...
    do_('G2476', 'stellen'                         ) # tr.(, Impf., Aor.1 Akt. und Fut.Akt.): stellen
    do_('G2532', 'und'                             )
    do_('G2596', 'herab'                           ) # räuml.: herab
    do_('G3101', 'Jünger'                          ) # Schüler
    do_('G3195', 'erwarten'                        )
    do_('G3326', 'inmitten'                        ) # örtl. inmitten
    do_('G3467', 'kurzsichtig'                     )
    do_('G3588', '-'                               )
    do_('G3694', 'hinten'                          ) # als Antwort auf Frage: Wo?: hinten
    do_('G3704', 'damit'                           )
    do_('G3739', 'refl. pr.'                       ) # welche (-er, -en, -es, usw.)
    do_('G3748', 'jeder, der'                      ) # verallgemeinernd: jeder, der...
    do_('G3754', 'daß'                             ) # daß...
    do_('G3756', 'nicht'                           ) # nein
    do_('G3760', 'keineswegs'                      ) # durchaus nicht
    do_('G3762', 'niemand'                         ) # nicht ein (-er, -e, -en, -es, usw.)
    do_('G3801', '-'                               ) # der "Seiende" und der "Er war" und der "Kommende"
    do_('G3825', 'zurück'                          ) # örtl.: zurück
    do_('G3936', 'beistehen'                       ) # im Akt. , Ipf., Aor.1, und Fut.): darstellen
    do_('G3956', 'alle'                            )
    do_('G4007', 'sehr'                            ) # im NT immer an ein anderes Wort angehängt um diesem eine positive<br>Betonung zu geben - hervorhebend oder verschärfend: ... wirklich; ... anders;<br>durchaus; eben.
    do_('G4012', 'herum'                           ) # περί - betreffs...
    do_('G4049', 'umhergerissen'                   ) # Ind.Impf....war ständig hin- und hergerissen
    do_('G4106', 'Irrtum'                          ) # im passiven Sinn: Irrtum
    do_('G4151', 'Geist'                           ) # Hauch
    do_('G4314', 'für'                             ) # zugunsten von...
    do_('G4381', 'Ansehen-Betrachtender'           ) # der auf Ansehen (Person Rücksicht) Nehmende
    do_('G4357', 'verharren'                       ) # weiterhin bleiben bei...
    do_('G4595', 'verfault'                        ) # intr. Ind.Pf.Akt. im pass. Sinn: verfault
    do_('G4697', 'erbarmen'                        ) # erbarmen
    do_('G4758', 'anwerben'                        ) # Aor.: zum Kriegsdienst angeworben Habende
    do_('G4886', 'Band'                            ) # (zusammenhaltende) Band
    do_('G4970', 'sehr'                            ) # in Verbindung mit einem Adj. oder einem Zeitwort: sehr ...
    do_('G4992', 'Heil'                            ) # als Adj. ohne Art., prädikativ: Errettung bringend (für)...
    do_('G5100', 'jemand'                          ) # irgendeiner, -e, -es
    do_('G5101', 'wer'                             ) # wer (was, welcher)
    do_('G5104', 'sicher'                          ) # wird nur in Verbindung mit anderen Partikeln gebraucht: gewiß
    do_('G5259', 'von'                             ) # von...
    do_('G5435', 'Gerücht'                         ) # Kunde
    do_('G5503', 'Witwe'                           )
    do_('G5537', 'anweisen'                        ) # (göttliche) Weisung erteilen
    do_('G5578', 'falscher Prophet'                ) # falsche Prophet
    do_('G5580', 'falscher Messias'                ) # ψευδόχριστος - falsche Messiase
    do_('G5424', 'Zwerchfell'                      ) # Verstand(esregungen)
    do_('G5616', 'wie'                             ) # vergleichend: gleichsam wie...
    do_('G5619', 'gleichsam'                       ) # ὡσπερεί - ganz genauso wie bei...
#_}

def noun_adj_verb(): #_{

    cur.execute('insert into strongs_noun_adj_verb values (?, ?, ?)', ('G1124',  None  , 'G1121')) # γραφή  - γράφω
    cur.execute('insert into strongs_noun_adj_verb values (?, ?, ?)', ('G2549', 'G2556', None   )) # κακία  - κακός
    cur.execute('insert into strongs_noun_adj_verb values (?, ?, ?)', ('G5162',  None  , 'G5142')) # τροφός - τρέφω
    cur.execute('insert into strongs_noun_adj_verb values (?, ?, ?)', ('H8318',  None  , 'H8317')) # wimmeln - Gewimmel

#_}

#q def see_also(nr_1, nr_2): #_{
#q     try:
#q       cur.execute('insert into strongs_see(nr_1, nr_2) values (?, ?)', (nr_1, nr_2))
#q     except sqlite3.IntegrityError as e:
#q       print('! {:s} nr_1 = {:s}, nr_2 = {:s}'.format(str(e), nr_1, nr_2))
#q     try:
#q       cur.execute('insert into strongs_see(nr_1, nr_2) values (?, ?)', (nr_2, nr_1))
#q     except sqlite3.IntegrityError as e:
#q       print('! {:s} nr_1 = {:s}, nr_2 = {:s}'.format(str(e), nr_1, nr_2))
#q 
#q #_}

def load_hebrew(): #_{

    cur_hebr_word  = ''
#   next_hebr_word = 'אָב'
    cur_hebr_lang  = ''
#   next_hebr_lang = 'A'
    strongs_xx_hebr = {}
#   cur_hebr_nr = 0

#   global strongs_xx_hebr


    def read_strong_hebr(lang, nr_expected): #_{
        nonlocal strongs_xx_hebr
#       nonlocal next_hebr_lang
#       nonlocal next_hebr_word
        nonlocal cur_hebr_lang
        nonlocal cur_hebr_word
        ret  = strongs_xx_hebr[lang]['line']
    
        if nr_expected != strongs_xx_hebr[lang]['next_strongs_nr']:
            print('! nr_expected: {:d}, next_strongs_en_nr: {:d}'.format(nr_expected, strongs_xx_hebr[lang]['next_strongs_nr']))
    
    
        while True:
          strongs_xx_hebr[lang]['line'] = strongs_xx_hebr[lang]['f'].readline()
    
          if not strongs_xx_hebr[lang]['line']:
             return ret
    
          m = re.search(r'^(A|H) @ (\d+) @ ([^@]+) @', strongs_xx_hebr[lang]['line'])
          if m:
             strongs_xx_hebr[lang]['next_strongs_nr'] = int(m[2])


             if lang == 'en':
#               cur_hebr_lang = next_hebr_lang
#               cur_hebr_word = next_hebr_word

                data_strongs.line(r'^(H\d\d\d\d) (.) (.*)')

# q cl          data_strongs_l = data_strongs_f.readline()
# q cl          data_strongs_m = re.search('^(H\d\d\d\d) (.) (.*)', data_strongs_l)
# q cl          cur_hebr_lang = data_strongs_m[2]
# q cl          cur_hebr_word = data_strongs_m[3]

                cur_hebr_lang = data_strongs.re_group(2)
                cur_hebr_word = data_strongs.re_group(3)

#               next_hebr_lang = m[1]
#               next_hebr_word = m[3]
                

             return ret
          else:
             ret += strongs_xx_hebr[lang]['line']
    #_}


    for xx in ['de', 'en']: #_{
       strongs_xx_hebr[xx] = {}
       strongs_xx_hebr[xx]['f'   ] = open('strongs-numbers/hebrew-{:s}.@'.format(xx), 'r', encoding='utf-8')
       strongs_xx_hebr[xx]['line'] = strongs_xx_hebr[xx]['f'].readline()
       strongs_xx_hebr[xx]['next_strongs_nr'] = 1
    #_}

    for strongs_nr_hebr in range(1, 8674):
        strongs_en_hebr = read_strong_hebr('en', strongs_nr_hebr)
        strongs_de_hebr = read_strong_hebr('de', strongs_nr_hebr)

        data_uebersetzung.line(r'^(H\d\d\d\d) (.*)')
        data_bemerkung   .line(r'^(H\d\d\d\d) (.*)')
        data_flags       .line(r'^(H\d\d\d\d) (.)' )

#       flag          = data_uebersetzung.re_group(2)
        flag          = data_flags.re_group(2)
        if flag == ' ':
           flag = None

        word_de       = data_uebersetzung.re_group(2)
        note_de       = data_bemerkung   .re_group(2)

        if word_de == '':
           word_de =  '' # 'n/a'


        cur.execute('insert into strongs(nr, word, lang, word_de, note_de, strongs_en, strongs_de, flag) values (?, ?, ?, ?, ?, ?, ?, ?)', ('H' + str(strongs_nr_hebr).zfill(4), cur_hebr_word, cur_hebr_lang, word_de, note_de, strongs_en_hebr, strongs_de_hebr, flag))

#_}

class strongs_file: #_{
    def __init__(self, file_name):
        self.f = open('data/{:s}'.format(file_name), 'r', encoding='utf-8')

    def line(self, re_pattern):
        l = self.f.readline()
        self.m = re.search(re_pattern, l)

    def re_group(self, group):
        if self.m is None:
           return None
        return self.m[group]
#_}

data_strongs      = strongs_file('strongs'     )
data_uebersetzung = strongs_file('uebersetzung')
data_flags        = strongs_file('flags'       )
data_bemerkung    = strongs_file('bemerkung'   )

for entry in root_greek.findall('entries/entry'): #_{


    strongs_de = ''
    strongs_en = ''

    greek = entry.find('./greek')
    if greek is not None:
       strongs_nr = int(entry.findtext('./strongs'))


#      greek_unicode = greek.attrib['unicode']


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

          if False:
             if gerhard_kautz_I:
                print("{:d}: {:s}".format(gerhard_kautz_strongs_nr, gerhard_kautz_I))
             else:
                print("{:d}: {:s}".format(gerhard_kautz_strongs_nr, 'n/a'))
   #         print("gerhard_kautz_strongs_nr: {:d}, strongd: {:d}".format(gerhard_kautz_strongs_nr, strongs_nr))

       else:
          gerhard_kautz_I = None


    #  ---------------------------------

       strongs_en = read_strong('en', strongs_nr)
       strongs_de = read_strong('de', strongs_nr)
#      print(strongs_en)


       data_strongs     .line(r'^(G\d\d\d\d) (.) (.*)')
       data_uebersetzung.line(r'^(G\d\d\d\d) (.*)')
       data_bemerkung   .line(r'^(G\d\d\d\d) (.*)')
       data_flags       .line(r'^(H\d\d\d\d) (.)' )

       flag          = data_flags.re_group(2)

       if flag == ' ':
          flag = None

       greek_lang    = data_strongs.re_group(2)
       greek_unicode = data_strongs.re_group(3)

       word_de       = data_uebersetzung.re_group(2)
       note_de       = data_bemerkung   .re_group(2)



#      print('nr {:4d} {:s} - {:20s} {:20s}'.format(strongs_nr, data_strongs_m[1], greek_unicode, data_strongs_m[2]))
#      cur.execute('insert into strongs(nr, word, lang, word_de, strongs_en, strongs_de) values (?, ?, "G", ?, ?, ?)', ('G' + str(strongs_nr).zfill(4), greek_unicode, gerhard_kautz_I, strongs_en, strongs_de))
       cur.execute('insert into strongs(nr, word, lang, gerhard_kautz_I, word_de, note_de, strongs_en, strongs_de, flag) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', ('G' + str(strongs_nr).zfill(4), greek_unicode, greek_lang, gerhard_kautz_I, word_de, note_de, strongs_en, strongs_de, flag))

       strongs_derivations=entry.findall('./strongs_derivation')
       if strongs_derivations is not None:
          if   len(strongs_derivations) == 0:
               pass
          elif len(strongs_derivations) > 1:
               raise Exception('strongs_nr: {:d}, len(strongs_derivations) = {:d}'.format(strongs_nr, len(strongs_derivations)))
#q  TODO else:
#q  TODO      for strongsref in strongs_derivations[0].findall("./strongsref[@language='GREEK']"):
#q  TODO          try:
#q  TODO            cur.execute('insert into strongs_see(nr_1, nr_2) values (?, ?)', ('G' + str(strongs_nr).zfill(4), 'G' + strongsref.attrib['strongs'].zfill(4) ))
#q  TODO          except sqlite3.IntegrityError as e:
#q  TODO            print('* Could not insert ' + str(e))

#_}

def load_roots(): #_{
    f_root = open('data/root', 'r', encoding='utf-8')
    line = f_root.readline()
    while line:

#         try:
          (nr, root) =(re.findall('(.....):(.....)', line))[0]
#         print (re.findall('(.....):(.....)', line))
#         except:
#            print(line)

          try:
            cur.execute('insert into strongs_root values (?, ?)', (nr, root))
          except sqlite3.IntegrityError as e:
            print('Could not insert into strongs_root: {:s} {:s}'.format(nr, root))

          line = f_root.readline()
#_}

def load_see_also(): #_{
    f_root = open('data/see-also', 'r', encoding='utf-8')
    line = f_root.readline()
    while line:

          (desc, entries) =(re.findall('([^:]+): *(.*)', line))[0]

          cur.execute('insert into strongs_see (description) values (?)', (desc, ))
          id_see_also = cur.lastrowid

          for nr_sa_entry in re.findall(r'(\w+) *', entries):
              cur.execute('insert into strongs_see_entry values (?, ?)', (id_see_also, nr_sa_entry))


          line = f_root.readline()
#_}

def load_synonyms(): #_{
    f_root = open('data/synonyms', 'r', encoding='utf-8')
    line = f_root.readline()
    id_syn = 0
    while line:
          id_syn+=1

          try:
            (entries, short, desc)=(re.findall('([^:]+): *([^-]*) *- *(.*) *$', line))[0]
          except:
            print("id_syn = " + str(id_syn))
            raise

          cur.execute('insert into strongs_syn (short, description) values (?, ?)', (short, desc))
          id_syn = cur.lastrowid

          for nr in re.findall(r'(\w+) *', entries):
              cur.execute('insert into strongs_syn_entry values (?, ?)', (id_syn, nr))


          line = f_root.readline()
#_}

# TQ84's entries:
#
#
#  select count(*), nr, nr_greek from strongs_greek_see group by nr, nr_greek having count(*) > 1;
#
# cur.execute('delete from strongs_greek_see where rowid in (select max(rowid) from strongs_greek_see group by nr, nr_greek having count(*) > 1)')

load_hebrew()

# update_strongs()
noun_adj_verb()

load_roots()
load_see_also()
load_synonyms()

cur.execute('commit')
