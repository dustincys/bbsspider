#! coding: utf-8
#!/usr/bin/env python

import xml.etree.ElementTree as ET

def parse(xmlFile, outFilePath):
    doc = ET.parse(xmlFile)
    root = doc.getroot()

    with open(outFilePath, "w") as outFile:
        for elem in root:
            outFile.write("=================================\n")
            for subelem in elem:
                if subelem.text is not None:
                    outFile.write(subelem.text.encode('utf-8'))
                outFile.write("\n\n")
            outFile.write("\n")

def main():
    parse("/home/dustin/temp/houston.xml", "/home/dustin/temp/houston.plain.txt")

if __name__ == '__main__':
    main()

