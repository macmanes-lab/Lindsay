# Final projects

- incorporate many different aspects of python
- For Monday....write out a short paragraph about what you want to do
	- input and output 
- Write a pseudocode for what was given to the	
- Judged on quality, comments, does it accomplish code?


# Dictionaries

- help(dict)
- dir(dict)
- **items** - gives us keys and values one at a time
- if you want to assert some kind of order, you can grab the **keys** and sort them and then sort the **values**
- **pop** - things get out of the dictionary randomly, like items, but not ordered


#Popen

		p1 = Popen(["dmesg"], stdout=PIPE)
		p2 = Popen (["grep", "hda"], stdin=p1.stout, stdout=PIPE)
		output = p2.communicate()[0]
		

#Defensive programming
- a form of defensive design intended to ensure continuing function of a piece of software under unforseen circumstances 
	- Finagle's Law of Dynamic Negatives
		- anything that can go wrong, will - at the worst possible moment 
		
1. Secure programming
	 - clear, concise and explicit instructions for user input 
	 - provide example of input in a Usage/help section for the program
	 - check input data integrity
	 - provide demo data template
	 - catch commonsense mistakes
	 - exception handling
	 	- Try/Except					
		
		
				if not currentLetter in DegNucCode.keys():
			    	warn
				else:
			   	 	process    
			 ==================================
			    if not all (x in list(seq) for x in DegNucCode.keys()):
			        print ('Non nucleotide elements detected!)
			        ans = int(input("Enter 0 to skip the offending elements or 1 to exit: "))
			        if ans == 0:
			            continue
			        else:
			            sys.exit(0)    
			            
#appending a list to a list

- Extend unravels a list and puts it as elements

	
#Popen:
- used when wanted to communicate with the shell 

#Blast
- compare bit scores because they are relative to the alignment (the part that is actually aligned with one another)
- larger file is the database 
- makeblastdb -parse_seqids makes index for them
	- this means that you can grab sequences by ID 
	 

#Bowtie-2 

Bowtie 2 is an ultrafast and memory-efficient tool for aligning sequencing reads to long reference sequences. It is particularly good at aligning reads of about 50 up to 100s or 1,000s of characters, and particularly good at aligning to relatively long (e.g. mammalian) genomes

1. Index
		
		Usage: bowtie2-build [options]* <reference_in> <bt2_index_base>
    	reference_in            comma-separated list of files with ref sequences
   		bt2_index_base          write bt2 data to files with this dir/basename

	bowtie2-build reference/lambda_virus.fa lambda_index
	
2. Bowtie 
		
		bowtie2 [options]* -x <bt2-idx> {-1 <m1> -2 <m2> | -U <r>} [-S <sam>]

#blastdbcmd:
- pulls a fasta sequence out of a database if you use -parseseqid when creating the database 

		blastdbcmd -db demoDB -entry "gi|195360728|gb|EU877944.1|" -dbtype nucl -range 10-20	
			            