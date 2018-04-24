#!/usr/bin/python
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

cur.execute("""create table strongs (
  nr           text    not null primary key, -- G\d\d\d\d or H\d\d\d\d
  word         text    not null,
  lang         text    check (lang in ('G', 'H', 'A')), -- Greek, Hebrew, Aramaeic
  word_de      text,
  strongs_en   text    not null,
  strongs_de   text    not null
)""")

cur.execute("""create table strongs_see (
  nr_1       text not null references strongs,
  nr_2       text not null references strongs,
  unique (nr_1, nr_2)
)""")

cur.execute("""create table strongs_noun_adj_verb (
  noun       text references strongs,
  adj        text references strongs,
  verb       text references strongs
)""")

#_}

strongs_xx      = {}

for xx in ['de', 'en']:
  strongs_xx[xx] = {}
  strongs_xx[xx]['f'   ] = open('strongs-numbers/greek-{:s}.@'.format(xx))
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

      m = re.search('^(\d+) *@', strongs_xx[lang]['line'])
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
    cur.execute('update strongs set word_de = ? where nr = ?', ('adramytisch'       , 'G0098'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('sondern'           , 'G0235'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('Einmischender'     , 'G0244'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('-'                 , 'G0302')) # Modalpartikel welche meist unübersetzbar ist; bezeichnet Handlung
    cur.execute('update strongs set word_de = ? where nr = ?', ('sich verabschieden', 'G0657')) # sich (als Zurückbleibender) verabschieden
    cur.execute('update strongs set word_de = ? where nr = ?', ('Fluchen'           , 'G0685'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('unsichtbar'        , 'G0855')) # ..er ward entschwunden, weg von ihnen...
    cur.execute('update strongs set word_de = ? where nr = ?', ('entfernen'         , 'G0868')) # tr. (im , Impf., Fut. und Aor1): abtrünnig machen)
    cur.execute('update strongs set word_de = ? where nr = ?', ('an der andern Seite vorübergehen', 'G0942')) # an der gegenüberliegenden (Straßenseite) vorübergehen
    cur.execute('update strongs set word_de = ? where nr = ?', ('bezaubern'         , 'G0940')) # jmd. verhexen
    cur.execute('update strongs set word_de = ? where nr = ?', ('denn'              , 'G1063'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('gottergeben'       , 'G1174')) # als Komp. (für Superl.): mehr Götter fürchtend...
    cur.execute('update strongs set word_de = ? where nr = ?', ('-'                 , 'G1473')) # ich (mein, mir, mich); betont: i c h (m e i n, m i r, m i c h)
    cur.execute('update strongs set word_de = ? where nr = ?', ('ähneln'            , 'G1503')) # Perfekt mit Präsensbedeutung: ist ähnlich...
    cur.execute('update strongs set word_de = ? where nr = ?', ('in'                , 'G1519')) # örtl.: hinein...in
    cur.execute('update strongs set word_de = ? where nr = ?', ('aus'               , 'G1537')) # aus...(heraus)
    cur.execute('update strongs set word_de = ? where nr = ?', ('dort'              , 'G1563')) # als Antwort auf Frage: Wo?: dort
    cur.execute('update strongs set word_de = ? where nr = ?', ('rum-huren'         , 'G1608')) # Aor.fem.: außergewöhnlich gehurt-Habende
    cur.execute('update strongs set word_de = ? where nr = ?', ('gering'            , 'G1646')) # als Superl., Geringste
    cur.execute('update strongs set word_de = ? where nr = ?', ('vor'               , 'G1715')) # als Adv.: (nach) vorne
    cur.execute('update strongs set word_de = ? where nr = ?', ('in'                , 'G1722')) # örtl.: auf
    cur.execute('update strongs set word_de = ? where nr = ?', ('auf'               , 'G1909')) # örtl.: auf
    cur.execute('update strongs set word_de = ? where nr = ?', ('haben'             , 'G2192')) # Akt. haben
    cur.execute('update strongs set word_de = ? where nr = ?', ('bis'               , 'G2193')) # als Konj. - solange bis...
    cur.execute('update strongs set word_de = ? where nr = ?', ('oder'              , 'G2228')) # trennend: oder
    cur.execute('update strongs set word_de = ? where nr = ?', ('unfähig'           , 'G2316')) # akt. von Personen: unvermögend
    cur.execute('update strongs set word_de = ? where nr = ?', ('damit'             , 'G2443')) # damit...
    cur.execute('update strongs set word_de = ? where nr = ?', ('stellen'           , 'G2476')) # tr.(, Impf., Aor.1 Akt. und Fut.Akt.): stellen
    cur.execute('update strongs set word_de = ? where nr = ?', ('und'               , 'G2532'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('herab'             , 'G2596')) # räuml.: herab
    cur.execute('update strongs set word_de = ? where nr = ?', ('erwarten'          , 'G3195'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('inmitten'          , 'G3326')) # örtl. inmitten
    cur.execute('update strongs set word_de = ? where nr = ?', ('kurzsichtig'       , 'G3467'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('-'                 , 'G3588'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('hinten'            , 'G3694')) # als Antwort auf Frage: Wo?: hinten
    cur.execute('update strongs set word_de = ? where nr = ?', ('damit'             , 'G3704'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('refl. pr.'         , 'G3739')) # welche (-er, -en, -es, usw.)
    cur.execute('update strongs set word_de = ? where nr = ?', ('jeder, der'        , 'G3748')) # verallgemeinernd: jeder, der...
    cur.execute('update strongs set word_de = ? where nr = ?', ('daß'               , 'G3754')) # daß...
    cur.execute('update strongs set word_de = ? where nr = ?', ('nicht'             , 'G3756')) # nein
    cur.execute('update strongs set word_de = ? where nr = ?', ('keineswegs'        , 'G3760')) # durchaus nicht
    cur.execute('update strongs set word_de = ? where nr = ?', ('niemand'           , 'G3762')) # nicht ein (-er, -e, -en, -es, usw.)
    cur.execute('update strongs set word_de = ? where nr = ?', ('-'                 , 'G3801')) # der "Seiende" und der "Er war" und der "Kommende"
    cur.execute('update strongs set word_de = ? where nr = ?', ('zurück'            , 'G3825')) # örtl.: zurück
    cur.execute('update strongs set word_de = ? where nr = ?', ('beistehen'         , 'G3936')) # im Akt. , Ipf., Aor.1, und Fut.): darstellen
    cur.execute('update strongs set word_de = ? where nr = ?', ('alle'              , 'G3956'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('sehr'              , 'G4007')) # im NT immer an ein anderes Wort angehängt um diesem eine positive<br>Betonung zu geben - hervorhebend oder verschärfend: ... wirklich; ... anders;<br>durchaus; eben.
    cur.execute('update strongs set word_de = ? where nr = ?', ('umhergerissen'     , 'G4049')) # Ind.Impf....war ständig hin- und hergerissen
    cur.execute('update strongs set word_de = ? where nr = ?', ('für'               , 'G4314')) # zugunsten von...
    cur.execute('update strongs set word_de = ? where nr = ?', ('Ansehen-Betrachtender', 'G4381')) # der auf Ansehen (Person Rücksicht) Nehmende
    cur.execute('update strongs set word_de = ? where nr = ?', ('Irrtum'            , 'G4106')) # im passiven Sinn: Irrtum
    cur.execute('update strongs set word_de = ? where nr = ?', ('verharren'         , 'G4357')) # weiterhin bleiben bei...
    cur.execute('update strongs set word_de = ? where nr = ?', ('verfault'          , 'G4595')) # intr. Ind.Pf.Akt. im pass. Sinn: verfault
    cur.execute('update strongs set word_de = ? where nr = ?', ('erbarmen'          , 'G4697')) # erbarmen
    cur.execute('update strongs set word_de = ? where nr = ?', ('anwerben'          , 'G4758')) # Aor.: zum Kriegsdienst angeworben Habende
    cur.execute('update strongs set word_de = ? where nr = ?', ('Band'              , 'G4886')) # (zusammenhaltende) Band
    cur.execute('update strongs set word_de = ? where nr = ?', ('sehr'              , 'G4970')) # in Verbindung mit einem Adj. oder einem Zeitwort: sehr ...
    cur.execute('update strongs set word_de = ? where nr = ?', ('Heil'              , 'G4992')) # als Adj. ohne Art., prädikativ: Errettung bringend (für)...
    cur.execute('update strongs set word_de = ? where nr = ?', ('jemand'            , 'G5100')) # irgendeiner, -e, -es
    cur.execute('update strongs set word_de = ? where nr = ?', ('wer'               , 'G5101')) # wer (was, welcher)
    cur.execute('update strongs set word_de = ? where nr = ?', ('sicher'            , 'G5104')) # wird nur in Verbindung mit anderen Partikeln gebraucht: gewiß
    cur.execute('update strongs set word_de = ? where nr = ?', ('von'               , 'G5259')) # von...
    cur.execute('update strongs set word_de = ? where nr = ?', ('Gerücht'           , 'G5435')) # Kunde
    cur.execute('update strongs set word_de = ? where nr = ?', ('Witwe'             , 'G5503'))
    cur.execute('update strongs set word_de = ? where nr = ?', ('anweisen'          , 'G5537')) # (göttliche) Weisung erteilen
    cur.execute('update strongs set word_de = ? where nr = ?', ('Zwerchfell'        , 'G5424')) # Verstand(esregungen)
    cur.execute('update strongs set word_de = ? where nr = ?', ('wie'               , 'G5616')) # vergleichend: gleichsam wie...
#_}

def noun_adj_verb(): #_{
    cur.execute('insert into strongs_noun_adj_verb values (?, ?, ?)', ('G2549', 'G2556', None)) # κακία - κακός
#_}

def see_also(nr_1, nr_2): #_{
    try:
      cur.execute('insert into strongs_see(nr_1, nr_2) values (?, ?)', (nr_1, nr_2))
    except sqlite3.IntegrityError as e:
      print('! {:s} nr_1 = {:s}, nr_2 = {:s}'.format(str(e), nr_1, nr_2))
    try:
      cur.execute('insert into strongs_see(nr_1, nr_2) values (?, ?)', (nr_2, nr_1))
    except sqlite3.IntegrityError as e:
      print('! {:s} nr_1 = {:s}, nr_2 = {:s}'.format(str(e), nr_1, nr_2))

#_}

def load_hebrew(): #_{

    cur_hebr_word  = ''
    next_hebr_word = 'אָב'
    cur_hebr_lang  = ''
    next_hebr_lang = 'A'
    strongs_xx_hebr = {}
#   cur_hebr_nr = 0

#   global strongs_xx_hebr


    def read_strong_hebr(lang, nr_expected): #_{
        nonlocal strongs_xx_hebr
        nonlocal next_hebr_lang
        nonlocal next_hebr_word
        nonlocal cur_hebr_lang
        nonlocal cur_hebr_word
        ret  = strongs_xx_hebr[lang]['line']
    
        if nr_expected != strongs_xx_hebr[lang]['next_strongs_nr']:
            print('! nr_expected: {:d}, next_strongs_en_nr: {:d}'.format(nr_expected, strongs_xx_hebr[lang]['next_strongs_nr']))
    
    
        while True:
          strongs_xx_hebr[lang]['line'] = strongs_xx_hebr[lang]['f'].readline()
    
          if not strongs_xx_hebr[lang]['line']:
             return ret
    
          m = re.search('^(A|H) @ (\d+) @ ([^@]+) @', strongs_xx_hebr[lang]['line'])
          if m:
             strongs_xx_hebr[lang]['next_strongs_nr'] = int(m[2])


             if lang == 'en':
                cur_hebr_lang = next_hebr_lang
                cur_hebr_word = next_hebr_word

                next_hebr_lang = m[1]
                next_hebr_word = m[3]
                

             return ret
          else:
             ret += strongs_xx_hebr[lang]['line']
    #_}

#   def insert_hebrew():
#       cur.execute('insert into strongs(nr, word, lang, strongs_en, strongs_de) values (?, ?, ?, ?, ?)', ('H' + str(cur_strongs_nr).zfill(4), cur_hebr_word, strongs_en, strongs_de))


#      strongs_en = read_strong('en', strongs_nr)
#      strongs_de = read_strong('de', strongs_nr)

    for xx in ['de', 'en']: #_{
       strongs_xx_hebr[xx] = {}
       strongs_xx_hebr[xx]['f'   ] = open('strongs-numbers/hebrew-{:s}.@'.format(xx))
       strongs_xx_hebr[xx]['line'] = strongs_xx_hebr[xx]['f'].readline()
       strongs_xx_hebr[xx]['next_strongs_nr'] = 1
    #_}

    for strongs_nr_hebr in range(1, 8674):
        strongs_en_hebr = read_strong_hebr('en', strongs_nr_hebr)
        strongs_de_hebr = read_strong_hebr('de', strongs_nr_hebr)

        cur.execute('insert into strongs(nr, word, lang, strongs_en, strongs_de) values (?, ?, ?, ?, ?)', ('H' + str(strongs_nr_hebr).zfill(4), cur_hebr_word, cur_hebr_lang, strongs_en_hebr, strongs_de_hebr))



#       if m:
#          hebr_nr = int(m[2])

#          if hebr_nr != cur_hebr_nr +1:
#             print('! hebr_nr: {:d}, cur_hebr_nr: {:d}'.format(hebr_nr, cur_hebr_nr))

#          insert_hebrew()

#          cur_hebr_nr = hebr_nr

#       hebr_l = hebr.readline()

#_}

for entry in root_greek.findall('entries/entry'): #_{

    strongs_de = ''
    strongs_en = ''

    greek = entry.find('./greek')
    if greek is not None:
       strongs_nr = int(entry.findtext('./strongs'))


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

       cur.execute('insert into strongs(nr, word, word_de, strongs_en, strongs_de) values (?, ?, ?, ?, ?)', ('G' + str(strongs_nr).zfill(4), greek_unicode, gerhard_kautz_I, strongs_en, strongs_de))

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
#_}


# TQ84's entries:
#
see_also('G5485', 'G1435') # δῶρον <--> χάρις
see_also('G1722', 'G1519') # ἐν <--> εἰς
see_also('G0894', 'G4088') # ἄψινθος <--> ...  Wermut / Bitterkeit
see_also('G2549', 'G4189') # κακία <-->  πονηρία   ( 1. Kor 5:8 )
see_also('G4105', 'G4107') # πλανάω <-->  πλανήτης
see_also('G5215', 'G5603') # ὕμνος <--> ᾠδή

#
#  select count(*), nr, nr_greek from strongs_greek_see group by nr, nr_greek having count(*) > 1;
#
# cur.execute('delete from strongs_greek_see where rowid in (select max(rowid) from strongs_greek_see group by nr, nr_greek having count(*) > 1)')

load_hebrew()

update_strongs()
noun_adj_verb()

cur.execute('commit')
