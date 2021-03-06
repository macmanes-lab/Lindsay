#Transcriptome work:
##Bless adult
1. bless -read1 harmonia_adult.R1.fastq -read2 harmonia_adult.R2.fastq -prefix no.trimmed.adult -kmerlength 25

##Bless Larva
1. bless -read1 harmonia_larva.R1.fastq -read2 harmonia_larva.R2.fastq -prefix no.trimmed.larva -kmerlength 25


##Trinity adult

1. Trinity --seqType fq --JM 50G --trimmomatic --left ../no.trimmed.adult.1.corrected.fastq --right no.trimmed.adult.2.corrected.fastq --CPU 12 --output adult.notrim.bless.nonorm.trinity --quality_trimming_params "ILLUMINACLIP:/opt/trinity/trinity-plugins/Trimmomatic-0.30/adapters/TruSeq3-PE.fa:2:40:15 LEADING:2 TRAILING:2 MINLEN:25"

##Trinity larva
1. Trinity --seqType fq --JM 50G --trimmomatic --left ../no.trimmed.larva.1.corrected.fastq --right no.trimmed.larva.2.corrected.fastq --CPU 12 --output larva.notrim.bless.nonorm.trinity --quality_trimming_params "ILLUMINACLIP:/opt/trinity/trinity-plugins/Trimmomatic-0.30/adapters/TruSeq3-PE.fa:2:40:15 LEADING:2 TRAILING:2 MINLEN:25"

##Predicting orfs with TransDecoder

*adult*

1. /share/TransDecoder/TransDecoder.LongOrfs -t adult.notrim.bless.nonorm.trinity.fasta
2. /share/TransDecoder/TransDecoder.Predict -t adult.notrim.bless.nonorm.trinity.fasta	
3. blastp -query longest_orfs.pep  -db uniprot_sprot  -max_target_seqs 1 -outfmt 6 -evalue 1e-5 -num_threads 10 > blastp.outfmt6
4. hmmscan --cpu 8 --domtblout pfam.domtblout Pfam-A.hmm longest_orfs.pep
5. /share/TransDecoder/TransDecoder.Predict -t adult.notrim.bless.nonorm.trinity.fasta --retain_pfam_hits pfam.domtblout --retain_blastp_hits blastp.outfmt6	

*larva*

3. /share/TransDecoder/TransDecoder.LongOrfs -t larva.notrim.bless.nonorm.trinity.fasta
4. /share/TransDecoder/TransDecoder.Predict -t larva.notrim.bless.nonorm.trinity.fasta
5. blastp -query longest_orfs.pep  -db /mnt/data3/lah/transrate/adult/adult.notrim.bless.nonorm.trinity.fasta.transdecoder_dir/uniprot_sprot  -max_target_seqs 1 -outfmt 6 -evalue 1e-5 -num_threads 10 > blastp.outfmt6
6. hmmscan --cpu 8 --domtblout pfam.domtblout Pfam-A.hmm longest_orfs.pep



6. /share/TransDecoder/TransDecoder.Predict -t larva.notrim.bless.nonorm.trinity.fasta --retain_pfam_hits pfam.domtblout --retain_blastp_hits blastp.outfmt6
 
##Combine adult and larva left and adult and larva right bless outputs for transrate merge 
 
1. cat no.trimmed.adult.1.corrected.fastq no.trimmed.larva.1.corrected.fastq > adult.larva.1.corrected.fastq
2. cat no.trimmed.adult.2.corrected.fastq no.trimmed.larva.2.corrected.fastq > adult.larva.2.corrected.fastq

##Transrate w/merge function 
1. transrate --merge-assemblies=merge.fasta --assembly ../adult.notrim.bless.nonorm.trinity.fasta ../larva.notrim.bless.nonorm.trinity.fasta --left adult.larva.1.corrected.fastq --right adult.larva.2.corrected.fastq 
2. mv good.merge.fasta larva.adult.transrate.good.fasta

##Vsearch
1. vsearch --fasta_width 0 --threads 5 --id .99 --cons_truncate   
--cluster_fast ../adult.larva.notrim.bless.nonorm.trinity.fasta --strand both --centroid adult.larva.centroid.trinity.fasta

##Rename vsearch headers for transrate analysis
1. awk '/^>/{print ">" ++i; next}{print}' < adult.larva.centroid.trinity.fasta  > unique_headers_adult.larva.centroid.trinity.fasta

##Transrate on vsearch
1. transrate -a unique_headers_adult.larva.centroid.trinity.fasta -l ../adult.larva.1.corrected.fastq -r ../adult.larva.2.corrected.fastq
2. mv good.merge.fasta good.unique_headers_adult.larva.centroid.trinity.fasta


##BUSCO on both Transrate and Vsearched merged assemblies to assure that vsearch is best

*vsearch*

1. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonoia.transcriptome.vsearch.eukaryota.busco -in good.unique_headers_adult.larva.centroid.trinity.fasta -l eukaryota/

2. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonoia.transcriptome.vsearch.arthropoda.busco -in good.unique_headers_adult.larva.centroid.trinity.fasta -l arthropoda/


*transrate*

1. python3 /share/B
2. USCO_v1.1b1/BUSCO_v1.1b1.py -o harmonia.transcriptome.transrate.eukaryota.busco -in good.merge.fasta -l eukaryota/

2. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonia.transcriptome.transrate.arthropoda.busco -in good.merge.fasta -l arthropoda/

##Pfam on vsearch transcriptome
1. /share/TransDecoder/TransDecoder.LongOrfs -t good.unique_headers_adult.larva.centroid.trinity.fasta 
1. blastp -query longest_orfs.pep -db uniprot  -max_target_seqs 1 -outfmt 6 -evalue 1e-5 -num_threads 10 > blastp.outfmt6
1. hmmscan --cpu 8 --domtblout pfam.domtblout Pfam-A.hmm longest_orfs.pep
2. /share/TransDecoder/TransDecoder.Predict -t good.unique_headers_adult.larva.centroid.trinity.fasta --retain_pfam_hits pfam.domtblout --retain_blastp_hits blastp.outfmt6
3. grep ">" good.unique_headers_adult.larva.centroid.trinity.fasta.transdecoder.mRNA | wc -l

		39582

3. grep "complete" good.unique_headers_adult.larva.centroid.trinity.fasta.transdecoder.mRNA | wc -l

		23241
4. wc -l  blastp.outfmt6 
		
		18766 blastp.outfmt6

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


#Genome work - DNA only:

##PreQC

1. sga preprocess --pe-mode 1 harm1.fastq harm2.fastq > harmonia.fastq
2. sga index -a ropebwt --no-reverse -t 8 harmonia.fastq
3. sga preqc -t 8 harmonia.fastq > harmonia.preqc
4. sga-preqc-report.py harmonia.preqc sga/src/examples/*.preqc



## Bless
1. bless -read1 ../harm1.fq -read2 ../harm2.fq -prefix no.trimmed -kmerlength 25 -notrim -verify

##Interleave/Splitting bless files - need to get file names


1. interleave-reads.py -o nontrimmed.bless.genome.interleaved.fq no.trimmed.genome
2. split --lines=30000000 --additional-suffix .fastq nontrimmed.bless.genome.fq
 
##ABySS

	for k in 91 101 111 121; do
     			mkdir k$k;
     			abyss-pe -C k$k np=18 k=$k name=k$k n=5 
    	 		in='../x*.fastq';
    	 		done
 
##Analyze ABySS files
1. abyss-fac k111-8.fa
2. python3 BUSCO_v1.1b1.py -o abyss_eukaryota -in k111-8.fa	-l eukaryota
3. python3 BUSCO_v1.1b1.py -o abyss_arthropoda -in k111-8.fa	-l arthropoda
    	 		


#Nanopore 
## stats 
1. poretools stats fail/ 
2. poretools stats pass/

##Converting files from fast5 to fastq 

*fail*

3. poretools fastq --min-length 500 fail/ > nanopore2.harmonia.fail.fastq

	
*pass*

1. poretools fastq --min-length 1000 pass/ > nanopore2.harmonia.pass.fastq

	
##concatenating fail/pass and old nanopore data 
1. cat nanopore2.harmonia.fail.fastq nanopore2.harmonia.pass.fastq nanopore.harmonia.fastq > nanopore.all.fastq


##nanocorrect to correct all.fastq file

*convert .fastq to .fa*

4. more nanopore.all.fastq | awk '{if(NR%4==1) {printf(">%s\n",substr($0,2));} else if(NR%4==2) print;}' > nanopore.all.fa		

*run it*

5. make -f nanocorrect-overlap.make INPUT=../nanopore.all.fa NAME=corrected
6. python nanocorrect.py corrected all > corrected.fasta

##SPAdes 1st


1. spades.py -1 harm1.fq -2 harm2.fq --nanopore corrected.fasta -t 8 -m 500 -o scaffolds.fa --careful --only-assembler

##analyze SPAdes results
1. abyss-fac -e 800000000 scaffolds.fasta 
1. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o scaffolds.arthropoda -in scaffolds.fasta -l arthropoda/
2. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o scaffolds.eukaryota -f -in scaffolds.fasta -l /mnt/data3/lah/busco/eukaryota

#Assembly using both nanopore and Illuminia DNA data 

##Nanocorrect on both nanopore run outputs

*1st run*

*convert .fastq to .fasta*

1. more nanopore.harmonia.fastq | awk '{if(NR%4==1) {printf(">%s\n",substr($0,2));} else if(NR%4==2) print;}' > nanopore.harmonia.fasta 

1. make -f nanocorrect-overlap.make INPUT=nanopore.harmonia.fasta NAME=corrected 
2. python nanocorrect.py corrected all > nanocorrect.fasta


*2nd run*

*convert .fastq to .fa*

4. more nanopore2.harmonia.fastq | awk '{if(NR%4==1) {printf(">%s\n",substr($0,2));} else if(NR%4==2) print;}' > nanopore2.harmonia.fa		,*run it*
/.÷
5. make -f nanocorrect-overlap.make INPUT=../nanopore2.harmonia.fa NAME=corrected2
6. python nanocorrect.py corrected2 all > nanocorrect2.fasta

##fasta to fastq
  

1. python /share/ectools/fastaToFastq.py nanocorrect.fasta > nanocorrect.fastq
2. python /share/ectools/fastaToFastq.py nanocorrect2.fasta > nanocorrect2.fastq

##fastaToCA

5. fastqToCA -libraryname nanocorrect -technology pacbio-corrected -reads nanocorrect.fastq > nanocorrect.frg
6. fastqToCA -libraryname nanocorrect -technology pacbio-corrected -reads nanocorrect2.fastq > nanocorrect2.frg	
7. fastqToCA -libraryname superreads -technology sanger -reads superReadSequences.fastq > superReadSequences.frg
		


##MaSuRCA - add config.file.txt
7. /share/MaSuRCA-3.1.0beta/bin/masurca congfig.file.txt
8. ./assemble.sh
9. python /share/ectools/fastaToFastq.py superReadSequences.fasta > superReadSequences.fastq

			 
##WGS 
1. runCA -d wgs_first -p harmonia -s spec_file_2

		merSize=22
		merylThreads = 10
		merylMemory = 32000
		frgCorrBatchSize = 100000
		ovlHashBlockLength = 180000000
		ovlCorrConcurrency = 10
		ovlConcurrency = 10
		ovlHashBits=25
		ovlHashBlockLength=180000000
		ovlThreads = 5
		ovlRefBlockSize = 1000000
		ovlCorrBatchSize = 100000
		ovlStoreMemory = 219362
		mbtConcurrency = 2
		frgCorrThreads = 10
		frgCorrConcurrency = 1
		cnsConcurrency = 10
		batThreads = 10
		batMemory = 250
		superReadSequences.frg
		nanocorrect.frg
		nanocorrect2.frg


##Analysis of harmonia.scf.fasta file
1. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o second_harmonia_wgs_eukaryota -in harmonia.scf.fasta -l eukaryota/
2.  python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o second_harmonia_wgs_arthropoda -in harmonia.scf.fasta -l arthropoda/
3.  abyss-fac -e 800000000 harmonia.scf.fasta	


#Genome improvement w/ RNA reads
##Error correcting RNA reads

*30129*

perl /share/Rcorrector/run_rcorrector.pl -1 ../30129_TAGCTT_BC6PR5ANXX_L008_001.R1.fastq -2 ../30129_TAGCTT_BC6PR5ANXX_L008_001.R2.fastq -t 10

	Processed 38710598 reads
        Corrected 11568621 bases.
        
*40129*

perl /share/Rcorrector/run_rcorrector.pl -1 ../ 40129_GGCTAC_BC6PR5ANXX_L008_001.R1.fastq -2 ../ 0129_GGCTAC_BC6PR5ANXX_L008_001.R2.fastq -t 10
	
	Processed 31894166 reads
        Corrected 9562341 bases.
        
*70129*  

perl /share/Rcorrector/run_rcorrector.pl -1 ../70129_CTTGTA_BC6PR5ANXX_L008_001.R1.fastq ../70129_CTTGTA_BC6PR5ANXX_L008_001.R2.fastq -t 10  
		
	Processed 100133196 reads
        Corrected 28495607 bases.
*80129*

perl /share/Rcorrector/run_rcorrector.pl -1 ../80129_AGTCAA_BC6PR5ANXX_L008_001.R1.fastq -2 ../80129_AGTCAA_BC6PR5ANXX_L008_001.R2.fastq -t 10  
	
	Processed 106141522 reads
        	Corrected 31009879 bases.
##Blat
1. blat -noHead k111-scaffolds.fa adult.larva.centroid.trinity.fasta harmonia.psl

##L_RNA_Scaffolder
1. L_RNA_scaffolder.sh -d /share/L_RNA_scaffolder -i harmonia.psl -j k111-scaffolds.fa

##Analyzing results
1. abyss-fac -e 8000000000 L_RNA_scaffolder.fasta
2. python3 BUSCO_v1.1b1/BUSCO_v1.1b1.py -o -f l_scaffold_eukaryota -in L_RNA_scaffolder.fasta -l BUSCO_v1.1b1/eukaryota/
3. python3 BUSCO_v1.1b1/BUSCO_v1.1b1.py -o l_scaffold_arthropoda -in L_RNA_scaffolder.fasta -l BUSCO_v1.1b1/arthropoda/

##BWA
1. bwa index -p {0}_bwa_index ../L_RNA_scaffolder.fasta

*30129*

3. seqtk mergepe /mnt/data3/lah/adult_transcriptomes/30129_TAGCTT_BC6PR5ANXX_L008_001.R1.fastq /mnt/data3/lah/adult_transcriptomes/30129_TAGCTT_BC6PR5ANXX_L008_001.R2.fastq | skewer -Q 2 -t 10 -x /share/trinityrnaseq/trinity-plugins/Trimmomatic/adapters/TruSeq3-PE-2.fa - -1 | extract-paired-reads.py -p - -s /dev/null - | bwa mem -p -t 10 {0}_bwa_index - | samtools view -T . -bu - | samtools sort -l 0 -O bam -T tmp -@ 15 -m 22G -o 30129_{0}.bam -

*40129*

4. seqtk mergepe /mnt/data3/lah/adult_transcriptomes/40129_GGCTAC_BC6PR5ANXX_L008_001.R1.fastq /mnt/data3/lah/adult_transcriptomes/40129_GGCTAC_BC6PR5ANXX_L008_001.R2.fastq | skewer -Q 2 -t 10 -x /share/trinityrnaseq/trinity-plugins/Trimmomatic/adapters/TruSeq3-PE-2.fa - -1 | extract-paired-reads.py -p - -s /dev/null - | bwa mem -p -t 10 {0}_bwa_index - | samtools view -T . -bu - | samtools sort -l 0 -O bam -T tmp -@ 15 -m 22G -o 40129_{0}.bam -

*70129*

5. seqtk mergepe /mnt/data3/lah/adult_transcriptomes/70129_CTTGTA_BC6PR5ANXX_L008_001.R1.fastq /mnt/data3/lah/adult_transcriptomes/70129_CTTGTA_BC6PR5ANXX_L008_001.R2.fastq | skewer -Q 2 -t 10 -x /share/trinityrnaseq/trinity-plugins/Trimmomatic/adapters/TruSeq3-PE-2.fa - -1 | extract-paired-reads.py -p - -s /dev/null - | bwa mem -p -t 10 {0}_bwa_index - |samtools view -T . -bu - | samtools sort -l 0 -O bam -T tmp -@ 15 -m 22G -o 70129_{0}.bam -

*80129*

6. seqtk mergepe /mnt/data3/lah/adult_transcriptomes/80129_AGTCAA_BC6PR5ANXX_L008_001.R1.fastq /mnt/data3/lah/adult_transcriptomes/80129_AGTCAA_BC6PR5ANXX_L008_001.R2.fastq | skewer -Q 2 -t 10 -x /share/trinityrnaseq/trinity-plugins/Trimmomatic/adapters/TruSeq3-PE-2.fa - -1 | extract-paired-reads.py -p - -s /dev/null - | bwa mem -p -t 10 {0}_bwa_index - | samtools view -T . -bu - | samtools sort -l 0 -O bam -T tmp -@ 15 -m 22G -o 80129_{0}.bam -

##Merge and index all files
1. samtools merge -f all.bam *_{0}.bam
2. samtools index all.bam

##BESST_RNA
1. "python /share/BESST_RNA/src/Main.py 1 -c /mnt/data3/lah/better_genome/bwa/scaffold_3_harmonia/pass1/Scaffolds-pass1.fa -f all.bam -e 3 -T 50000 -k 500 -d 1 -z 1000 -o iter_{0}

##Run BESST_RNA iteratively
1. bwa index -p {0}_bwa_index iter_{1}/pass1/Scaffolds-pass1.fa

##Analyze results- BESST_RNA
1. abyss-fac -e 8000000000 Scaffolds-pass1.fa
2. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o iter1.eukaryota -f -in Scaffolds-pass1.fa -l /mnt/data3/lah/b
usco/eukaryota/
python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o iter1.arthropoda -f -in Scaffolds-pass1.fa -l /mnt/data3/lah/busco/arthropoda/


	
					
