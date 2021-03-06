#! /usr/bin/python3

import sys
import re

DegNucCodes = {'R' : "AG",  'Y' : "CT",  'M' : "CA",  'K' : "TG",  'W' : "TA",
               'S' : "CG",  'B' : "CTG", 'D' : "ATG", 'H' : "ATC", 'V' : "ACG",
               'N' : "ACGT",'A' : "A" ,  'C' : "C",   'G' : "G",   'T' : "T"}



DegNucNum = {'R' : 2, 'Y' : 2, 'M' : 2, 'K' : 2, 'W' : 2, 'S' : 2, 'B' : 3, 'D' : 3, 'H' : 3, 'V' : 3, 'N' : 4, 'A' : 1, 'G' : 1, 'C' : 1, 'T' : 1}

out = open('out_file.txt', 'a')

dna = sys.argv[1]

dict = {}
n=0


seq_num=1

for i in dna: # this block calculates the number of sequences needed
    seq_num *= DegNucNum[i]


in_list = [dna]
fin_list = []

while in_list:
    counter = 0
    seq = in_list.pop() #pop extracts last element of the initial list and assigns it to a variable
    for i in seq:
        if i.upper() in "ATGC": #if I is ATGC we don't have to look at dictionary
            counter += 1
            continue
        for v in DegNucCodes[i]:
            temp_list = list(seq)
            temp_list[counter] = value
            in_list.insert(0,''.join(temp_list))
         break
     if counter == len(seq):
         fin_list.append(seq)          
            