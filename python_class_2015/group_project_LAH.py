#! /usr/bin/python3

import sys
import re

DegNucCodes = {'R' : "AG",  'Y' : "CT",  'M' : "CA",  'K' : "TG",  'W' : "TA",
               'S' : "CG",  'B' : "CTG", 'D' : "ATG", 'H' : "ATC", 'V' : "ACG",
               'N' : "ACGT",'A' : "A" ,  'C' : "C",   'G' : "G",   'T' : "T"}



DegNucNum = {'R' : 2, 'Y' : 2, 'M' : 2, 'K' : 2, 'W' : 2, 'S' : 2, 'B' : 3, 'D' : 3, 'H' : 3, 'V' : 3, 'N' : 4, 'A' : 1, 'G' : 1, 'C' : 1, 'T' : 1}

out = open('lah_out.txt', 'a') #doesn't override file 

dna = sys.argv[1]

dict = {}
n=0


seq_num=1

for i in dna: # this block calculates the number of sequences needed
    seq_num *= DegNucNum[i]


in_list = [dna] #putting the input string into a list to work with
fin_list = [] #we will fill this in at the end

####################This block calculates all possiblities and places them into fin_list#######################
##################### We're using a queue format here (.pop and .insert tell us that)
while in_list:
    counter = 0
    seq = in_list.pop() #Remove the item at the given position in the list, and return it, so is copying the last entry here (seq is = to totalinput sequence) 
    for nuc in seq:
        if nuc.upper() in "ATGC": #if nuc looking at is ATGC we don't have to look at dictionary
            counter += 1 #counter is going to just keep track of the position (index) 
            continue #looping through sequence until we find something that isn't an A,T,G, or C
        for letter in DegNucCodes[nuc]: #using the letter that we are looking at (not an A, T,C, or G)
            temp_list = list(seq) #turing the sequence that we are parsing through into a list
            temp_list[counter] = letter #counter is = to the index of the string that is not an A, T, G, or C
            in_list.insert(0,''.join(temp_list)) #Insert an item at a given position. The first argument is the index of the element before which to insert, so a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x) is equivalent to a.append(x). Join temp list to in list 
        break #want to work on a sigle nucleotide at a time
    if counter == len(seq):
        fin_list.append(seq)     
 
            
#print (fin_list)

#for item in fin_list:
#    out.write("%s\n" % item) #%s = string conversion via str() prior to formatting
 
 
#tm_file = open("lah_out.txt", 'r')
 
 
count = 1 
for poss in fin_list:
	#print(lines)
    a_count = poss.count("A")
    t_count = poss.count("T")
    c_count = poss.count("C")
    g_count = poss.count("G")
    total = a_count + t_count + c_count + g_count 
    gc_content = (((c_count+g_count)/total)*100)
    at_content = (((a_count+t_count)/total)*100)
	#wallace- Tm = 64.9 + 41 * (G + C - 16.4)/(A + T + G + C)
	wallace = (64.9 + 41 * (g_count + c_count - 16.5)/ (a_count + t_count + g_count + c_count))
	marmur = ((4* (gc_content)) + (2*(at_content))
	
	print(wallace)
	
	#    print(gc_content)
#out.write(fin_list, +"\n")



#zip will take as many lists as you want 
#it = zip[fin_list, melting_temp] #zip returns two lists as combined as a tuple, can't index it 

#counter = 0
#for tuple in it: #gives us all of the possible iterations , when it doesn't have anything else it stops 
#    if counter == 4: 
#        print(tuple[0])
#		 break
#	 counter +=1
#list(it)?? 