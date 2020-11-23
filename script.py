#!/usr/bin/python3
import os
import sys
import subprocess,shutil
import re

# user input will be put in a library 
details={}
details["Protein"]   = input("What protein do you want? ")
details["Taxon"]    = input("Which taxonomic group do you want to search for? ")
details["Partial"] = input ("Do you want to include partial proteins? Please answer yes or no ")

# yes and no function which return true or false to use for conditions 
def yes_no(answer):
	yes = set(['yes','y'])		# both yes or y will return true
	no = set(['no','n']) 		# both no or n will return true
	choice = answer.lower()		# set all types of answer to lower case
	# loop forever until something is returned
	while True:		
		if choice in yes:		# both yes or y will return true
			return True
		elif choice in no:		# both no or n will return true
			return False
		else:					# error trap, all other input will cause the function to ask "yes or no" over and over until a desired answer is received
			print ("\n Please respond with 'yes' or 'no' \n")
			choice = input(" yes or no?").lower()


# search function to retrieve sequences from ncbi database base on users input 
# depend on the search results, different outcomes are possible, downloading sequences are optional
def search(protein,taxon,partial) :
	import string
	# error trap, input protein for search cannot be empty or spaces
	if len(protein)==0 or str.isspace(protein):
        	print("\n Sorry, no protein was chosen, please try again..\n")        	
    # error trap, input taxon name for search cannot be empty or spaces    	
	elif len(taxon)==0 or str.isspace(taxon):
        	print("\n Sorry, no taxon was chosen, please try again..\n")
    
    # call yes_no function to evaluate if user want to include partial proteins or not
    # only carry on this part if it is true     	
	elif yes_no(partial):
		# print search information of protein input and taxon input
		print("\n Protein sequences searching for:\n\tProtein:",protein,"\n\tTaxon:",taxon,"\n\tPartial: Yes")
		# esearch in shell, taxon and protein as query  
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" "
		# shell language to extract count number after doing esearch
		es_number = es + "|grep -i \"count\"|awk \'{split($0,a,\"<|>\");print a[3];}\'"
		# print process message
		print("\n This is what I am running for you in shell \n\n " + es + "\n\n Please wait... \n")
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
			dow = input(" Do you want to download the sequences on your server? (Please note: taxon name will be used as output file name.) Please respond yes or no.")
			# starting downloading if response is yes
			if yes_no(dow):
				print("\n\n Downloading sequences...\n\n Please wait... \n")
				# output file name is based on user's taxon input
				file_name = ''.join(i for i in taxon if i.isalnum())
				# download sequence with efetch and save sequances in file_name based on user's taxon input
				ef = es + "|efetch -db protein -format fasta >"+ file_name +".nuc.fa"
				# print processing message
				print("\n This is what I am running for you in shell\n\n " + ef + "\n\n Please wait... \n")
				# call download in shell
				subprocess.call(ef,shell=True)
				# open the downloaded file and and confirm protein sequence number by counting ">" 
				print ("\n------\n Sequence downloaded! Checking " + file_name + ".nuc.fa content... \n")  
				file_contents = open(file_name + ".nuc.fa").read()
				count = file_contents.count('>')
				# print confirmation message
				print ("\n------\n Check completed." + str(count) + " protein sequences were successfully retrieved! Protein sequences are saved in " \
				+ file_name +".nuc.fa \n" )
			# if user do not want to continue downloading sequences, quit the script
			else:
				print("Thank you for searching! Bye!")
				quit()				
	
	# all the same as above but searching with 'no partial' as additional query keyword 
	# only proceed from here if yes_no(partial) returns false
	else:
		print("\n Protein sequences searching for:\n\tProtein:",protein,"\n\tTaxon:",taxon,"\n\tPartial: No")
		file_name = ''.join(i for i in taxon if i.isalnum())
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " Not partial" + " \" " 
		# shell language to extract count number after doing esearch
		es_number = es + "|grep -i \"count\"|awk \'{split($0,a,\"<|>\");print a[3];}\'"
		# print process message
		print("\n This is what I am running for you in shell \n\n " + es + "\n\n Please wait... \n")
		
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
			dow = input(" Do you want to download the sequences on your server? (Please note: taxon name will be used as output file name.)\n\n Please respond yes or no.")
			# starting downloading if response is yes
			if yes_no(dow):
				print("\n\n Downloading sequences...\n\n Please wait... \n")
				# output file name is based on user's taxon input
				file_name = ''.join(i for i in taxon if i.isalnum())
				# download sequence with efetch and save sequances in file_name based on user's taxon input
				ef = es + "|efetch -db protein -format fasta >"+ file_name +".nuc.fa"
				# print processing message
				print("\n This is what I am running for you in shell\n\n " + ef + "\n\n Please wait... \n")
				# call download in shell
				subprocess.call(ef,shell=True)
				# open the downloaded file and and confirm protein sequence number by counting ">" 
				print ("\n------\n Sequence downloaded! Checking " + file_name + ".nuc.fa content... \n")  
				file_contents = open(file_name + ".nuc.fa").read()
				count = file_contents.count('>')
				# print confirmation message
				print ("\n------\n Check completed." + str(count) + " protein sequences were successfully retrieved! Protein sequences are saved in " \
				+ file_name +".nuc.fa \n" )
			# if user do not want to continue downloading sequences, quit the script
			else:
				print("Thank you for searching! Bye!")
				quit()				


# function to read the file downloaded by 'search' function and analyse the sequences if the file exists
def analyse(protein,taxon,partial):
		# to find the file generated by 'search' function
		file_name = ''.join(i for i in taxon if i.isalnum())
		import os.path
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
				answer = input(" yes or no?")
				# only if user answers is true do following
				if yes_no(answer):
					print("To access the sequence similarity")
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
								
					# multiple alignment within species by clustalo	and conservation plots by plotcon
					for i in range(len(spe)):
						# species name without special characters
						files = ''.join(a for a in spe[i] if a.isalnum())
						# alignment within species, output in tree-order, more closely related sequence are at the bottom of the file
						align = "clustalo -i "+ files + ".fasta -o " + files + ".align.fasta --output-order=tree-order"
						subprocess.call(align, shell=True)
						# conservation plots saved in .svg and subtitle uses species name	
						plot = "plotcon -winsize 4 -graph svg -gdirectory ./plotcon -gsubtitle=\"" + files + " " + files + ".align.fasta"
						subprocess.call(plot,shell=True)  
				else:
					print("Thank you! Bye!")
					quit()
			else:
				quit()
		else:
			print("\n\n Ummm, something is wrong. No downloaded file found. \n")		

# call 'search' function and pass multiple arguments from the 'details' library to the function as a list 
search(*list(details.values()))

# call 'analyse' function and pass multiple arguments from the 'details' library to the function as a list 
analyse(*list(details.values()))


