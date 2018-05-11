#!/usr/bin/python

import re

root_f     = open('data/root'        , 'w')
see_also_f = open('data/see-also.tmp', 'w')
compare_f  = open('data/compare.tmp' , 'w')

def do_lang(lang, letter):
    f_strong = open('strongs-numbers/{:s}-en.@'.format(lang))

    line = f_strong.readline()
    while line:

          m = re.search('(^|[HA] @) *(\d+) *@', line)

          if m:
             strongs_nr = letter + m[2].zfill(4)

          else:
             m = re.search('See also: *(.*)', line)
             if m:
                ar = [strongs_nr]
                for (L, nr) in re.findall('(.)(\d+) *(?:,|$)', m[1]):
                    nr = L + nr.zfill(4)
                    ar.append(nr)

                ar = sorted(ar)
                see_also_f.write(' '.join(ar))
                see_also_f.write('\n')

             m = re.search('Compare: *(.*)', line)
             if m:
                ar = [strongs_nr]
                for (L, nr) in re.findall('(.)(\d+) *(?:,|$)', m[1]):
                    nr = L + nr.zfill(4)
                    ar.append(nr)

                ar = sorted(ar)
                compare_f.write(' '.join(ar))
                compare_f.write('\n')




          line = f_strong.readline()


do_lang('greek' , 'G')
do_lang('hebrew', 'H')
