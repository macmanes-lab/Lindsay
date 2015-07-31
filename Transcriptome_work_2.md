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


##Counting number of reads loss with bless
1. grep "@HWI" harmonia_adult.R1.fastq | wc -l

		58000821
2. grep "@HWI" harmonia_adult.R2.fastq | wc -l 

		58000821
		
3. more both.fa.read_count

		115999771		

		
##Transdecoder on vsearch and transrate edited merged file
**WD: /mnt/data3/lah/transcriptome_work/transdecoder**

*Step1- longest orfs*

1. /share/TransDecoder/TransDecoder.LongOrfs -S -t good.unique_headers_adult.larva.centroid.trinity.fasta

Output- good.unique_headers_adult.larva.centroid.trinity.fasta.transdecoder_dir/longest_orfs.pep



*Step 2- Homology search- pfam release 28*

1. hmmpress Pfam-A.hmm
2. hmmscan --cpu 8 --domtblout vsearch_merged.pfam.domtblout Pfam-A.hmm longest_orfs.pep

		Internal pipeline statistics summary:
		-------------------------------------
		Query sequence(s):                         1  (99 residues searched)
		Target model(s):                       16230  (2852355 nodes)
		Passed MSV filter:                      1189  (0.0732594); expected 324.6 (0.02)
		Passed bias filter:                      411  (0.0253235); expected 324.6 (0.02)
		Passed Vit filter:                        95  (0.00585336); expected 16.2 (0.001)
		Passed Fwd filter:                        17  (0.00104744); expected 0.2 (1e-05)
		Initial search space (Z):              16230  [actual number of targets]
		Domain search space  (domZ):               0  [number of targets reported over threshold]

3. grep ">" longest_orfs.pep | wc -l

		27320


*Step 3 - blastp*

1. makeblastdb -in uniprot_sprot.fasta -out uniprot -dbtype prot
2. blastp -db uniprot -query longest_orfs.pep -max_target_seqs 1 -outfmt 6 -evalue 1e-10 -num_threads 5 > adult.larva.blastp

*Step 4- TransDecoder predict*

1. /share/TransDecoder/TransDecoder.Predict -t good.unique_headers_adult.larva.centroid.trinity.fasta --retain_long_orfs 300 --retain_pfam_hits vsearch_merged.pfam.domtblout --retain_blastp_hits adult.larva.blastp --cpu 5



##Filtering kallisto reads from adult.larva_adult and adult.larva_larva for TMP average > 1 
**WD/mnt/data3/lah/transcriptome_work/kallisto/blast**

**Excel - filtered_kallisto_greater_than_1.xlsx in Lindsay folder**

1. find average tpm from kallisto
2. =IF(G3>1, 1,0)
3. Sort by column
4. Grab all of the headers from transcripts that have header >1 
3. nano merged_transcripts_average_kallisto_tmp_1+
4. tmux new -s grep
5. grep -w -A1 -f merged_transcripts_average_kallisto_tmp_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > filtered_kallisto_hits


##grabbing all transcripts from adult and larva kallisto that have a tpm >1

1. **Do in excel- filtered_kallisto_greater_than_1.xlsx in Lindsay folder**
2. nano all_adult_transcripts_1+ (32346)
3. nano all_larva_transcripts_1+
4. grep -w -A1 -f all_adult_transcripts_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > filtered_kallisto_hits_adult
5. grep -w -A1 -f all_larva_transcripts_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > filtered_kallisto_hits_larva

##blasting all transcripts that have an average kallisto tpm >1

**WD/mnt/data3/lah/transcriptome_work/kallisto/blast/1st_attempt**

*all*

1. blastx -db uniprot -query filtered_kallisto_hits -max_target_seqs 1 -outfmt 6 -evalue 1e-10 -num_threads 5 > filtered_kallisto_hits_blast
		
			20779 hits for 34285 contigs
2. Grabbing unique ones:
 			
 			 sort -uk1,1 filtered_kallisto_hits_blast > unique_filtered_kallisto_hits_blast
 			 
 			
 			 16420

*adult*

1. blastx -db uniprot -query filtered_kallisto_hits_adult -max_target_seqs 1 -outfmt 6 -evalue 1e-10 -num_threads 5 > filtered_kallisto_hits_blast_adult
2. Grabbing unique ones:

			sort -uk1,1 filtered_kallisto_hits_blast_adult > unique_filtered_kallisto_hits_adult
	
			24560

*larva*

1. blastx -db uniprot -query filtered_kallisto_hits_larva -max_target_seqs 1 -outfmt 6 -evalue 1e-10 -num_threads 5 > filtered_kallisto_hits_blast_larva
2. Grabbing unique ones:

			sort -uk1,1 filtered_kallisto_hits_blast_larva > unique_filtered_kallisto_hits_larva
				
			24560	

##Panther on the blast results of all transcripts that have an average kallisto tpm >1 
 **Do in excel- filtered_kallisto_greater_than_1.xlsx in Lindsay folder**
 
 **/Users/lindsayhavens/Documents/Science/papers I wrote/transcriptome paper/panther results/panther_results**
 
*all*

1. Copy column 2 (upiprot headers)	
2. Paste into new column
3. Find sp| and replace with nothing
4. In the next column run =LEFT(F1,FIND("|",F1)-1)
5. Copy this column (only the uniprot ID to new file) paste special, values
6. pantherGeneList_filtered>1_adult.txt
7. pantherGeneList_filtered>1_combined.txt
8. pantherGeneList_filtered>1_larva.txt

##Transrate on merged files to check that vsearch is in fact the best
1. transrate -a transrate.merged.good.fasta,good.unique_headers_adult.larva.centroid.trinity.fasta -l adult.larva.1.corrected.fastq -r adult.larva.2.corrected.fastq

*vsearch is better, or at least not worse. The original score was highter, there were more reads mapped back initially and the optimal score is a little better.**
		
		Transrate % mapped - 91.6%
		Vsearch % mapped - 93.3
		Transrate score - .292
		Vsearch score - .305 
		Transrate optimal - .310
		Vsearch score - .319
		
		
##Figuring out what the transcripts that are highly expressed in adult or larva but not both are. 	
**Excel ncbi_blast**

1. Sort by tmp column adult or larva
2. Copy transcipt ID 
3. Grab them from merged kallisto file
	A. grep -w -A1 -f ncbi_blast good.unique_headers_adult.larva.centroid.trinity.fasta > ncbi_blast_contigs
	
			NOTE: This didn't work bc it sorts contigs alphabetically. 
4. give file to ncbi blast 
5. blastn

##Double checking kallisto filtered grabbed only important ones b/c in panther everything looks the same  	
**WD: /mnt/data3/lah/transcriptome_work/kallisto/blast/filtered_greater_than_0/adult**
**WD: /mnt/data3/lah/transcriptome_work/kallisto/blast/filtered_greater_than_0/larva**
**Excel: /Users/lindsayhavens/Documents/Science/papers I wrote/transcriptome paper/filtered_kallisto/filtered_kallisto_greater_than_1.xlsx**

1. grep -w -A1 -f adult_greater_than_0.1 good.unique_headers_adult.larva.centroid.trinity.fasta > adult_greater_than_1_contigs_1


2
. grep -w -A1 -f adult_greater_than_0.2 good.unique_headers_adult.larva.centroid.trinity.fasta > adult_greater_than_1_contigs_2
3. grep -w -A1 -f adult_greater_than_0.4 good.unique_hs_adult.larva.centroid.trinity.fasta > adult_greater_than_1_contigs_3
3. grep -w -A1 -f adult_greater_than_0.5 good.unique_headers_adult.larva.centroid.trinity.fasta > adult_greater_than_1_contigs_4
4. etc and then same for larva

##Concatenate contig files into one file and then blastx w/ uniprot data
*adult*

1. cat * > concatenated_contigs_adult
2. blastx -db ../uniprot -query concatenated_contigs_adult -max_target_seqs 1 -outfmt 6 -evalue 1e-10 -num_threads 5 > concatenated_contigs_adult_blast

*larva*

3. cat larva_greater_than_1_contigs_* > concatenated_contigs_larva
4. blastx -db ../uniprot -query concatenated_contigs_larva -max_target_seqs 1 -outfmt 6 -evalue 1e-10 -num_threads 5 > concatenated_contigs_larva_blast


		Something didn't work w/ grep
		
		
##Try grep a different way...with a for loop
**/mnt/data3/lah/transcriptome_work/kallisto/blast/filtered_greater_than_0/adult/transcripts**

1. for i in `cat adult_greater_than_0.1`; do  grep --max-count=1 -A1 -w $i good.unique_headers_adult.larva.centroid.trinity.fasta >> 1.fasta; done &
2. for i in `cat adult_greater_than_0.2`; do  grep --max-count=1 -A1 -w $i good.unique_headers_adult.larva.centroid.trinity.fasta >> 2.fasta; done &
3. for i in `cat adult_greater_than_0.3`; do  grep --max-count=1 -A1 -w $i good.unique_headers_adult.larva.centroid.trinity.fasta >> 3.fasta; done &
4. for i in `cat adult_greater_than_0.4`; do  grep --max-count=1 -A1 -w $i good.unique_headers_adult.larva.centroid.trinity.fasta >> 4.fasta; done &
5. for i in `cat adult_greater_than_0.5`; do  grep --max-count=1 -A1 -w $i good.unique_headers_adult.larva.centroid.trinity.fasta >> 5.fasta; done &	
		
			Same problem as before...only grabbing 1 transcript ID
			
**WD: /mnt/data3/lah/transcriptome_work/kallisto/blast**
 
1. grep -w -A1 -f transcripts_adult good.unique_headers_adult.larva.centroid.trinity.fasta > test1

2. grep -w -A1 -f transcripts_adult good.unique_headers_ad
ult.larva.centroid.trinity.fasta > test1  

##blastx
**WD: /mnt/data3/lah/transcriptome_work/kallisto/blast**

1.  blastx -db uniprot -query adult_contigs -outfmt 6 -evalue 1e-10 -num_threads 5 > adult_greater_than_0 &
2.   blastx -db uniprot -query larva_contigs -outfmt 6 -evalue 1e-10 -num_threads 5 > larva_greater_than_0 &	
	
	