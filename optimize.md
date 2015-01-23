##Starting Trimmed bless and ABySS with trimmed transcriptome but no normalization with khmer  
Running on 20 threads 
	

Moving everything to new folder (/mnt/data3/lah/abyss/trimmed.bless.error.corrected/):

1. cp /mnt/data3/lah/abyss/adult.trinity.fasta trimmed.bless.error.corrected/
2. cp /mnt/data3/lah/abyss/larva.trinity.fasta trimmed.bless.error.corrected/
3. cp /mnt/data3/lah/bless/v0p17/harm.corrected.1.corrected.fastq /mnt/data3/lah/abyss/trimmed.bless.error.corrected/
4. cp /mnt/data3/lah/bless/v0p17/harm.corrected.2.corrected.fastq /mnt/data3/lah/abyss/trimmed.bless.error.corrected/

 Have to interleave trimmed bless output files so I can split them:

5. nohup interleave-reads.py harm.corrected.1.corrected.fastq harm.corrected.2.corrected.fastq -o trimmed.bless.no.norm.interleaved.fq &
	
Have to break corrected.fastq files into 20 so mpi is working to the best of it's ability:

6. General code: split --lines=24000000 --additional-suffix .fastq normalized.fq

	To split into 24 files I used 16800000
	 
				24000000 = 27
				30000000 = 22
				38000000 = 17
				36000000 = 18

Run cd-hit on the trimmed, bless, khmer normalized transcriptomes

7. cd-hit-est -M 5000 -T 23 -c .97 -i adult.larva.fasta -o adult.larva.cdhit.fasta

Running ABySS

8. nano abyss.no.norm.sh


	
		for k in 91 101 111 121; do
     			mkdir k$k;
     			abyss-pe -C k$k np=18 k=$k name=k$k n=5 long=adult.larva.cdhit.fasta\
    	 		in='../x*.fastq';
    	 		done	
		
###### NOTE: RESULTS WERE BETTER THEN THE TRIMMED DATA WITH NORMALIZATION BY AN N50 OF ABOUT 1000


	
##Re-running *genome* bless with -notrim flag 


mkdir nontrimmed.genome.bless

DIR: /mnt/data3/lah/bless/nontrimmed.genome.bless

1. nohup bless -read1 ../harm1.fq -read2 ../harm2.fq -prefix no.trimmed -kmerlength 25 -notrim -verify &

##Re-running *larva* bless with -notrim flag 							
#####NOTE: Bless needs fq files not fq.gz

DIR: /mnt/data3/lah/bless/nontrimmed.larva.bless

1. gunzip harmonia_larva.R1.fastq.gz
2. gunzip harmonia_larva.R2.fastq.gz
3. nohup bless -read1 harmonia_larva.R1.fastq -read2 harmonia_larva.R2.fastq -prefix no.trimmed.larva -kmerlength 25 -notrim -verify &

## Re-running *adult* bless with -notrim flag 
DIR: /mnt/data3/lah/bless/nontrimmed.adult.bless

1. gunzip harmonia_adult.R1.fastq.gz
2. gunzip harmonia_adult.R2.fastq.gz
3. nohup bless -read1 harmonia_adult.R1.fastq -read2 harmonia_adult.R2.fastq -prefix no.trimmed.adult -kmerlength 25 -notrim -verify &

##Running *adult* Trinity with bless-notrim, but no khmer 
DIR: /mnt/data3/lah/bless/nontrimmed.adult.bless/trinity.with.no.norm

1. nohup Trinity --seqType fq --JM 50G --trimmomatic --left ../no.trimmed.adult.1.corrected.fastq --right ../no.trimmed.adult.2.corrected.fastq --CPU 8 --output adult.notrim.bless.nonorm.trinity.fasta --quality_trimming_params "ILLUMINACLIP:/opt/trinity/trinity-plugins/Trimmomatic-0.30/adapters/TruSeq3-PE.fa:2:40:15 LEADING:2 TRAILING:2 MINLEN:25" &
							
## Re-running *adult* khmer with bless -notrim data 
DIR: /mnt/data3/lah/bless/nontrimmed.adult.bless/khmer

1. nohup interleave-reads.py -o nontrimmed.adult.interleaved.txn.fq ../no.trimmed.adult.1.corrected.fastq ../no.trimmed.adult.2.corrected.fastq &
2. nohup normalize-by-median.py -p -x 15e8 -k 25 -C 50 --out nontrimmed.bless.adult.fq nontrimmed.adult.interleaved.txn.fq &

		kept 22333810 of 116001642 or 19%
		
		


		
##Running *larva* Trinity with bless-notrim, but no khmer 
DIR: /mnt/data3/lah/bless/nontrimmed.larva.bless

1. nohup Trinity --seqType fq --JM 50G --trimmomatic --left no.trimmed.larva.1.corrected.fastq --right no.trimmed.larva.2.corrected.fastq --CPU 8 --output 	 larva.notrim.bless.nonorm.trinity.fasta --quality_trimming_params "ILLUMINACLIP:/opt/trinity/trinity-plugins/Trimmomatic-0.30/adapters/TruSeq3-PE.fa:2:40:15 LEADING:2 TRAILING:2 MINLEN:25" &

##Re-running *larva* khmer with bless --notrim data
DIR: /mnt/data3/lah/bless/nontrimmed.larva.bless/khmer

1. nohup interleave-reads.py -o nontrimmed.larva.interleaved.txn.fq ../no.trimmed.larva.1.corrected.fastq ../no.trimmed.larva.2.corrected.fastq &	
2. nohup normalize-by-median.py -p -x 15e8 -k 25 -C 50 --out nontrimmed.bless.larva.fq nontrimmed.larva.interleaved.txn.fq &
		
		kept 18509780 of 134977416 or 13%


## Running Transdecoder on trinity output of bless -notrim no norm transcriptomes##
	Transdecoder finds coding regions within transcripts (used notrim trinity outputs)
DIR:/mnt/data3/lah/transdecoder/notrim.nonorm.transdecoder

1. mkdir transdecoder/notrim.nonorm.transdecoder
2. **FROM** /mnt/data3/lah/bless/nontrimmed.adult.bless/trinity.with.no.norm/adult.notrim.bless.nonorm.trinity.fasta$ **TO** /mnt/data3/lah/transdecoder/notrim.nonorm.transdecoder
	cp adult.notrim.bless.nonorm.trinity.fasta /mnt/data3/lah/transdecoder/notrim.nonorm.transdecoder		
3. **FROM** /mnt/data3/lah/bless/nontrimmed.larva.bless/larva.notrim.bless.nonorm.trinity.fasta$ **TO** /mnt/data3/lah/transdecoder/notrim.nonorm.transdecoder
	cp larva.notrim.bless.nonorm.trinity.fasta /mnt/data3/lah/transdecoder/notrim.nonorm.transdecoder
4. **Cat adult and larva trinity outputs**
 
	nohup cat adult.notrim.bless.nonorm.trinity.fasta larva.notrim.bless.nonorm.trinity.fasta &
5. **Rename nohup.out**
	
	mv nohup.out adult.larva.notrim.bless.nonorm.trinity.fasta
6. **Run abyss-fac to get # contigs before transdecoder**

	abyss-fac adult.larva.notrim.bless.nonorm.trinity.fasta
	
		**1st attempt with broken butterfly** OUTPUT:n=200593 n50=1082
		GOOD OUPUT: n=150862 n50=2281
7. **Run Transdecoder**

	nohup TransDecoder -S --CPU 20 -t adult.larva.notrim.bless.nonorm.trinity.fasta &
	
		S = strand-specific
8. **Evaluate TransDecoder output**

	abyss-fac adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.pep 
	
		**1st attempt with broken butterfly** OUTPUT: n=35410 N50=749
			OUTPUT: n=24871 N50=625

	abyss-fac adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.cds
	 
		**1st attempt with broken butterfly** OUTPUT: n=3415 N50=951
			OUTPUT: n=24878 N50=1674
			
9. **Find number of complete transcripts**

	grep -c complete adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.pep 
	
		**1st attempt with broken butterfly** 6200
		**2nd attempt with correct butterfly = 14324
		
##Running bwa to map raw reads to *adult* Transdecoder output##
	Used Bwa to test how many reads mapped back
DIR: /mnt/data3/lah/bwa

1. mkdir bwa

2. **make a bwa index of cds from transdecoder**
 
	nohup bwa index -p transdecoder /mnt/data3/lah/transdecoder/adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.cds & 
3. **run bwa with adult raw reads**
	
	bwa mem -t 20 transdecoder harmonia_adult.R1.fastq harmonia_adult.R2.fastq | samtools view -@6 -Sub - > adult.trandecoder.bam 	
4. **Run express on transdecoder output.cds** 

		express is run to quantify the abundances of a set of target sequences from subsequences
	
	nohup express --rf-stranded -o adult.transcoder.express -p 10 \ /mnt/data3/lah/transdecoder/adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.cds \ adult.trandecoder.bam &
	
5. **Grab rows from express output with tmp >1**

	awk '1>$15{next}1' results.xprs > adult_greater_than_1.txt

6. **Count number with tmp >1**
	
	WD: /mnt/data3/lah/bwa/adult.transcoder.express
	
	wc -l adult_greater_than_1.txt
		
		16874
	

## Running bwa to map raw reads to *larva* transdecoder output ####
1. **Use bwa index made in last step**
2. **run bwa with larva raw reads**
	
	 bwa mem -t 20 transdecoder harmonia_larva.R1.fastq harmonia_larva.R2.fastq | samtools view -@6 -Sub - > larva.trandecoder.bam
3. **Run express of transdecoder output.cds**
	
	nohup express --rf-stranded -o larva.transcoder.express -p 10 \ /mnt/data3/lah/transdecoder/adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.cds \ larva.trandecoder.bam &

4. **Grab rows from express output with tmp > 1**

	awk '1>$15{next}1' results.xprs > larva_greater_than_1.txt
	
5. **Count number with tmp >1**

	WD: /mnt/data3/lah/bwa/larva.transcoder.express
	
	wc -l larva_greater_than_1.txt
		
		14255


##Re-running khmer on bless -trim *genome* data

		Doing this because the N50 was a lot lower when khmer was added -- maybe something was wrong with khmer?
		
WD: /mnt/data3/lah/bless/trimmed.genome.bless/khmer

1. nohup interleave-reads.py -o trimmed.genome.interleaved.fq ../harm.corrected.1.corrected.fastq ../harm.corrected.2.corrected.fastq &
2. nohup normalize-by-median.py -p -x 15e8 -k 25 -C 50 --out trimmed.bless.gemone.fq trimmed.genome.interleaved.fq &

##Re-running abyss with khmer norm bless -trim data

		The transdecoder transcriptome doesn't have khmer normalization, but this should be fine
		
WD: /mnt/data3/lah/abyss/trimmed.norm.bless.error.corrected

1. **Copying everything to working directory**

	*khmer ouput* cp trimmed.genome.interleaved.fq /mnt/data3/lah/abyss/trimmed.norm.bless.error.corrected/
	
	*transdecoder* cp adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.mRNA /mnt/data3/lah/abyss/trimmed.norm.bless.error.corrected/

2. **Splitting khmer files**

	split --lines=30000000 --additional-suffix .fastq trimmed.genome.interleaved.fq
		
		Splits into 22 files

3. **Run ABySS**

	nano abyss.sh
	
		for k in 91 101 111 121; do
     			mkdir k$k;
     			abyss-pe -C k$k np=18 k=$k name=k$k n=5 \ long=adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.mRNA \
    	 		in='../x*.fastq';
    	 		done
4. **Analyze results**

	*91* - did not work?? 
	
		**re-run**
		
			for k in 93; do
                        mkdir k$k;
                        abyss-pe -C k$k np=18 k=$k name=k$k n=5 \ long=adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.mRNA \
                        in='../x*.fastq';
                        done
                        
          N50=4330
          
	*101* - abyss-fac k101-scaffolds.fa
	
		N50=4594 
	*111* - abyss-fac k111-scaffolds.fa 
	
		N50=4631
	*121* - abyss-fac k121-scaffolds.fa
	
		N50=4109


	
##Running khmer on bless -notrim *genome* data
WD: /mnt/data3/lah/bless/nontrimmed.genome.bless/khmer

1. nohup interleave-reads.py -o nontrimmed.genome.interleaved.fq ../no.trimmed.genome.1.corrected.fastq ../no.trimmed.genome.2.corrected.fastq &
2. nohup normalize-by-median.py -p -x 15e8 -k 25 -C 50 --out nontrimmed.bless.gemone.fq nontrimmed.genome.interleaved.fq &

##Running abyss with khmer normalized bless -nontrimmed data

WD: /mnt/data3/lah/abyss/nontrimmed.bless.norm.error.corrected

1. *khmer output* cp nontrimmed.bless.gemone.fq /mnt/data3/lah/abyss/nontrimmed.bless.norm.error.corrected/
2. *transdecoder output* cp adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.mRNA /mnt/data3/lah/abyss/nontrimmed.bless.norm.error.corrected/ 
3. split --lines=24000000 --additional-suffix .fastq nontrimmed.bless.gemone.fq
		
		21 files
4. nano abyss.sh

	for k in 93 101 111 121; do
     			mkdir k$k;
     			abyss-pe -C k$k np=18 k=$k name=k$k n=5 \ long=adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.mRNA \
    	 		in='../x*.fastq';
    	 		done

5. chmod +x abyss.sh
5. **Run abyss** nohup ./abyss.sh &
6. Check N50 using abyss-fac
	
	abyss-fac k101-scaffolds.fa
		
			4048
	
	abyss-fac k111-scaffolds.fa
	
			3981
			
	abyss-fac k121-scaffolds.fa
	
			3531
			
	***These seems really really low.***

7. Rerunning abyss with lower kmer values
8. nano abyss.low.sh

		for k in 51 61 71 81 91; do
     			mkdir k$k;
     			abyss-pe -C k$k np=18 k=$k name=k$k n=5 \ long=adult.larva.notrim.bless.nonorm.trinity.fasta.transdecoder.mRNA \
    	 		in='../x*.fastq';
    	 		done
      			 		
9. chmod +x abyss.low.sh
10. nohup ./abyss.low.sh &
	  	 		
    
    abyss-fac k51-scaffolds.fa
    
    		2586
	abyss-fac k61-scaffolds.fa
			
			2988
			
	abyss-fac k71-scaffolds.fa
	
			3314
			
	abyss-fac k81-scaffolds.fa
	
			3590
			
	abyss-fac k91-scaffolds.fa
	
			3873
			
			
			
							
##Not sure why these n50s are so low, rerunning abyss with nothing except for trimming 
WD: /mnt/data3/lah/abyss/no.ec.no.norm.no.txn

1. mkdir no.ec.no.norm.no.txn
2. cd no.ec.no.norm.no.txn
3. **Interleave Reads**

	nohup interleave-reads.py -o interleaved.genome.fq /mnt/data3/lah/fastq_files_h.axyridis/harm1.fq /mnt/data3/lah/fastq_files_h.axyridis/harm2.fq &
4. 	**Split files**

	split --lines=30000000 --additional-suffix .fastq interleaved.genome.fq	
	
5. **count files**	
 	
	ls -l | wc -l
	
		22 files
		
6. **make .sh file**

	nano abyss.sh
	
		for k in 93 101 111 121; do
     			mkdir k$k;
     			abyss-pe -C k$k np=18 k=$k name=k$k n=5 in='../x*.fastq';
    	 		done
    	 		
    	*not sure why, but when the "in=" line wasn't on same line as abyss-pe, it didn't work 		
7. chmod +x abyss.sh
8. nohup ./abyss.sh &


##Run ABySS on error corrected non-trimmed genome with no khmer or transcriptome added

WD: /mnt/data3/lah/abyss/nontrimmed.bless.no.norm.no.txn

**already had non-trimmed bless genome in: /mnt/data3/lah/bless/nontrimmed.genome.bless**

1. **copy them to wd using cp**
2. **interleave**
3. **split**
4. 