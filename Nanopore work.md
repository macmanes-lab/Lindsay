#Using nanopore (MinION) information to improve assembly#

##Steps:
1. pbcr
2. LINKS (n50 = 66K)
3. Gap fill - bc they are joined with N's 
4. REAPER to break obvious missassemblies back up

____________________________________________________

##Start
1. Downloaded the file to my computer from: https://unh.app.box.com/nanopore-fastQ
2. Placing files in 

		WD:/mnt/data3/lah/nanopore/

3. scp all.long.harmonia.fastq.gz lah@davinci.unh.edu:/mnt/data3/lah/nanopore/
4. gunzip all.long.harmonia.fastq.gz
5. mv all.long.harmonia.fastq nanopore.harmonia.fastq
6. scp another copy of compressed file just to have

		scp all.long.harmonia.fastq.gz lah@davinci.unh.edu:/mnt/data3/lah/nanopore/


##1. Using PBcR to error correct##

DIR:/mnt/data3/lah/nanopore/pbcr
		
	info about PBcR: http://wgs-assembler.sourceforge.net/wiki/index.php/PBcR 
		

####fastqToCA - use Illumina reads! 

1. moved nontrimmed (in bless) khmer normalized file to pbcr working directory
	
	From: /mnt/data3/lah/bless/nontrimmed.genome.bless/khmer
	
	To: /mnt/data3/lah/nanopore/pbcr
	
		cp nontrimmed.genome.interleaved.fq /mnt/data3/lah/nanopore/pbcr/
		
2. mv nontrimmed.genome.interleaved.fq interleaved.ec.norm.harmonia.genome.fq
3. tmux new -s FQTCA (fastqtoCA)
		
		tmux help: https://gist.github.com/henrik/1967800
	
2. fastqToCA -insertsize 200 30 -libraryname harmonia.illumina -technology illumina -type illumina -reads interleaved.ec.norm.harmonia.genome.fq > harmonia.illumina.frg 
3. tmux new -s pbcr2

3. Command:

		PBcR -s spec.txt -fastq nanopore.harmonia.fastq -length 1000 -partitions 20 -l harmonia.nanopore.pbcr -t 10 -genomeSize 872000000 harmonia.illumina.frg
4. 	Error that blasr and sawriter weren't in my path
5. 	'which both'...in PATH

		PATH=/share/smrtanalysis/install/smrtanalysis_2.3.0.140936/analysis/bin/:$PATH
		
		Error message meant that the smrtanalysis wasn't in my PATH (b/c asked to download)
6. Start run! 
7. going back to tmux 

		tmux at -t pbcr2
		
8. Run died...trying to find tmux config file

		find / -name tmux.conf	2> /dev/null 
		(2 > means send all permission denied stuff to dead space )
		_____________________________________________
		Doesn't like quality scores	 (nanopore goes up to 93)
9. Changing fastq to fasta

	 	fastq-to-fasta.py -o nanopore.harmonia.fasta nanopore.harmonia.fastq
	 	
10. Change from fasta to fastq again	
		
		downloaded java from: http://wgs-assembler.sourceforge.net/wiki/index.php/PBcR
		
		java -jar convertFastaAndQualToFastq.jar nanopore.harmonia.fasta > nanopore.harmonia.altered.fastq

11. Rerun pbcr

				PBcR -s spec.txt -fastq nanopore.harmonia.altered.fastq -length 1000 -partitions 20 -l harmonia.nanopore.pbcr -t 10 -genomeSize 872000000 harmonia.illumina.frg

12. kill run (reads are going to be too long) break up long reads...they can only be 65 kb long				

