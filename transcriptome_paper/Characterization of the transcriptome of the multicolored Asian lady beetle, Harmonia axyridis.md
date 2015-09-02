##Bless adult
1. bless -read1 harmonia_adult.R1.fastq -read2 harmonia_adult.R2.fastq -prefix no.trimmed.adult -kmerlength 25

##Bless Larva
1. bless -read1 harmonia_larva.R1.fastq -read2 harmonia_larva.R2.fastq -prefix no.trimmed.larva -kmerlength 25

##Combine adult and larav left and adult and larva right bless outputs for transrate merge 
 
1. cat no.trimmed.adult.1.corrected.fastq no.trimmed.larva.1.corrected.fastq > adult.larva.1.corrected.fastq
2. cat no.trimmed.adult.2.corrected.fastq no.trimmed.larva.2.corrected.fastq > adult.larva.2.corrected.fastq

##Transrate w/merge function 
1. transrate --merge-assemblies=merge.fasta --assembly ../adult.notrim.bless.nonorm.trinity.fasta ../larva.notrim.bless.nonorm.trinity.fasta --left adult.larva.1.corrected.fastq --right adult.larva.2.corrected.fastq 
2. mv good.merge.fasta larva.adult.transrate.good.fasta

##Trinity larva
1. Trinity --seqType fq --JM 50G --trimmomatic --left ../no.trimmed.larva.1.corrected.fastq --right no.trimmed.larva.2.corrected.fastq --CPU 12 --output larva.notrim.bless.nonorm.trinity --quality_trimming_params "ILLUMINACLIP:/opt/trinity/trinity-plugins/Trimmomatic-0.30/adapters/TruSeq3-PE.fa:2:40:15 LEADING:2 TRAILING:2 MINLEN:25"

##Trinity adult

1. Trinity --seqType fq --JM 50G --trimmomatic --left ../no.trimmed.adult.1.corrected.fastq --right no.trimmed.adult.2.corrected.fastq --CPU 12 --output adult.notrim.bless.nonorm.trinity --quality_trimming_params "ILLUMINACLIP:/opt/trinity/trinity-plugins/Trimmomatic-0.30/adapters/TruSeq3-PE.fa:2:40:15 LEADING:2 TRAILING:2 MINLEN:25"

##Combining adult and larva Trinity files
1. cat adult.notrim.bless.nonorm.trinity.fasta  larva.notrim.bless.nonorm.trinity.fasta > adult.larva.notrim.bless.nonorm.trinity.fasta


##Vsearch
1. vsearch --fasta_width 0 --threads 5 --id .99 --cons_truncate   
--cluster_fast ../adult.larva.notrim.bless.nonorm.trinity.fasta --strand both --centroid adult.larva.centroid.trinity.fasta

##Rename vsearch headers for transrate analysis
1. awk '/^>/{print ">" ++i; next}{print}' < adult.larva.centroid.trinity.fasta  > unique_headers_adult.larva.centroid.trinity.fasta

##Transrate on vsearch
1. transrate -a unique_headers_adult.larva.centroid.trinity.fasta -l ../adult.larva.1.corrected.fastq -r ../adult.larva.2.corrected.fastq
2. mv good.merge.fasta good.unique_headers_adult.larva.centroid.trinity.fasta


##BUSCO on both Transrate and Vsearched merged assemblies to assure that vsearch is best
####Vsearch####
1. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonoia.transcriptome.vsearch.eukaryota.busco -in good.unique_headers_adult.larva.centroid.trinity.fasta -l eukaryota/

2. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonoia.transcriptome.vsearch.arthropoda.busco -in good.unique_headers_adult.larva.centroid.trinity.fasta -l arthropoda/


####Transrate####
1. python3 /share/B
2. USCO_v1.1b1/BUSCO_v1.1b1.py -o harmonia.transcriptome.transrate.eukaryota.busco -in good.merge.fasta -l eukaryota/

2. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonia.transcriptome.transrate.arthropoda.busco -in good.merge.fasta -l arthropoda/


##Kallisto
1. kallisto index -i adult.larva.idx good.unique_headers_adult.larva.centroid.trinity.fasta
2. kallisto quant -i adult.larva.idx -o adult.larva.merged --plaintext adult.larva.1.corrected.fastq adult.larva.2.corrected.fastq 

##Grabbing all transcripts from adult and larva kallisto that have a tpm >1 (filtered out using excel)
1. nano all_adult_transcripts_1+
2. nano all_larva_transcripts_1+
3. grep -w -A1 -f all_adult_transcripts_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > adult_contigs
4. grep -w -A1 -f all_larva_transcripts_1+ ../good.unique_headers_adult.larva.centroid.trinity.fasta > larva_contigs

##blasting all transcripts that have an average kallisto tpm >1
1. makeblastdb -in uniprot_sprot.fasta -out uniprot -dbtype prot

*adult*

2. blastx -db uniprot -query adult_contigs -outfmt 6 -evalue 1e-10 -num_threads 5 > adult_greater_than_0 &
3. Find unique ones: sort -uk1,1 adult_greater_than_0 > unique_adult_greater_than_0


*larva*

1. blastx -db uniprot -query larva_contigs -outfmt 6 -evalue 1e-10 -num_threads 5 > larva_greater_than_0 &	
2. sort -uk1,1 larva_greater_than_0 > unique_larva_greater_than_0
