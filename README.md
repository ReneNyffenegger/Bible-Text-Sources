# Text Sources for the Bible

## Directory structure


     ├── github.byztxt
     │   ├── create-db.py                       creates BP5.db
     │   ├── BP5.db                             created create-db.py
     │   ├── sql                                shell script: opens BP5.db
     │   ├── v                                  shell script: queries vers
     │   ├── byzantine-majority-text
     │   │   ├── parsed
     │   │   │   ├── {1CO,2CO,…}.BP5
     │   │   ├── textonly-beta-code
     │   │   │   ├── *.CCT
     │   │   └── textonly-online-bible
     │   │       ├── *.ASC
     │   ├── robinson-documentation
     │   └── www
     │       └── handler.php                    handler for https://renenyffenegger.ch/Biblisches/Grundtext/Datenbank
     ├── github.openscriptures
     ├── lxx
     │   └── create-lxx-db.py
     ├── strongs     
     │   ├── create-strongs-db.py               Creates strongs.db (from github.morphgnt/strongs-dictionary-xml/strongsgreek.xml and …)
     │   ├── data
     │   │   ├── synonyms
     │   │   └── …
     │   ├── strongs.db                         created by create-strongs-db.py
     │   ├── github.morphgnt                    Clones (submodules) from https://github.com/morphgnt
     │   │   ├── README.md
     │   │   └── strongs-dictionary-xml
     │   │       └── strongsgreek.xml
     │   └── strongs-numbers                    Clone (submodule) from https://github.com/ReneNyffenegger/strong-numbers
     │       ├── greek-en.@                     Strong's concordance of greek words
     │       ├── greek-de.@                     Google translation of greek-en.@
     │       ├── github.bibel                   Directory for clones from https://github.com/bibel
     │       │   └── strong                     https://github.com/bibel/strong  / Übersetzung von Strong's Nummern ins Deutsche durch Gerhard Kautz
     │       └── Gerhard-Kautz                  Working directory for Gerhard Kautz' translation
     │           ├── extract.py                 Creates translation-de.txt from ../github-bibel/strong/dict/G*.html
     │           └── translation-de.txt         Extracted with extract.py
     ├── www                                    Obsolete, should probably be deleted eventually
     └── www.byztxt.com                         Obsolete, kept for historical reasons (content from www.byztxt.com)
         ├── downloaded
         │   ├── BP05FNL/                       *.BP5 files
         │   ├── BYZ05ASC/                      *.ASC files
         │   ├── BYZ05CCT/                      *.CCT files
         │   ├── BYZ-ASCII/                     *.txt files
         │   ├── BYZPRSD/                       *.BZP files
         │   ├── BYZTXT/                        *.BZ  files
         │   ├── SCR-ASCII/                     *.txt files
         │   ├── SCRIVNER/                      *.SCR files
         │   ├── SCR-TR/                        *.SCR files
         │   ├── ST-SCR/                        *.SS2 files
         │   ├── STV-ASCII/                     *.txt files
         │   ├── STV-TR/                        *.STV files
         │   ├── TR-PRSD/                       *.TRP files
         │   ├── WH27PRSD/                      *.WHP files
         │   ├── WH-N27/                        *.W27 files
         │   └── WHN27PRS/                      *.WHP files
         ├── out/                               created files by scripts
         │   ├── 010_oneLinePerVerse
         │   └── 040_createDB
         └── scripts

## Links

https://github.com/ReneNyffenegger/Bibeluebersetzungen
