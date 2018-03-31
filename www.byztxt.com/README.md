# Downloads from www.byztxt.com

2018-03-31: Apparentyl, the site is down. It seems as though more recent files can be optained
from https://github.com/byztxt


## BYZTXT:   Byzantine Unparsed Text

The Greek New Testament according to the Byzantine Textform, edited by Maurice
A. Robinson and William G. Pierpont, 2000 edition.

## BYZPRSD:  Byzantine Parsed Text

The Robinson/Pierpont Byzantine Greek New Testament with complete parsing
information for all Greek words. 

The parsed Byzantine 2005 text includes textual variants which correspond to the marginal readings of the printed edition: `| [the main text replaced by the variant text] | [the variant text] |`.


Hence, [030_removeStrongsAndParsing.pl](https://github.com/ReneNyffenegger/Bible-Text-Sources/blob/master/www.byztxt.com/scripts/030_removeStrongsAndParsing.pl) should produce
the same output for `BYZTXT` and `BYZPRSD`, yet it varies a bit (mostly in revelation), with `BYZPRSD` seeming to have better quality.

## SCRIVNER

Scrivener's 1894 Textus Receptus as published by Trinitarian Bible Society

## SCR-ASCII

Text of `SCRIVNER` in *one-verse-one-line format*

Hence, running [010_oneLinePerVerse](https://github.com/ReneNyffenegger/Bible-Text-Sources/blob/master/www.byztxt.com/scripts/010_oneLinePerVerse.pl) on `SCRIVNER` and `SCR-ASCII` produces
exactly the same output.

## SCR-TR:   Scrivener 1894 TR

The Scrivener 1894 Textus Receptus edition, as reprinted by the Trinitarian
Bible Society and (in its original form) by the Bible for Today, Inc. 

After running [010_oneLinePerVerse](https://github.com/ReneNyffenegger/Bible-Text-Sources/blob/master/www.byztxt.com/scripts/010_oneLinePerVerse.pl), `SCR-TR` seems to differ
from `SCRIVNER` and `SCR-ASCII` only in that `SCR-TR` writes `diapantov` as one word while the other two write it as `dia pantov`.


## STV-TR:   Stephens 1550 TR

The Stephens 1550 Textus Receptus edition, as printed in the George Ricker
Berry Interlinear Greek NT volume

## STV-ASCII

Text of `STV-TR` in *one-verse-one-line format*

Running [010_oneLinePerVerse](https://github.com/ReneNyffenegger/Bible-Text-Sources/blob/master/www.byztxt.com/scripts/010_oneLinePerVerse.pl) on `STV-TR` and `STV-ASCII` produces
the same text, but does not use exactly the same verses (around Acts 24:2-3 and II Cor 13:12-14).

## ST-SCR 

Stephens' 1550 Textus Receptus combined with Scrivener's 1894 Textus Receptus

Base of `TR-PRSD`?

## TR-PRSD:  Stephens TR Parsed with Scrivener Variants

The Textus Receptus with complete parsing information for all Greek words; base
text is Stephens 1550, with variants of Scrivener 1894 shown as footnotes
(marked as the second element within piping symbols, e. g., `| EN | EIV |`, in
which `EN` would be the reading of Stephens 1550, while `EIV` would be the reading
of Scrivener 1894).


## WH-N27:   Westcott-Hort Text with NA27 Variants

The Westcott-Hort edition of 1881, with readings of Nestle27/UBS4 shown as
footnotes (marked as the second element within piping symbols, e. g., as 
`| EN | EIV |`, in which `EN` would be the reading of Westcott-Hort, while `EIV` would be
the reading of the Nestle27/UBS4 edition). 

## WH27PRSD

Text of `WH-N27`, pre-formatted with Strong's numbers and parsing data

## WHN27PRS: Westcott-Hort Parsed Text with NA27 Variants

The Westcott-Hort edition of 1881 with complete parsing information for all
Greek words. Readings of Nestle27/UBS4 shown as footnotes, also with complete
parsing information attached (footnote format uses the piping symbol as above). 

## BYZ05CCT: The New Testament in the Original Greek: Byzantine Textform 2005

The modified-betacode ASCII text of The New Testament in the Original Greek:
Byzantine Textform 2005 includes accents, breathing marks, punctuation,
capitalization, Byzantine variant readings and Nestle-Aland variants. 

## BYZ05ASC

The text of The New Testament in the Original
Greek: Byzantine Textform 2005, edited by
Maurice A. Robinson and William G. Pierpont

## BYZ-ASCII

Text of `BYZ05ASC` in *one-verse-one-line format*.

Hence, running [010_oneLinePerVerse](https://github.com/ReneNyffenegger/Bible-Text-Sources/blob/master/www.byztxt.com/scripts/010_oneLinePerVerse.pl) on `BYZ-ASCII` and `BYZ05ASC` produces
exactly the same output.

## BP05FNL

Textof `BYZ05ASC`, pre-formatted with Strong's numbers and parsing data.

After running [030_removeStrongsAndParsing.pl](https://github.com/ReneNyffenegger/Bible-Text-Sources/blob/master/www.byztxt.com/scripts/030_removeStrongsAndParsing.pl),
`BP05FNL` seems to be similar to `BYZ05ASC` and `BYZ-ASCII`, yet it also lists variations.

# Parsing information


## Undeclined forms

      ADV   = ADVerb or adverb and particle combined
      CONJ  = CONJunction or conjunctive particle
      COND  = CONDitional particle or conjunction
      PRT   = PaRTicle, disjunctive particle
      PREP  = PREPosition
      INJ   = INterJection
      ARAM  = ARAMaic transliterated word (indeclinable)
      HEB   = HEBrew transliterated word (indeclinable)
      N-PRI = Indeclinable PRoper Noun
      A-NUI = Indeclinable NUmeral (Adjective)
      N-LI  = Indeclinable Letter (Noun)
      N-OI  = Indeclinable Noun of Other type


## Declined forms

    All follow the order: prefix, case, number, gender

###   Prefixes:

      N-    = Noun
      A-    = Adjective
      R-    = Relative pronoun
      C-    = reCiprocal pronoun
      D-    = Demonstrative pronoun
      T-    = definite arTicle
      K-    = correlative pronoun
      I-    = Interrogative pronoun
      X-    = indefinite pronoun
      Q-    = correlative or interrogative pronoun
      F-    = reFlexive pronoun (person 1,2,3 added)
      S-    = poSsessive pronoun (person 1,2,3 added)
      P-    = Personal pronoun (person 1,2,3 added)
                (Note: 1st and 2nd personal pronouns have no gender)


### Cases (5-case system only):

      -N    = Nominative
      -V    = Vocative
      -G    = Genitive
      -D    = Dative
      -A    = Accusative


###  Number:                       Gender:

      S     = Singular              M     = Masculine
      P     = Plural                F     = Feminine
                                    N     = Neuter

###  Suffixes:

      -S    = Superlative (used primarily with adjectives and some adverbs)
      -C    = Comparative (used primarily with adjectives and some adverbs)
      -ABB  = ABBreviated form (used only with the number 666)
      -I    = Interrogative
      -N    = Negative (used with some particles, adverbs, adjectives,
                 and conjunctions)
      -K    = "Kai" (CONJ), second person personal pronoun "su", or neuter
                 definite article "to" merged by crasis with a second word;
                 declension is that of the second word.
      -ATT  = ATTic Greek form

# Variants

    | [the main text replaced by the variant text] | [the variant text] |
