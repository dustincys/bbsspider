#! coding: utf-8
#!/usr/bin/env python

import xml.etree.ElementTree as ET

def parse(xmlFile, outFilePrefix):
    doc = ET.parse(xmlFile)
    root = doc.getroot()

    my_own_order = ['title', 'date', 'url', 'content']
    order = {key: i for i, key in enumerate(my_own_order)}

    for elemidx, elem in enumerate(root):

        outFilePath = "{0}_{1}.txt".format(outFilePrefix, elemidx)
        with open(outFilePath, "w") as outFile:
            elem = sorted(elem, key=lambda item: order[item.tag])

            for subelem in elem:
                if subelem.text is not None:
                    outFile.write(subelem.text.encode('utf-8'))
                    pass
                outFile.write("\n\n")
                pass
        pass

def main():
   import argparse
   parser = argparse.ArgumentParser(description = 'parseargs')

   parser.add_argument('-i', dest='xmlfile', help='xmlfile')
   parser.add_argument('-op', dest='txtfileprefix', help='txtfileprefix')

   args = parser.parse_args()

   parse(args.xmlfile, args.txtfileprefix)

if __name__ == '__main__':
    main()
