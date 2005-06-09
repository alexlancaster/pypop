#!/usr/bin/env python
import sys, string, random

def gen_table(n, k):

    notvalid = True
    
    while notvalid:

        gametes_left = 2*n
        alleles_left = k
        alleles = {}

        for allele in range(0, k):
            num_gametes = random.randint(1, gametes_left)
            gametes_left -=  num_gametes

            #print "generate: %d alleles, got %d left" % \
            # (num_gametes, gametes_left)
            alleles[allele] = num_gametes

            if gametes_left == 0:
                break

        # do left over
        if gametes_left > 0:
            alleles[allele] += gametes_left


        total_alleles = len(alleles.keys())
        print "distinct alleles generated: %d, total needed: %d" % (total_alleles, k)
        if (total_alleles == k):
            notvalid = False

    # convert dictionary to list
    li = []

    for i in alleles:
        for j in range(0, alleles[i]):
            li.append(i)
    return li

number = int(sys.argv[1])
n = int(sys.argv[2])
k = int(sys.argv[3])
shuffles = int(sys.argv[4])

if len(sys.argv) > 5:
    fixed_allele_freqs = [int(i) for i in sys.argv[5:]]
    if len(fixed_allele_freqs) != k:
        sys.exit("specified number of alleles must be equal to k (%d)" % k)
    print fixed_allele_freqs
else:
    fixed_allele_freqs = None

if k > 2*n:
    sys.exit("must have at least as many gametes as alleles")

for i in range(0, number):
    if fixed_allele_freqs:
        alleles = []
        k = 0
        for i in fixed_allele_freqs:
            for j in range(0,i):
                alleles.append(k)
            k+=1
    else:
        alleles = gen_table(n, k)
    print alleles

    for shuffle in range(0, shuffles):
        random.shuffle(alleles)

        filename = "simdata-N%d-K%d-%02d-%02d.pop" % (n, k, i, shuffle)
        print filename
        f = open(filename, "w")
        # output .pop file
        print alleles
        f.write("a_1\ta_2\n")
        for line in range(0, len(alleles)/2):
            #print alleles[line*2], alleles[line*2+1]
            f.write("A%d\tA%d\n" % (alleles[line*2]+1, alleles[line*2+1]+1))
        f.close()

