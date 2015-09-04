August 31, 2015
###Three types of programming languages
1. Strings of numbers giving machine specific instructions (Martian language)
2. Assembly language 

		English-like abbreviations representing elementary computer operations
3. 	High-level languages

		Codes written in non redundant, unambiguous subset of everyday English
		
		*must be translated by compilers or interpreters*
		
		Pyhon is a hybrid between a complied and *interpretated* languages 
###Why Python?

-Freely available open source project	

-Actively developed 

-Cross platform	

-Well developed scientific libraries
		
		1. NumPy
		2. SciPy
		3. matplotlib	
		
September 2, 2015
#LINUX/UNIX

- LINUX is a clone of UNIX (it is the free version)
- Architehture independent 
- Structure:
	- **Kernal** - controls the computer resources and schedules jobs
	- **Shell** - Command interpreter in chief
	- **Commands** - comprehensive set of inbuilt utilities that are universally required by Linux/Unix administrators & users. 
	- **Programs/ scripts/ executables** - variable number of user/programmer defined utilities that are developed for specific tasks such as bioinformatics analysis or document processing 

- /bin/ is short for binary, this is where the compiled files are 
- /dev/ device files
- /etc/ congiguration files
- /lib/ essential shred libraries 
- /mnt/ temporarily mounted filesystems
- /opt/ add-on application software packages (third party software)


#Working in Shell

- fg - foreground
- bg - background 
- logging into wildcat unix shell 
- exit - leave a shell

September 4, 2015
#Getting help

- man command
- info command
- command --help
- whatis command
- apropos term --> I am clueless, show me anything you have 

#Linux/unix command structure

- command [option] [argument]
	- options are modifies of command
	- arguments are input upon which the command is supposed to act 
	
#wget important flags 
- -i  (download all URL's that are found in this file)
- -t 
- -nc
- -N
- -c 
- -T

#Editing commands	
- Alt (control + option on macs) + b = jump backward to the next word
- Alt (control + option on macs) + f = jump forward to the next word
- Ctrl + a = return to the start of the command you are typing
- Ctrl + e = go to the end of the fommand you are typing
- Erase characters
	- backspace of ctrl-backspace
- Delete entire word
	-  Ctrl - w
- delete and entire line
	- Ctrl - u 

#whereis/which	
- whereis list more than 1 path for the command 
- which displays the one computer uses/calls first when the command is called to action
- file (shows the type of files)

#creating/ adding lines to a file 
- touch filename
- echo "what ever text you want to write" > file
- echo "I want to add lines to this file, not override it" >> file

#cat vs more also wc
- cat displays everything at once 
- more allows you to paruse through your file one screen at a time
- wc filename gives you *lines* *words/tokens* *bites*