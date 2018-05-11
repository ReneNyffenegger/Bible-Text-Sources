#!/usr/bin/python

import re

root_f = open('data/root', 'w')

def do_lang(lang, letter):
    f_strong = open('strongs-numbers/{:s}-en.@'.format(lang))

    line = f_strong.readline()
    while line:

          m = re.search('(^|[HA] @) *(\d+) *@', line)
#         m = re.search('\(^\) *(\d+) *@', line)

          if m:
             strongs_nr = letter + m[2].zfill(4)
#            print(strongs_nr)

          else:
             m = re.search('Root\(s\): *(.*)', line)
             if m:
#               print('{:s}: {:s}'.format(strongs_nr, m[1]))
                for (L, nr) in re.findall('(.)(\d+) *(?:,|$)', m[1]):
                    nr = nr.zfill(4)
#                   print('  {:s} - {:s}'.format(L, nr))
                    root_f.write('{:s}:{:s}{:s}\n'.format(strongs_nr, L, nr))



          line = f_strong.readline()


do_lang('greek' , 'G')
do_lang('hebrew', 'H')
