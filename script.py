#!/usr/bin/python3
import os
import sys
import subprocess,shutil
import re
import string
import os.path

## user input will be put in a library 
details={}
details["Protein"]   = input(" What protein do you want to search for? ")
details["Taxon"]    = input(" Which taxonomic group do you want to search for? ")
details["Partial"] = input (" Do you want to include partial proteins? Please answer yes or no ")


## yes and no function which return True or False to use for conditions 
def yes_no(answer):
	yes = set(['yes','y'])		# both yes or y will return True
	no = set(['no','n']) 		# both no or n will return False
	choice = answer.lower()		# set all types of answer to lower case
	# loop forever until something is returned
	while True:		
		if choice in yes:		# both yes or y will return True
			return True
		elif choice in no:		# both no or n will return False
			return False
		else:					# error trap, all other input will cause the function to ask "yes or no" over and over until a desired answer is received
			print ("\n Please respond with 'yes' or 'no' \n")
			choice = input(" yes or no?").lower()


## search function to retrieve sequences from ncbi database base on users input 
# depend on the search results, different outcomes are possible, downloading sequences are optional
def search(protein,taxon,partial) :
	# error trap, input protein for search cannot be empty or spaces
	if len(protein)==0 or str.isspace(protein):
        	print("\n Sorry, no protein was chosen, please try again..\n")        	
    # error trap, input taxon name for search cannot be empty or spaces    	
	elif len(taxon)==0 or str.isspace(taxon):
        	print("\n Sorry, no taxon was chosen, please try again..\n")
    
    # call yes_no function to evaluate if user want to include partial proteins or not
    # only carry on this part if it is True     	
	elif yes_no(partial):
		# print search information of protein input and taxon input
		print("\n Protein sequences searching for:\n\tProtein:",protein,"\n\tTaxon:",taxon,"\n\tPartial: Yes")
		# esearch in shell, taxon and protein as query  
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" "
		# shell language to extract count number after doing esearch
		es_number = es + "|grep -i \"count\"|awk \'{split($0,a,\"<|>\");print a[3];}\'"
		# print process message
		print("\n This is what is running in shell: \n\n " + es + "\n\n Please wait... \n")
		# run es_number in shell to find search count and output is pulled as a byte string
		seq_number = subprocess.check_output(es_number,shell=True)
		
		# convert byte string into integer and if sequence number is over 1000, script will end with a warning message 
		if int(seq_number) > 1000:
			print("\n ** Warning: Over 1000 sequences found, continue is not recommended, please narrow down your search,"+ \
			"\n otherwise very slow processing speed and probably taking too much space! Thank you! \n")
			quit()
		# error trap, if no search result, error message with a hint of potential spelling mistake 
		if int(seq_number) == 0:
			print("\n Sorry, no sequence was found! Likely spelling mistakes. Please try again. Thank you! \n")
			quit()
		# otherwise carry on
		else:
			# print amount of the sequence found, nubmer converted from byte string to normal string
			print("\n------\n "+ str(seq_number.decode('ascii').rstrip()) +" sequences was found! Nice choice! \n\n")
			
			# provide choices for user by ask if they want to download the sequences or not
			dow = input(" Do you want to download the sequences on your server? (Please note: taxon name will be used as output file name.) \n\n Protein sequence analysis will only be available if sequences are downloaded. \n\n If your changed your mind about your search, you can reply no and start over again.\n\n Please respond yes or no. ")
			# yes_no function: only start downloading if response returns True
			if yes_no(dow):
				print("\n------\n Downloading sequences...\n\n Please wait... \n")
				# output file name is based on user's taxon input
				file_name = ''.join(i for i in taxon if i.isalnum())
				# download sequence with efetch and save sequances in file_name based on user's taxon input
				ef = es + "|efetch -db protein -format fasta >"+ file_name +".nuc.fa"
				# print processing message
				print("\n This is what is running in shell: \n\n " + ef + "\n\n Please wait... \n")
				# call download in shell
				subprocess.call(ef,shell=True)
				# open the downloaded file and and confirm protein sequence number by counting ">" 
				print ("\n------\n Sequence downloaded! Checking " + file_name + ".nuc.fa for content... \n")  
				file_contents = open(file_name + ".nuc.fa").read()
				count = file_contents.count('>')
				# print confirmation message
				print ("\n------\n Check completed. " + str(count) + " protein sequences were successfully retrieved! Protein sequences are saved in " \
				+ file_name +".nuc.fa \n" )
			# if user do not want to continue downloading sequences, quit the script
			else:
				print("\n Thank you for searching! Bye! \n")
				quit()				
	
	# all the same as above but searching with 'no partial' as additional query keyword 
	# only proceed from here if yes_no(partial) returns False
	else:
		print("\n Protein sequences searching for:\n\tProtein:",protein,"\n\tTaxon:",taxon,"\n\tPartial: No")
		file_name = ''.join(i for i in taxon if i.isalnum())
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " Not partial" + " \" " 
		# shell language to extract count number after doing esearch
		es_number = es + "|grep -i \"count\"|awk \'{split($0,a,\"<|>\");print a[3];}\'"
		# print process message
		print("\n This is what is running in shell: \n\n " + es + "\n\n Please wait... \n")
		
		# run es_number in shell to find search count and output is pulled as a byte string
		seq_number = subprocess.check_output(es_number,shell=True)
		# convert byte string into integer and if sequence number is over 1000, script will end with a warning message 
		if int(seq_number) > 1000:
			print("\n ** Warning: Over 1000 sequences found, continue is not recommended, please narrow down your search,"+ \
			"\n otherwise very slow processing speed and probably taking too much space! Thank you! \n")
			quit()
		# error trap, if no search result, error message with a hint of potential spelling mistake 
		if int(seq_number) == 0:
			print("\n Sorry, no sequence was found! Likely spelling mistakes. Please try again. Thank you! \n")
			quit()
		# otherwise carry on
		else:
			# print amount of the sequence found, nubmer converted from byte string to normal string
			print("\n------\n "+ str(seq_number.decode('ascii').rstrip()) +" sequences was found! Nice choice! \n\n")
			
			# provide choices for user by ask if they want to download the sequences or not			
			dow = input(" Do you want to download the sequences on your server? (Please note: taxon name will be used as output file name.) \n\n Protein sequence analysis will only be available if sequences are downloaded. \n\n If your changed your mind about your search, you can reply no and start over again.\n\n Please respond yes or no. ")
			# yes_no function: only start downloading if response returns True
			if yes_no(dow):
				print("\n------\n Downloading sequences...\n\n Please wait... \n")
				# output file name is based on user's taxon input
				file_name = ''.join(i for i in taxon if i.isalnum())
				# download sequence with efetch and save sequences in file_name based on user's taxon input
				ef = es + "|efetch -db protein -format fasta >"+ file_name +".nuc.fa"
				# print processing message
				print("\n This is what is running in shell: \n\n " + ef + "\n\n Please wait... \n")
				# call download in shell
				subprocess.call(ef,shell=True)
				# open the downloaded file and and confirm protein sequence number by counting ">" 
				print ("\n------\n Sequence downloaded! Checking " + file_name + ".nuc.fa for content... \n")  
				file_contents = open(file_name + ".nuc.fa").read()
				count = file_contents.count('>')
				# print confirmation message
				print ("\n------\n Check completed. " + str(count) + " protein sequences were successfully retrieved! Protein sequences are saved in " \
				+ file_name +".nuc.fa \n" )
			# if user do not want to continue downloading sequences, quit the script
			else:
				print("Thank you for searching! Bye!")
				quit()				


## function to read the file downloaded by 'search' function and analyse the sequences if the file exists
def similarity(protein,taxon,partial):
		# to find the file generated by 'search' function
		file_name = ''.join(i for i in taxon if i.isalnum())
		# only carry on if the file exists
		if os.path.isfile(file_name + ".nuc.fa"):
			# read downloaded sequences
			file_contents = open(file_name + ".nuc.fa").read()
			# count unique species number, using regex to find all the text with [] around
			spe = list(set(re.findall('\[.*?\]',file_contents)))
			genus = list(set(re.findall('\[\w*',file_contents)))
			
			# if more than one species in the downloaded file do following
			if len(spe) >1:
				#print species count and ask if user want to continue or not
				print("\n Sequences are from " + str(len(genus))+ " different genera and there are " + str(len(spe)) + " different species in total. Do you wish to continue? \n")
				answer = input(" Please respond yes or no. ")
				# yes_no function: only when user's answer returns True do following
				if yes_no(answer):
					# print information about following steps
					print("\n------\n\n Sequence similarity can established either within species or between species (max 250 sequences), conservation plots can be done accordingly. \n")
					# ask user if within sequence conservation is desired
					within = input("\n\n Do you wish to assess conservation within each species? \n\n Alignment will be done for each species and conservation plot will be available for each alignmnet. \n\n Please respond yes or no.")	
					# yes_no function: only proceed this part if user answer is True
					if yes_no(within):
						# print sorting message
						print("\n------\n Start sorting sequences by species... Sequences of same species will be put into a new separate file \n")	
						# sort the sequences by species and output into different files
						lines = open(file_name + ".nuc.fa").readlines()
						for line in lines:		# loop over each line of the file
							for i in range(len(spe)):		# loop for each unique species 	
								if spe[i] in line:			# if line contains the species name
									acc = str(re.findall("^>\w*..",line)).strip("['>']")	# use regex to find the accession in that line, convert it to string and strip special characters 
									files = ''.join(a for a in spe[i] if a.isalnum())		# use the species name as output file name, strip off special characters
									# shell command to pull sequence using the accession, append the sequence to the new file
									sort = "seqkit grep -r -p " + acc +" " + file_name + ".nuc.fa >>" + files + ".fasta"
									subprocess.call(sort, shell=True)	# call the shell command
						# print sorting job done message
						print("\n Sequence sorting is done. Sequences for each species can now be found in fasta files under species names \n")  
						direc = input("\n------\n Multiple plots will be generated after alignment, would you like to store all the plots in a new directory \".\plotcon\"? \n\n Please respond yes or no.") 
						# yes_no function: if a new directory is wanted do fowllowing
						if yes_no(direc):
							try:	# try making a new directory 
								mkdir = "mkdir plotcon"		# shell command to make a new directory called plotcon
								subprocess_checkout(mkdir,shell=True)	# if making directory failed, try fails, except would proceed
							except:	# if failed,do following
								# print error message and ask user if want to continuew without a directory
								conti = input("\n Seems like there was an error when making a new directorty. Do you wish to continue without a new directory? \n\n Please respond yes or no.") 
								# yes_no function: if user wish to carry on do following
								if yes_no(conti):
									Print("\n Aligning sequences within species and plotting conservation for each of them. \n\n Please wait... \n")
									# multiple alignment within species by clustalo	and conservation plots by plotcon
									for i in range(len(spe)):
										# species name without special characters
										files = ''.join(a for a in spe[i] if a.isalnum())
										# alignment within species, output in tree-order, more closely related sequence are at the bottom of the file
										within_align = "clustalo -i "+ files + ".fasta -o " + files + ".align.fasta --output-order=tree-order"
										subprocess.call(within_align, shell=True)
										# conservation plots saved in .svg and subtitle uses species name	
										plot = "plotcon -winsize 4 -graph svg -gdirectory ./plotcon -gsubtitle=\"" + files + "\" " + files + ".align.fasta"
										subprocess.call(plot,shell=True)
										# shell command to rename each plot to prevent overwrite
										rename = "mv plotcon.svg " + file_name + ".svg"
										# call the rename shell command
										subprocess.call(rename,shell=True)
									print(" Alignments are done. Alignment within species sorted in tree order can be found in .align.fasta files")
									print(" \n\n Conservation plot is ready in .svg files under species name \n")  
								# if user do not want to continue
								else:
									print("\n Sorry to hear that you do not want to continue! Have a nice day. Bye. \n")
									quit()
						# carry on without a new directory
						else:
							Print("\n Aligning sequences within species and plotting conservation for each of them. \n\n Please wait... \n")
							# multiple alignment within species by clustalo	and conservation plots by plotcon
							for i in range(len(spe)):
								# species name without special characters
								files = ''.join(a for a in spe[i] if a.isalnum())
								# alignment within species, output in tree-order, more closely related sequence are at the bottom of the file
								within_align = "clustalo -i "+ files + ".fasta -o " + files + ".align.fasta --output-order=tree-order"
								subprocess.call(within_align, shell=True)
								# conservation plots saved in .svg and subtitle uses species name	
								plot = "plotcon -winsize 4 -graph svg -gsubtitle=\"" + files + "\" " + files + ".align.fasta"
								subprocess.call(plot,shell=True)
								# shell command to rename each plot to prevent overwrite
								rename = "mv plotcon.svg " + file_name + ".svg"
								# call the rename shell command
								subprocess.call(rename,shell=True)	 
							print(" Alignments are done. Alignment within species sorted in tree order can be found in .align.fasta files")
							print(" \n\n Conservation plot is ready in .svg files under species name \n")  
						
					# if user do not want within species similarity, ask if user wants conservation across the species 
					else:
						between = input("\n\n Do you wish to assess the conservation between all the species? Note: maximum 250 sequences can be processed this way. The more sequences, the longer the alignment will be... \n\n Please respond yes or no.")
						# yes_no function: carry on if user response is True
						if yes_no(between):
							print("\n------\n Trying to align sequences... Please wait... \n\n (The more sequences, the longer the alignment is...) \n")
							# shell command to align the sequences across species and output 
							between_align = "clustalo -i "+ file_name + ".nuc.fa -o " + file_name + ".align.nuc.fa --output-order=tree-order --maxnumseq=250"
							# try to align the sequences, if error occurs, print error message
							try:
								subprocess.call(between_align,shell=True)	# try call the shell command align in python
								print(subprocess.check_output(between_align,shell=True))	# when this command fail, try fail and error message will show up
							except:
								print("\n\n Sorry, error occured when trying to align the sequences! Did you have more than 250 sequences? \n") # error trap
							# only carry on if alignments are successfully written in file
							if os.path.isfile(file_name + ".align.nuc.fa"):
								# if the file created, print alignment success message 
								print("\n\n Sequences aligned successfully! Alignments are stored in " + file_name + ".align.nuc.fa and sorted in phylogenetic order \n")
								# print plotting progress
								print(" \n------\n Start plotting conservation plot based on the alignment. \n")
								# shell command to plot conservation plot 
								all_plot = "plotcon -winsize 4 -graph svg -gsubtitle=\"" + file_name + "\" " + file_name + ".align.nuc.fa"
								# call the shell command all_plot in python
								subprocess.call(all_plot,shell=True)
								# shell command to rename each plot to prevent overwrite
								all_rename = "mv plotcon.svg " + file_name + ".svg"
								# call the rename shell command
								subprocess.call(all_rename,shell=True)
								# print plotting job donw message 
								print(" \n\n Conservation plot is now ready in .svg file under taxon name. \n")
							else:
								print(" \n Something went wrong with the alignment, no alignment file can be found. \n")	# error trap
						# if user do not want any of the above analysing methods
						else:
							print("\n\n Sorry, no other similarity test is available. \n")
							
				# quit if do not want to continue with multiple species
				else:
					print("\n Thank you for searching! Bye! \n")
					quit()
			
			# if there is only one species among the downloaded sequences do following
			else:
				# confirming user want to proceed with similarity analysis
				single = input("\n\n All downloaded sequences belong to one species. \n\n Do you want to proceed with aligning sequences and plotting a conservation plot base on these sequences? \n\n Please respond yes or no. ")
				# yes_no function: proceed if user wish to continue
				if yes_no(single):
					# species name without special characters
					species_file = ''.join(a for a in spe[0] if a.isalnum())
					# alignment within species, output in tree-order, more closely related sequence are at the bottom of the file
					single_align = "clustalo -i "+ file_name + ".nuc.fa -o " + species_file + ".align.fasta --output-order=tree-order"
					subprocess.call(single_align, shell=True)
					# conservation plots saved in .svg and subtitle uses species name	
					single_plot = "plotcon -winsize 4 -graph svg -gsubtitle=\"" + species_file + "\" " + species_file + ".align.fasta"
					subprocess.call(single_plot,shell=True)
					# shell command to rename each plot to prevent overwrite
					single_rename = "mv plotcon.svg " + species_file + ".svg"
					# call the rename shell command
					subprocess.call(single_rename,shell=True) 
					print(" \n\n Conservation plot is ready in .svg file under species name \n")   
				# if user do not want to proceed with analysis, print the message and quit the script
				else:
					print("\n Ok! \n")

## a motif research function to find match pattern from Prosite databse
def motif(protein,taxon,partial):
	# to find the file generated by 'search' function
	file_name = ''.join(i for i in taxon if i.isalnum())
	# only carry on if the file exists
	if os.path.isfile(file_name + ".nuc.fa"):
		# ask user if protein motif search wanted  
		prosite_search = input("\n------\n Do you want to search all the sequences against Prosite database to find motif patterns? \n\n Please respond yes or no. ")
		# yes_no function: only carry on if user's respond returns True 
		if yes_no(prosite_search):
			# read downloaded sequences
			file_contents = open(file_name + ".nuc.fa").read()
			# number of sequences in the file
			count = file_contents.count('>')
			# split the file by accessions
			split = "seqkit split --quiet -i " + file_name + ".nuc.fa"
			subprocess.call(split,shell=True)
			# download the accession file from database
			es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" "	
			ef = es + "|efetch -db protein -format acc >"+ file_name + ".acc.fa"
			subprocess.call(ef,shell=True)
			# read the accession file line by line
			acce = open(file_name + ".acc.fa").readlines()
			# prepare an empty list for the loop to store hit result
			hit_list=[]
			# loop over every sequence in the sequence file 
			for i in range(count):	
				acc = str(acce[i]).rstrip()		# strip off new line from each accession file line
				if acc in file_contents:
					try:
						file_path = file_name +".nuc.fa.split/" + file_name + ".nuc.id_" + acc + ".fa"		# file path to the sequence with accession from the list
						prosite = "patmatmotifs -auto " +  file_path + " -rname2 " + acc + " -rdirectory2 " + file_name + ".nuc.fa.split"	# search motif pattern against prosite database
						subprocess.call(prosite,shell=True)		# call the shell command 
						file = open(file_name + ".nuc.fa.split/" + acc + ".patmatmotifs").read()	# open the output file
						hit = re.findall('#.\w*:.(\d)',file)	# find all the hit count, group the hit number 
						hit_list.append(int(hit[0]))	# append the count as a integer to a list 
						if int(hit[0]) != 0 :	# report hit counts that are not 0 in the terminal with its accession number
							print("\n " + acc + " has " + hit[0] +  " hits \n")
					except:
						print("\n Bad file name found. No match with accesssion. Pass sequence.\n")		# error trap
						pass
			# remove redundant element in the hit_list  
			hit_list = list(dict.fromkeys(hit_list))
			# if hit_list only have 1 element and it is 0, it means that no hit was found for any sequence
			if len(hit_list) == 1 and int(hit_list[0]) == 0:
				print("\n Sorry, no hit was found for any of the input sequence. \n")  
			
					

# call 'search' function and pass multiple arguments from the 'details' library to the function as a list 
search(*list(details.values()))

# call 'analyse' function and pass multiple arguments from the 'details' library to the function as a list 
similarity(*list(details.values()))

# call 'motif' function and pass multiple arguments from the 'details' library to the function as a list 
motif(*list(details.values()))
