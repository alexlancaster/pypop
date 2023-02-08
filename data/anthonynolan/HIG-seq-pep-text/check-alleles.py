#!/usr/bin/env python
import sys, glob, re, os
verbose = 0

patt = re.compile("^([0-9a-zA-Z]+)\*([0-9a-zA-Z]+)")

xslFilename = sys.argv[1]
sortedXML = sys.argv[2:]

dict = {}
loci = ['a', 'b', 'c', 'dqa', 'dqb', 'drb', 'dpb', 'dpa']
for locus in loci:
    #print locus
    lines = (open(locus + '_pt.txt', 'r')).readlines()
    
    for line in lines:
        matchobj = re.search(patt, line)
        if matchobj:
            name = matchobj.group(1)
            if name == "Cw":
                name = "C"
            allele = matchobj.group(2)
            # print name, allele
            if dict.has_key(name):
                if allele not in dict[name]:
                    dict[name].append(allele)
            else:
                dict[name] = []
                dict[name].append(allele)


for file in sortedXML:

    if file == ">":
        # found a redirect, ignore
        break

    print "checking:", os.path.basename(file)
    
    stdout = os.popen("xsltproc %s %s" % (xslFilename, file), 'r').readlines()

    for line in stdout:
        locus, unparsed_alleles = line.split(":")
        locus = locus.strip().uppercase()
        if unparsed_alleles == " \n":
            continue

        if verbose:
            print "{%s: " % locus,
            print

        alleles = unparsed_alleles.split()

        for allele in alleles:
            allele = allele.strip()
	    alleleName, alleleCount = allele.split('/')
	    alleleInfo = "%s (%s)" % (alleleName, alleleCount)
	    #print alleleName, alleleCount
            if alleleName in dict[locus]:
                if verbose:
                    print "[", alleleName, "exact match found ]"
            else:
                expandedList = []
                extraList = []
                lcdList = []

                for dbAllele in dict[locus]:
                    if dbAllele[:4] == alleleName:
                        expandedList.append(dbAllele)
                    if alleleName[:4] == dbAllele:
                        extraList.append(dbAllele)
                    if alleleName[:4] == dbAllele[:4]:
                        lcdList.append(dbAllele)
                if expandedList != []:
                    if verbose:
                        print "  [", alleleInfo, "no exact match; expands into:",
                        for li in expandedList:
                            print li, 
                        print "]"
                elif extraList != []:
                    if verbose:
                        print "  [", alleleInfo, "no exact match; zero-padded:",
                        for li in extraList:
                            print li, 
                        print "]"
                elif lcdList != []:
                    if verbose:
                        print "  [", alleleInfo, "no exact match; un-zero-padded expands into:",
                        for li in lcdList:
                            print li, 
                        print "]"
                else:
                    if verbose:
                        print "  [", alleleInfo, "NOT FOUND; no close matches!]" 
                    else:
                        print "  [%s: %s not found ]" % (locus, alleleInfo)
                        
        if verbose:
            print "}"
        
    
#out = open('all.out', 'w')
#for i in dict.keys():
#    out.write("%s:\n" % i)
#    for j in dict[i]:
#        out.write("%s\n" % j)
    
    
