#Using nanopore (MinION) information to improve assembly#

## Possible Steps:
1. pbcr
2. LINKS (n50 = 66K)
3. Gap fill - bc they are joined with N's 
4. REAPER to break obvious missassemblies back up


##What I actually did:
1. LSC
2. SPAdes
3. Try wgs
4. 


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

#Pbcr isn't working...trying LSC
http://www.healthcare.uiowa.edu/labs/au/LSC/

WD: /mnt/data3/lah/lsc

1. Error corrector
2. Have to edit run.cfg file


		1. No removing of tails of PacBio reads (I don't have PacBio reads) 
		2. Running it with bowtie2 as aligner for mapping Illuminia to Nanopore
			--default
			--end-to-end -a -f -L 15 --mp 1,1 --np 1 --rdg 0,1 --rfg 0,1 --score-min L,0,-0.12 --no-unal
			*probably a place to change and see what happens
3. Start lsc

		python /share/lsc/runLSC.py run.cfg
		
4. lsc finished at 11 AM (2PM-11AM)	
5. There isn't any information given except percentage of corrected output sequences covered by short reads and quality scores
6. Figure out average % coverage of short reads

		#!/bin/bash

		count=0;
		total=0; 

			for i in $( awk ' BEGIN { FS = "|" } { print $2; }' corrected_LR.fa )
  						 do 
     		total=$(echo $total+$i | bc )
     
   		done
        num=$(grep '>' corrected_LR.fa |wc -l)

		echo "scale=2; $total / $num" | bc		
		
	Average % coverage of short reads when making the long read is .73
	
	
####I think LSC is good...73% average coverage of short reads


		symbolic link
			ln -s /mnt/data3/lah/spades/harm1.fq .
			
#SPAdes
WD: /mnt/data3/lah/nanopore/spades

1. tmux new -s spades

		spades.py -1 harm1.fq -2 harm2.fq --nanopore corrected_LR.fq -t 10 -m 500 -o harmonia.nanopore2.spades --careful --only-assembler

2. tmux at -t spades
3. K77 didn't work
4. Also got warning that the reads were 151 bp?

		Maybe talking about the short reads that I used w/ nanopore
5. abyss-fac -e 665000000 final_contigs.fasta for k55

		1025
6. Something went wrong and it didn't scaffold using the Nanopore data


		Error ==  system call for: "['/share/SPAdes-3.5.0-Linux/bin/spades', '/mnt/data3/lah/nanopore/spades/harmonia.nanopore.spades/K77/configs/config.info']" finished abnormally, err code: -9

		======= SPAdes pipeline finished WITH WARNINGS!

			=== Pipeline warnings:
 			
 			* Default k-mer sizes were set to [21, 33, 55, 77] because estimated read length (151) is equal to or greater than 150	
 
 7. Pick up where it left off
 		spades.py -1 harm1.fq -2 harm2.fq --nanopore corrected_LR.fq -t 10 -m 500 -o harmonia.nanopore.spades --careful --only-assembler --continue
 		
 		== Error ==  the output_dir should exist for --continue and for --restart-from!
			(wasn't up above the harmonia.nanopore.spades output file)
			
			
8. abyss-fac -e 665000000 contigs.fasta					
			
			NG50 only 1608
			
9. abyss-fac -e 665000000 scaffolds.fasta						
			
			NG50 1633
10. saving output : mv contigs.fasta 21.33.55.77.contigs.fasta		

##Re-run spades with larger kmer	
1. spades.py -1 harm1.fq -2 harm2.fq --nanopore corrected_LR.fq -t 10 -m 500 -k 91,111,127 -o harmonia.nanopore.spades_91,111,127 --careful --only-assembler

			Died
			== Error ==  system call for: "['/share/SPAdes-3.5.0-Linux/bin/corrector', '/mnt/data3/lah/nanopore/spades/harmonia.nanopore.spades_91,111,127/mismatch_corrector/contigs/configs/corrector.info', '/mnt/data3/lah/nanopore/spades/harmonia.nanopore.spades_91,111,127/misc/assembled_contigs.fasta']" finished abnormally, err code: -11
			
2. tmux at -t spades			

3. spades.py -1 harm1.fq -2 harm2.fq --nanopore corrected_LR.fq -t 10 -m 500 -k 91,111,127 -o harmonia.nanopore.spades_91,111,127 --careful --only-assembler --continue

4. abyss-fac -e 665000000 contigs.fasta
		
		2939			
5. scaffolds didn't form spades.py -1 harm1.fq -2 harm2.fq --nanopore corrected_LR.fq -t 10 -m 500 -k 91,111,127 -o harmonia.nanopore.spades_91,111,127 --careful --only-assembler --continue	

6. abyss-fac -e 665000000 scaffolds.fasta 

		3045
	

	
**These low values are probably due to the fact that there is very low coverage for my nanopore work, follow this pipeline when I have more data**


			 


	

			
