##Getting more data
####What is unique to these unique transcripts

######1. Kallisto
######2. TMP average > 1
######3. Blast w/ uniprot
######4. Panther w/ these blast results
######5. Put unique IDs and put them into panther
######6. Transdecoder ORF's (% or number) - gives you proteins
	
		w/in transdecoder--The number of transcripts that have a hit to pfam database
		w/in transdecoder-- Pfam 
######8. Dryad- assembled contigs, pfam
######9. make a plot of count vs. TMP from filtered
######10. make plot expression adult vs. expression larva from filtered (potentially interesting)


##Transdecoder on vsearch and transrate edited merged file
**WD: /mnt/data3/lah/transcriptome_work/transdecoder**

**Step 1 Longest Orfs**

Code: /share/TransDecoder/TransDecoder.LongOrfs -S -t transcriptome (vsearch merged transrate editted)

1. /share/TransDecoder/TransDecoder.LongOrfs -S -t good.unique_headers_adult.larva.centroid.trinity.fasta

Output- longest.orfs.pep

**Step 2 Homology search**
hmmscan --cpu 8 --domtblout adult.pfam.domtblout 

##Filtering kallisto reads from adult.larva_adult and adult.larva_larva for TMP average > 1 