#! /usr/bin/env python

import sys, os, string, glob, re
from Haplo import HaploArlequin

# global summary table
summaryTable = {}

def stripSuffix(filename):
    return string.split(os.path.basename(filename), '.')[0]

def genArpFilename(prefix, start, stop):
    return prefix + "-" + start + "-" + stop + ".haplo"

def genHaplotypes(inputFilename, arpFilename, windowSize, debug):

    haploParse = HaploArlequin(idCol = 1,
                               arpFilename = arpFilename,
                               prefixCols = 2,
                               suffixCols = 0,
                               windowSize = windowSize,
                               debug=debug)
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

def recordSummary(data, popName, start, stop):
    global summaryTable
    pattLabel = re.compile("            Label.*")
    pattSep = re.compile ("[=].*")
    pattTotal = re.compile("          Totals.*")
    startrecording = 0
    mostsigsofar = ""
    
    for line in data:
        if re.search(pattLabel, line):
            startrecording = 1
        elif re.search(pattSep, line):
            startrecording = 0
        elif re.search(pattTotal, line):
            totalsig = (string.split(line)[6])[8:]
        elif startrecording:
            sig = (string.split(line)[6])[8:]
            if len(sig) > len(mostsigsofar):
                mostsigsofar = sig

    if mostsigsofar == '':
        mostsigsofar = '-'
    if totalsig == '':
        totalsig = '-'

    # parse popName into <pop><chrom>-cases 
    pop = popName[:-(len("-cases")+1)]
    chrom = popName[-(len("-cases")+1)]
    
    print pop, chrom, mostsigsofar, totalsig

    datatuple = (totalsig, mostsigsofar)
    locus = ("%02d" % int(start)) + "-" + ("%02d" % int(stop))
    
    if summaryTable.has_key(chrom):
        if summaryTable[chrom].has_key(locus):
            if summaryTable[chrom][locus].has_key(pop):
                print "has pop key"
            else:
                summaryTable[chrom][locus][pop] = datatuple
        else:
            summaryTable[chrom][locus] = {pop: datatuple}
    else:
        summaryTable[chrom] = {locus: {pop: datatuple}}

def printSummary():
    chroms = summaryTable.keys()
    chroms.sort()
    for chrom in chroms:
        print "Chromosome %s" % chrom
        print
        loci = summaryTable[chrom].keys()
        loci.sort()
        # get the list of keys from the first loci
        pops = summaryTable[chrom][loci[0]].keys()
        pops.sort()
        # print the column header
        print "       ",
        for pop in pops:
            print "%9s" % pop,
        print
        for locus in loci:
            print "%7s  " % locus,
            pops = summaryTable[chrom][locus].keys()
            pops.sort()
            for pop in pops:
                totalsig, mostsig = summaryTable[chrom][locus][pop]
                print "%3s %3s  " % (totalsig, mostsig),
            print
        print

def genContingency(casesFilename, controlsFilename, ws, debug):

    casesArpFilename = stripSuffix(casesFilename) + ".arp"
    controlsArpFilename = stripSuffix(controlsFilename) + ".arp"

    casesHaplotypes = genHaplotypes(casesFilename,
                                  casesArpFilename,
                                  ws,
                                  debug)
    controlsHaplotypes = genHaplotypes(controlsFilename,
                                       controlsArpFilename,
                                       ws,
                                       debug)
    
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
        recordSummary(open(contingFilename, 'r').readlines(),
                      popName, start, stop)

listcases=glob.glob(os.path.expanduser(sys.argv[1]))
listcontrols=glob.glob(os.path.expanduser(sys.argv[2]))
windowsize=int(sys.argv[3])

debug = 0
if len(sys.argv) == 5:
    if sys.argv[4] == '1':
        debug = 1

if len(listcases) == len(listcontrols):
    for i in range(0, len(listcases)):
        print "generating contingency for (%s, %s)" % \
              (os.path.basename(listcases[i]), os.path.basename(listcontrols[i]))
        genContingency(listcases[i], listcontrols[i], windowsize, debug)
else:
    sys.exit("Error: must be same number of cases and controls!")

printSummary()
