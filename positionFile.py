#!/usr/local/bin/python

#	Yingssu Tsai
#	May 2003

#	convert data in .pop file into another .pop file with amino acids or 
#	nucleotides

#	format of output file:
#	<same as original file>	locus
#	<same as original file>	<locus name>
# populat id 1_1	1_2	....
# <same as original> <same as original> <aa/nucl> <aa/nucl> ....

import sys
import re
import string

class positionFile:

  def __init__(self, popfile1, seqfile, datatype):

    self.inFile = popfile1
    self.dataFile = seqfile

    self.data_type = datatype.lower()

    #	self.loci_used - array used to store loci that need to be translated
    self.loci_used = []

    # self.loci - list of locus names
    self.loci = ["a", "c", "b", "dra", "drb1", "dqa1", "dqb1", "dpa1", "dpb1"]

    # self.ids - array of id names
    self.ids = []

    #	self.data - key : locus_1 or locus_2, store : dictionary : key : ID, store		# : allele name
    # locus : a, c, b, dra, drb1, dqa1, dqb1, dpa1, dpb1
    self.data = {}

    # self.locus_pos - key : locus_1 or locus_2, store : position in line
    self.locus_pos = {
      "a_1" : 2,
      "a_2" : 3,
      "c_1" : 4,
      "c_2" : 5,
      "b_1" : 6,
      "b_2" : 7,
      "dra_1" : 8,
      "dra_2" : 9,
      "drb1_1" : 10,
      "drb1_2" : 11,
      "dqa1_1" : 12,
      "dqa1_2" : 13,
      "dqb1_1" : 14,
      "dqb1_2" : 15,
      "dpa1_1" : 16,
      "dpa1_2" : 17,
      "dpb1_1" : 18,
      "dpb1_2" : 19
      }


  def readFile(self):
    """extracts data from the input file
    format:
    <categories>
    <information for each category>
    populat id  a_1 a_2 c_1 c_2 b_1 b_2 dra_1 dra_2 drb1_1  drb1_2  dqa1_1 \
             dqa1_2  dqb1_1  dqb1_2  dpa1_1  dpa1_2  dpb1_1  dpb1_2
    <data>
    populat = alphabetical and numeric characters
    id = alphabetical and numeric characters
    genotype info = numeric characters
    """

    f = open(self.inFile)

    self.t1 = f.readline()
    self.t2 = f.readline()

    f.readline()

    find_populat = 0
    self.num_indiv = 0

    for line in f.xreadlines():

      #	split the line by whitespace
      line_contents = line.split()

      if find_populat == 0:
        self.pop = line_contents[0]
        find_populat = 1

      self.num_indiv += 1
      indiv_id = line_contents[1]
      self.ids.append(indiv_id)

      for locus in self.locus_pos.keys():
        locus_index = self.locus_pos[locus]
        #	get allele name
        allele = line_contents[locus_index]
        
        if self.data.has_key(locus):
          info = self.data[locus]
        else:
          info = {}
          self.data[locus] = info

        info[indiv_id] = allele
        self.data[locus] = info

    f.close()     


  def whichLoci(self):
    """determines which loci are used for analysis
    stores information in self.loci array
    """
    
    for locus in self.locus_pos.keys():
      info = self.data[locus]
      allele = []
      for each in info.keys():
        allele.append(info[each])
        blank = allele.count('****')
      if blank == self.num_indiv:
        pass
      else:
        cut = locus.index('_')
        loc = locus[0:cut]
        if self.loci_used.count(loc) == 0:
          self.loci_used.append(loc)


  def getFiles(self):
    """function to get the file names of the sequence files and put them in a
    dictionary
    list_names - file of files names in order of
    a, cw, b, dra, drb1, dqa1, dqb1, dpa1, dpb1
    """
    f = open(self.dataFile)

    # self.seq_files - dictionary, key : locus name, store : file names
    self.seq_files = {} 
    
    c = 0
    for each in f.xreadlines():
      file = each.strip()
      self.seq_files[self.loci[c]] = file
      c += 1

    f.close()


  def findSequences(self):
    """obtain sequence from the sequence file as indicated in self.dataFile
    """
    #	self.sequences - key : allele name, store : sequence
    self.sequences = {}
    # self.alleles - array of allele names in the sequence file
    self.alleles = []
      
    f = open(self.seq_files[self.locus])

    for line in f.xreadlines():
      match = re.search(r'[A-Zw0-9]+?\*[0-9]+?\s[A-Z]+?', line)
      if match:
        n = match.group(0)
        n2 = n.strip()
        space = len(n2) - 1
        c = n2.index('*')
        c += 1
        n3 = n2[c:space]
        name = n3.strip()

        s = line[space:]
        seq = s.strip()

        self.alleles.append(name)
        self.sequences[name] = seq

    f.close()
    self.length = len(self.sequences[self.alleles[0]])


  def topLines(self):
    """form the first three lines of the output file
    """
    self.outFile = self.locus + "_" + self.inFile

    t_1 = self.t1.strip()
    t_2 = self.t2.strip()

    self.t1 = t_1
    self.t2 = t_2

    self.top1 = self.t1 + "\t" + "locus" + "\n"
    self.top2 = self.t2 + "\t" + self.locus + "\n"

    t3 = "populat" + "\t" + "id"
    t = 1
    l = self.length + 1
    first = ""
    second = ""
    while t < l:
      first = str(t) + "_1"
      second = str(t) + "_2"
      t3 = t3 + "\t" + first + "\t" + second
      t += 1

    self.top3 = t3 + "\n"


  def writeFile(self):
    """write information to the output file
    """
    f = open(self.outFile, 'w')

    f.write(self.top1)
    f.write(self.top2)
    f.write(self.top3)

    a = 0
    line = ""
    while a < self.num_indiv:
      indiv = self.ids[a]
      line = self.pop + "\t" + indiv

      #	get locus name based on position
      pos1 = self.locus + "_1"
      pos2 = self.locus + "_2"

      info1 = self.data[pos1]
      info2 = self.data[pos2]

      allele1 = info1[indiv]
      allele2 = info2[indiv]

      if not self.sequences.has_key(allele1):
        a1 = self.substitute[allele1]
        allele1 = a1

      if not self.sequences.has_key(allele2):
        a2 = self.substitute[allele2]
        allele2 = a2

      seq1 = self.sequences[allele1]
      seq2 = self.sequences[allele2]

      pos = 0
      while pos < self.length:
        s1 = seq1[pos]
        s2 = seq2[pos]
        line = line + "\t" + s1 + "\t" + s2
        pos += 1

      line = line + "\n"
      
      f.write(line)
      a += 1


  def isDone(self):
    """determines if self.loci_used is empty
    """
    return self.loci_used == []


  def checkAlleles(self):
    """checks the input data to determine if sequence exists for the alleles
    raises StandardError if it does not
    """

    self.substitute = {}

    # add all "*" sequence for "****" allele
    seq = ""
    l = 0
    while l < self.length:
      seq = seq + "*"
      l += 1
    seq = seq + "\n"
    self.sequences["****"] = seq
    
    for pos in self.pos:
      alleles_inFile = self.data[pos]
      for name in self.ids:
        allele = alleles_inFile[name]
        replaced = 0
        if not self.sequences.has_key(allele) and not self.substitute.has_key(allele):
          length = len(allele)
          for each in self.alleles:
            compare = each[0:length]
            if compare == allele:
              self.substitute[allele] = each
              replaced = 1
              break
          if replaced == 0:
            print self.locus
            print allele
            raise StandardError


  def finish_locus(self):
    """used when the transfer is complete for a locus
    to remove the locus name from self.locus_pos
    """
    print self.loci_used
    print self.locus
    self.loci_used.remove(self.locus)


  def getLocus(self):
    """gets the next locus to run the transfer of amino acids
    """
    self.locus = self.loci_used[0]
    self.pos1 = self.locus + '_1'
    self.pos2 = self.locus + '_2'
    self.pos = [self.pos1, self.pos2]




# testing

anExample = positionFile(sys.argv[1], sys.argv[2], sys.argv[3])

anExample.readFile()

anExample.whichLoci()

while not anExample.isDone():

  anExample.getLocus()
  anExample.getFiles()
  anExample.findSequences()
  anExample.checkAlleles()
  anExample.topLines()
  anExample.writeFile()
  anExample.finish_locus()
