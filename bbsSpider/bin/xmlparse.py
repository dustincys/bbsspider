#! coding: utf-8
#!/usr/bin/env python

import xml.etree.ElementTree as ET

def parse(xmlFile, outFilePath):
    doc = ET.parse(xmlFile)
    root = doc.getroot()

    with open(outFilePath, "a") as outFile:
        for elem in root:
            outFile.write("=================================\n")
            for subelem in elem:
                if subelem.text is not None:
                    outFile.write(subelem.text.encode('utf-8'))
                outFile.write("\n\n")
            outFile.write("\n")

def main():
   import argparse
   parser = argparse.ArgumentParser(description = 'parseargs')

   parser.add_argument('-i', dest='xmlfile', help='xmlfile')
   parser.add_argument('-o', dest='txtfile', help='txtfile')

   args = parser.parse_args()

   parse(args.xmlfile, args.txtfile)

if __name__ == '__main__':
    main()

