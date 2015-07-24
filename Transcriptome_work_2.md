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
2. nano all_adult_transcripts_1+
3. nano all_larva_transcripts_1+
4. grep -w -A1 -f all_adult_transcripts_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > filtered_kallisto_hits_adult
5. grep -w -A1 -f all_larva_transcripts_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > filtered_kallisto_hits_larva

##blasting all transcripts that have an average kallisto tpm >1

**WD/mnt/data3/lah/transcriptome_work/kallisto/blast**

*all*

1. blastx -db uniprot -query filtered_kallisto_hits -max_target_seqs 1 -outfmt 6 -evalue 1e-10 -num_threads 5 > filtered_kallisto_hits_blast
		
			20779 hits for 34285 contigs


##Panther on the blast results of all transcripts that have an average kallisto tpm >1 
 **Do in excel- filtered_kallisto_greater_than_1.xlsx in Lindsay folder**
*all*

1. Copy column 2 (upiprot headers)	
2. Paste into new column
3. Find sp| and replace with nothing
4. In the next column run =LEFT(F1,FIND("|",F1)-1)
5. Copy this column (only the uniprot ID to new file) paste special, values
6. 
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
4. give file to ncbi blast 
5. blastn 	