#! /usr/bin/env python

import sys, os, string, glob, re
from Haplo import HaploArlequin
from Utils import OrderedDict

# global summary table
summaryTable = OrderedDict()

def stripSuffix(filename):
    return string.split(os.path.basename(filename), '.')[0]

def lociListSuffix(lociList):
    suffix = ""
    print lociList, len(lociList)
    for i in lociList:
        print "locus:", i
        extra = "%02d" % i
        print "formatting:", extra
        if suffix == "":
            suffix = extra
        else:
            suffix = suffix + "-" + extra
        print "new suffix:", suffix
    return suffix

def genArpFilename(prefix, lociList):
    return prefix + "-" + lociListSuffix(lociList) + ".haplo"

def genHaplotypes(inputFilename, arpFilename, windowSize, mapOrder, debug):

    haploParse = HaploArlequin(idCol = 1,
                               arpFilename = arpFilename,
                               prefixCols = 2,
                               suffixCols = 0,
                               windowSize = windowSize,
                               mapOrder = mapOrder,
                               debug=debug)
    haploParse.outputArlequin(open(inputFilename, 'r').readlines())
    haploParse.runArlequin()
    haplotypes = haploParse.genHaplotypes()
    return haplotypes

def outputHaploFiles(filename, haplotypes):
    for window in haplotypes:
        freqs, popName, sampleCount, lociList = window
        f = open(genArpFilename(filename, lociList), 'w')
        for haplotype in freqs.keys():
            # print haplotype, freqs[haplotype]
            f.write("%s %s %s" % (haplotype, freqs[haplotype], os.linesep))
        f.close()

def recordSummary(data, popName, lociList):
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
    # generate haplotype locus name
    locus = lociListSuffix(lociList)
    
    if summaryTable.has_key(chrom):
        if summaryTable[chrom].has_key(locus):
            if summaryTable[chrom][locus].has_key(pop):
                print "has pop key"
            else:
                summaryTable[chrom][locus][pop] = datatuple
        else:
            summaryTable[chrom][locus] = OrderedDict([pop, datatuple])
    else:
        summaryTable[chrom] = \
                            OrderedDict([locus, OrderedDict([pop, datatuple])])

    

def printSummary():
    chroms = summaryTable.keys()
    chroms.sort()
    for chrom in chroms:
        print "Chromosome %s" % chrom
        print

        # don't sort() loci, haplotypes are not necessarily in lexical
        # order
        loci = summaryTable[chrom].keys()

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

def genContingency(casesFilename, controlsFilename, ws, mapOrder, debug):

    casesArpFilename = stripSuffix(casesFilename) + ".arp"
    controlsArpFilename = stripSuffix(controlsFilename) + ".arp"

    casesHaplotypes = genHaplotypes(casesFilename,
                                    casesArpFilename,
                                    ws,
                                    mapOrder,
                                    debug)
    controlsHaplotypes = genHaplotypes(controlsFilename,
                                       controlsArpFilename,
                                       ws,
                                       mapOrder,
                                       debug)
    
    outputHaploFiles(casesArpFilename, casesHaplotypes)
    outputHaploFiles(controlsArpFilename, controlsHaplotypes)

    # loop through pairs of case, controls, generating contingency tables
    for window in casesHaplotypes:
        freqs, popName, sampleCount, lociList = window
        contingFilename = popName + "-" + lociListSuffix(lociList) + ".conting"
        print "running contingency: " + contingFilename
        f = open(contingFilename, 'w')
        f.write("Contingency table" + os.linesep)
        f.write("Population: %s" % popName + os.linesep)
        f.write("Loci: %s" % lociListSuffix(lociList) + os.linesep)
        f.write("Number of case samples: %s" % sampleCount + os.linesep)
        f.close()
        os.system("contingency.awk -c %s %s >> %s" \
                  % (genArpFilename(casesArpFilename, lociList), \
                     genArpFilename(controlsArpFilename, lociList),
                     contingFilename))
        recordSummary(open(contingFilename, 'r').readlines(),
                      popName, lociList)

listcases=glob.glob(os.path.expanduser(sys.argv[1]))
listcontrols=glob.glob(os.path.expanduser(sys.argv[2]))
windowsize=int(sys.argv[3])

debug = 0
mapOrder = None
if len(sys.argv) >= 5:
    if sys.argv[4] == '1':
        debug = 1
    if len(sys.argv) == 6:
        print sys.argv[5]
        mapOrder = map(int, string.split(sys.argv[5], ','))
        print mapOrder

if len(listcases) == len(listcontrols):
    for i in range(0, len(listcases)):
        print "generating contingency for (%s, %s)" % \
              (os.path.basename(listcases[i]), os.path.basename(listcontrols[i]))
        genContingency(listcases[i], listcontrols[i], windowsize,
                       mapOrder,debug)
else:
    sys.exit("Error: must be same number of cases and controls!")

printSummary()
