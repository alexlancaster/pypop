#! /usr/bin/env python

import sys, os, string
from Haplo import HaploArlequin

def outputHaploFile(inputFilename, arpFilename):

    haploParse = HaploArlequin(idCol = 1,
                               arpFilename = arpFilename,
                               prefixCols = 2,
                               suffixCols = 1,
                               windowSize = 3,
                               debug=1)

    data = open(inputFilename, 'r').readlines()

    haploParse.outputArlequin(data)
    haploParse.runArlequin()

    haplotypes = haploParse.genHaplotypes()

    f = open(arpFilename + ".haplo", 'w')
    for window in haplotypes:
        freqs, popName, sampleCount, start, stop = window
        print "Haplotype frequencies for %s population" % popName
        print "Num of samples = %s" % sampleCount
        print "Window start = %s, stop = %s" % (start, stop)
        print
        for haplotype in freqs.keys():
            print haplotype, freqs[haplotype]
            f.write("%s %s %s" % (haplotype, freqs[haplotype], os.linesep))
        print
    f.close()

casesFilename = sys.argv[1]
casesArpFilename = string.split(os.path.basename(casesFilename), '.')[0] + ".arp"
controlFilename = sys.argv[2]
controlArpFilename = string.split(os.path.basename(controlFilename), '.')[0] + ".arp"

outputHaploFile(casesFilename,  casesArpFilename)
outputHaploFile(controlFilename, controlArpFilename)

os.system("contingency.awk -c %s %s > contingency.out" \
          % (casesArpFilename + ".haplo", controlArpFilename + ".haplo"))
