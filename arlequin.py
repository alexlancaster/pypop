#! /usr/bin/env python

import sys, os, string
from Haplo import HaploArlequin

def stripSuffix(filename):
    return string.split(os.path.basename(filename), '.')[0]

def genArpFilename(prefix, start, stop):
    return prefix + "-" + start + "-" + stop + ".haplo"

def genHaplotypes(inputFilename, arpFilename):

    haploParse = HaploArlequin(idCol = 1,
                               arpFilename = arpFilename,
                               prefixCols = 2,
                               suffixCols = 0,
                               windowSize = 3,
                               debug=1)
    haploParse.outputArlequin(open(inputFilename, 'r').readlines())
    haploParse.runArlequin()
    haplotypes = haploParse.genHaplotypes()
    return haplotypes

def outputHaploFiles(filename, haplotypes):
    for window in haplotypes:
        freqs, popName, sampleCount, start, stop = window
        f = open(genArpFilename(filename, start, stop), 'w')
        for haplotype in freqs.keys():
            # print haplotype, freqs[haplotype]
            f.write("%s %s %s" % (haplotype, freqs[haplotype], os.linesep))
        f.close()

def genContingency(casesFilename, controlsFilename):

    casesArpFilename = stripSuffix(casesFilename) + ".arp"
    controlsArpFilename = stripSuffix(controlsFilename) + ".arp"

    casesHaplotypes = genHaplotypes(casesFilename,  casesArpFilename)
    controlsHaplotypes = genHaplotypes(controlsFilename, controlsArpFilename)
    
    outputHaploFiles(casesArpFilename, casesHaplotypes)
    outputHaploFiles(controlsArpFilename, controlsHaplotypes)

    # loop through pairs of case, controls, generating contingency tables
    for window in casesHaplotypes:
        freqs, popName, sampleCount, start, stop = window
        contingFilename = popName + "-" + start + "-" + stop + ".conting"
        print "running contingency: " + contingFilename
        f = open(contingFilename, 'w')
        f.write("Contingency table" + os.linesep)
        f.write("Population: %s" % popName + os.linesep)
        f.write("Loci: %s - %s" % (start, stop) + os.linesep)
        f.write("Number of case samples: %s" % sampleCount + os.linesep)
        f.close()
        os.system("contingency.awk -c %s %s >> %s" \
                  % (genArpFilename(casesArpFilename, start, stop), \
                     genArpFilename(controlsArpFilename, start, stop),
                     contingFilename))

genContingency(sys.argv[1], sys.argv[2])
