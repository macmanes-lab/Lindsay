#Getting more data
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
######11. retransrate good assemblies


##Transdecoder on vsearch and transrate edited merged file
**WD: /mnt/data3/lah/transcriptome_work/transdecoder**

*Step1- longest orfs*

1. /share/TransDecoder/TransDecoder.LongOrfs -S -t good.unique_headers_adult.larva.centroid.trinity.fasta

Output- good.unique_headers_adult.larva.centroid.trinity.fasta.transdecoder_dir/longest_orfs.pep



*Step 2- Homology search- pfam release 28*

1. hmmpress Pfam-A.hmm
2. hmmscan --cpu 8 --domtblout vsearch_merged.pfam.domtblout Pfam-A.hmm longest_orfs.pep

*Step 3 - blastp*
w/ uniprot and longest_orfs -max_target_seqs 1 -outfmt 6 -evalue 1e-10 -num_threads 10 

*Step 4- TransDecoder predict*
/share/TransDecoder/TransDecoder.Predict -t good.unique_headers_adult.larva.centroid.trinity.fasta --retain_long_orfs 300 --retain_pfam_hits vsearch_merged.pfam.domtblout --retain_blastp_hits OUTPUT --cpu 12



##Filtering kallisto reads from adult.larva_adult and adult.larva_larva for TMP average > 1 
**WD/mnt/data3/lah/transcriptome_work/kallisto/blast**

1. find average tpm from kallisto
2. =IF(G3>1, 1,0)
3. Sort by column
4. Grab all of the headers from transcripts that have header >1 
3. nano merged_transcripts_average_kallisto_tmp_1+
4. tmux new -s grep
5. grep -w -A1 -f merged_transcripts_average_kallisto_tmp_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > filtered_kallisto_hits

##Blasting all transcripts from adult and larva kallisto that have a tpm >1

1. Do in excel
2. nano all_adult_transcripts_1+
3. nano all_larva_transcripts_1+
4. grep -w -A1 -f all_adult_transcripts_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > filtered_kallisto_hits_adult
5. grep -w -A1 -f all_larva_transcripts_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > filtered_kallisto_hits_larva

##Transrate on merged files to check that vsearch is in fact the best
1. transrate -a transrate.merged.good.fasta,good.unique_headers_adult.larva.centroid.trinity.fasta -l adult.larva.1.corrected.fastq -r adult.larva.2.corrected.fastq

**Tranrate merged**

	Contig metrics:
	[ INFO] 2015-07-21 10:14:01 : -----------------------------------
	[ INFO] 2015-07-21 10:14:01 : n seqs                       122298
	[ INFO] 2015-07-21 10:14:01 : smallest                        200
	[ INFO] 2015-07-21 10:14:01 : largest                       21577
	[ INFO] 2015-07-21 10:14:01 : n bases                   115369262
	[ INFO] 2015-07-21 10:14:01 : mean len                     943.35
	[ INFO] 2015-07-21 10:14:01 : n under 200                       0
	[ INFO] 2015-07-21 10:14:01 : n over 1k                     33989
	[ INFO] 2015-07-21 10:14:01 : n over 10k                       96
	[ INFO] 2015-07-21 10:14:01 : n with orf                    34938
	[ INFO] 2015-07-21 10:14:01 : mean orf percent               57.5
	[ INFO] 2015-07-21 10:14:01 : n90                             332
	[ INFO] 2015-07-21 10:14:01 : n70                             966
	[ INFO] 2015-07-21 10:14:01 : n50                            1843
	[ INFO] 2015-07-21 10:14:01 : n30                            2935
	[ INFO] 2015-07-21 10:14:01 : n10                            5079
	[ INFO] 2015-07-21 10:14:01 : gc                             0.36
	[ INFO] 2015-07-21 10:14:01 : gc skew                         0.0
	[ INFO] 2015-07-21 10:14:01 : at skew                         0.0
	[ INFO] 2015-07-21 10:14:01 : cpg ratio                      1.65
	[ INFO] 2015-07-21 10:14:01 : bases n                           0
	[ INFO] 2015-07-21 10:14:01 : proportion n                    0.0
	[ INFO] 2015-07-21 10:14:01 : linguistic complexity          0.16