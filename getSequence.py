#!/usr/bin/env python

# Yingssu Tsai
# April 2003

#	convert .txt file from Anthony Nolan website to file of the format:
#	<locus name>*<allele name>	<allele sequence>
#	the sequence can be amino acid or nucleotide

import sys	# system info
import re		# string handling
import string
import deletedAlleles as replaceAlleles

class getSequence:

  def __init__(self, in_file, out_file, data_type, locus):

    self.inFile = in_file
    self.outFile = out_file

    self.data = data_type.lower()
    self.locus = locus.lower()

#    print self.inFile
#    print self.outFile
#    print self.data
#    print self.locus

    self.amino_acids = {
      "a" : (24, 207),		# exons 2, 3 : 25 - 206
      "b" : (24, 207),		# exons 2, 3 : 25 - 206
      "cw" : (24, 207),		# exons 2, 3 : 25 - 206
      "dqa" : (27, 111),	# exon 2 : 28 - 110
      "dqb" : (36, 127),	# exon 2 : 37 - 126
      "dpa" : (33, 116),	# exon 2 : 34 - 115
      "dpb" : (33, 122),	# exon 2 : 34 - 121
      "dra" : (27, 110),	# exon 2 : 28 - 109
      "drb" : (33, 124)		# exon 2 : 34 - 123
    }

    self.nucleotides = {
      "a" : (73, 620),		# exons 2, 3 : 74 - 619
      "b" : (73, 620),		# exons 2, 3 : 74 - 619
      "cw" : (73, 620),		# exons 2, 3 : 74 - 619
      "dqa" : (82, 332),	# exon 2 : 83 - 331
      "dqb" : (109, 380),	# exon 2 : 110 - 379
      "dpa" : (100, 347),	# exon 2 : 101 - 346
      "dpb" : (100, 365),	# exon 2 : 101 - 364
      "dra" : (82, 329),	# exon 2 : 83 - 328
      "drb" : (100, 371)	# exon 2 : 101 - 370
      }

    # self.sequences = dictionary, allele names as keys, used to store sequences
    self.sequences = {}
    # self.alleles = array of allele names, in entry order in file
    self.alleles = []
    #	array of positions to be deleted from the sequences
    self.remove = []


  def isAmino(self):
    """determines if the inFile contains amino acid sequence
    """
    return self.data == 'a'


  def haveLocus(self):
    """determines if the locus is a valid HLA locus
    """
    if self.amino_acids.has_key(self.locus):
      pass
    else:
      raise StandardError


  def uninterleave(self):
    """to put sequences in one line of file 
    the sequence is broken up into blocks of different codons
    "|" : exon delimiter
    < > : spaces : bewteen nucleotide codons, and between every 10 amino acids
    """
    f = open(self.inFile)

    for line in f.readlines():

      match = re.search(r'[A-Zw0-1]+?\*[0-9]+?\s[A-Z\.\*\-\|\s]+?', line)

      repeat = 0
      a = 0
      
      if match:

        # getting the allele name
        n = match.group(0)
        name = n.strip()

        # getting the partial sequence
        space = len(name)
        s = line[space:]
        s1 = s.strip()

        # find out where there is whitespace or "|" in subseq
        c = 0
        self.remove = []
        for each in s1:
          for space in string.whitespace:
            if each == space or each == '|':
              self.remove.append(c)
          c += 1

        # remove whitespace or "|" in sequence and form a new sequence
        start = 0
        for each in self.remove:
          if start == 0:
            seq = s1[start:each]
          else:
            seq = seq + s1[start:each]
          start = each + 1

        seq = seq + s1[start:]
        
        # store sequence as a string into dictionary to be edited
        if self.sequences.has_key(name):
          new_seq = self.sequences.get(name) + seq
        else:
          new_seq = seq
        self.sequences[name] = new_seq

        # keep track of allele names
        if self.alleles.count(name) == 0:
          self.alleles.append(name)

    f.close()


  def checkLength(self):
    """checks the length of the sequences to make sure they are equal
    """
    against = len(self.sequences.get(self.alleles[0]))

    for each in self.sequences.keys():
      if against != len(self.sequences.get(each)):
        raise StandardError

    self.total_len = against


  def indel(self):
    """an insertion or deletion is indicated by "."
    function used to removed excess "."
    most "." correspond to insertions in the null allele, which is not analyzed
    """
    for allele in self.alleles:
      c = 0
      self.remove = []
      s1 = self.sequences[allele]
      for each in s1:
        if each == '.':
          self.remove.append(c)
        c += 1

      start = 0
      for each in self.remove:
        if start == 0:
          seq = s1[start:each]
        else:
          seq = seq + s1[start:each]
        start = each + 1

      if start != 0:
        seq = seq + s1[start:]
        self.sequences[allele] = seq


  def undash(self):
    """convert dashed files to undashed files
    the primary sequence is the first sequence listed in the file
    <letters> : different than the primary sequence
    "-" : same as primary sequence
    "*" : not typed - sequence in comparison is replaced by "X" or "N"
    "." : insertion - if the primary seq does not have "." but the sequence
    in comparison does, the "." in the sequence in comparison is replaced by
    "X" or "N"
    sequence becomes a list
    """

    count = 0

    while count < self.total_len:
      for each in self.alleles:
        # case of primary sequence, used to complete other sequences
        if each == self.alleles[0]:
          s = self.sequences[each]
          # convert sequence from string to a list
          # list is mutable
          seq_comp = list(s)
          c_comp = seq_comp[count]

        # case of non-primary sequences, need to be completed
        else:
          seq = self.sequences[each]

          s = list(seq)
          c = s[count]

          if c == '-':
            s[count] = c_comp
          elif c == '*' or c == '.' and c_comp != '.':
            if self.isAmino():
              s[count] = 'X'
            else:
              s[count] = 'N'

          # store new sequence
          self.sequences[each] = s

      count += 1


  def whichCodons(self):
    """determines the cuts to be made to the sequence, based on amino acid 
    sequence
    HLA class I - exon 2 and exon 3
    HLA class II - exon 2
    """
    if self.isAmino():
      ends = self.amino_acids.get(self.locus)
      self.start = ends[0]
      self.end = ends[1]
    else:
      ends = self.nucleotides.get(self.locus)
      self.start = ends[0]
      self.end = ends[1]

    print self.start
    print self.end


  def choose(self):
    """to extract the nucleotides or amino acids within exons
    """
    for each in self.sequences.keys():
      seq = self.sequences.get(each)
      s = seq[self.start:self.end]
      self.sequences[each] = s


  def toString(self):
    """self.sequences stores sequences as lists
    used to convert the lists to strings to be printed
    """
    for each in self.sequences.keys():
      count = 0
      for every in self.sequences.get(each):
        if count == 0:
          seq = every
          count = 1
        else:
          seq = seq + every

      self.sequences[each] = seq


  def printSeq(self):
    """prints the keys and items of self.sequences to outFile
    """
    f = open(self.outFile, 'w')

    for each in self.alleles:
      seq = self.sequences[each]
      f.write(each)
      f.write("\t")
      f.write(seq)
      f.write("\n")

    f.close()


# testing:

anExample = getSequence(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

try:
  anExample.haveLocus()
except:
  sys.exit("Locus does not exist")

anExample.uninterleave()

anExample.checkLength()

anExample.undash()

anExample.indel()

anExample.whichCodons()
anExample.choose()

anExample.toString()
anExample.printSeq()
