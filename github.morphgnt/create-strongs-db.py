# from xml.dom import minidom

# dom = minidom.parse('strongs-dictionary-xml/strongsgreek.xml')

import xml.etree.ElementTree as ET

# for entry in dom.entries
#     print(entry)

tree = ET.parse('strongs-dictionary-xml/strongsgreek.xml')
root = tree.getroot()

for entry in root.findall('entries/entry'):

    greek      =     entry.find('./greek')
    if greek is not None:
       strongs_no = int(entry.findtext('./strongs'))
       greek_unicode = greek.attrib['unicode']
       print(str(strongs_no) + ': ' + greek_unicode)

