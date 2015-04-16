#Using nanopore (MinION) information to improve assembly#



1. Downloaded the file to my computer from: https://unh.app.box.com/nanopore-fastQ
2. Placing files in 

		WD:/mnt/data3/lah/nanopore/

3. scp all.long.harmonia.fastq.gz lah@davinci.unh.edu:/mnt/data3/lah/nanopore/
4. gunzip all.long.harmonia.fastq.gz
5. mv all.long.harmonia.fastq nanopore.harmonia.fastq
6. scp another copy of compressed file just to have

		scp all.long.harmonia.fastq.gz lah@davinci.unh.edu:/mnt/data3/lah/nanopore/


##Using PBcR to error correct##

DIR:/mnt/data3/lah/nanopore/pbcr
		
	info about PBcR: http://wgs-assembler.sourceforge.net/wiki/index.php/PBcR 
		

####fastqToCA - used Illumina reads! 

1. moved nontrimmed (in bless) khmer normalized file to pbcr working directory
	
	From: /mnt/data3/lah/bless/nontrimmed.genome.bless/khmer
	
	To: /mnt/data3/lah/nanopore/pbcr
	
		cp nontrimmed.genome.interleaved.fq /mnt/data3/lah/nanopore/pbcr/
		
2. mv nontrimmed.genome.interleaved.fq interleaved.ec.norm.harmonia.genome.fq
3. tmux new -s FQTCA (fastqtoCA)
		
		tmux help: https://gist.github.com/henrik/1967800
	
2. fastqToCA -insertsize 200 30 -libraryname harmonia.illumina -technology illumina -type illumina -reads interleaved.ec.norm.harmonia.genome.fq > harmonia.illumina.frg


3. PBcR -s spec.txt -fastq nanopore.harmonia.fastq -length 1000 -partitions 20 -l harmonia.nanopore.pbcr -t 10 -genomeSize 872000000 harmonia.illumina.frg