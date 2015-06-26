#Transcriptome work
##Game plan:
#### 1. kallisto 
####2. blast to tribolium
####3. PANTHER (gene ontology)
####4. HMMER3 (conserved protein domains contained in the dataset using Pfam database)
####5. Transdecoder (putative coding sequences)

June 22, 2015
##1. kallisto

		WD: /mnt/data3/lah/transcriptome_work/kallisto
1. make ghost files of transcriptome work 	

	ln -s /mnt/data3/lah/bless/nontrimmed.adult.bless/trinity.with.no.norm/adult.notrim.bless.nonorm.trinity.fasta/adult.notrim.bless.nonorm.trinity.fasta
	
	ln -s /mnt/data3/lah/bless/nontrimmed.larva.bless/larva.notrim.bless.nonorm.trinity.fasta/larva.notrim.bless.nonorm.trinity.fasta
	
2. tmux new -s kallisto
###Adult

3. kallisto index -i adult.idx adult.notrim.bless.nonorm.trinity.fasta
4. kallisto quant -i adult.idx -o adult.output --plaintext no.trimmed.adult.1.corrected.fastq no.trimmed.adult.2.corrected.fastq 
 
###Larva

5. kallisto index -i larva.idx larva.notrim.bless.nonorm.trinity.fasta  
6. kallisto quant -i larva.idx -o larva.output --plaintext no.trimmed.larva.1.corrected.fastq no.trimmed.larva.2.corrected.fastq 

##Blast high abundance contigs with uniprot database

	WD: /mnt/data3/lah/transcriptome_work/kallisto/blast
1. Grep 20 best contigs (based on tpm of abundance.txt)from adult.notrim.bless.nonorm.trinity.fasta file


		Put into adultdb
2. Grep 20 best contigs (based on tpm of abundance.txt)from larva.notrim.bless.nonorm.trinity.fasta file	


		Put into larvadb
3. makeblastdb -in uniprot_sprot.fasta -out uniprot -dbtype prot
4. tmux new -s blast
5. blastx -db uniprot -query adultdb -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 5 > adult_txn_blast
6. blastx -db uniprot -query larvadb -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 5 > larva_txn_blast

		**Nothing super intersting here...just a lot of myosin and cytocrome c sequences

June 25, 2015	
##Blast transcriptomes with tribolium database
		
1. ln -s /mnt/data3/lah/cpg_blast/tribolium.protein.fa
2. tmux at -t blast
3. makeblastdb -in tribolium.protein.fa -out tribolium -dbtype prot
3. blastx -db tribolium -query ../adult.notrim.bless.nonorm.trinity.fasta -outfmt '6 qseqid sacc pident length evalue' -evalue 1e-10 -num_threads 1 > adult_txn_tribolium_blast