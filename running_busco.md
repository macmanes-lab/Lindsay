##Running BUSCO

**WD: /mnt/data3/lah/busco**

1. Not in path... source ~/.profile

1. wget http://busco.ezlab.org/files/arthropoda_buscos.tar.gz
2. tar -zxvf arthropoda_buscos.tar.gz
3. ln -s /mnt/data3/lah/abyss/nontrimmed.bless.no.norm.no.txn/k111/k111-scaffolds.fa
4. tmux new -s busco
3. python3 /share/BUSCO_v1.1b1/BUSCO_v1.1b1.py -o harmonia.assembly.busco -in k111-scaffolds.fa -l arthropoda