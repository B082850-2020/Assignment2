#!/usr/bin/python3
import os
import sys
import subprocess,shutil
import re

# user input will be put in a library 
details={}
details["Protein"]   = input("What protein do you want? ")
details["Taxon"]    = input("What taxon for the protein? ")
details["Partial"] = input ("Do you want to include partial proteins? yes or no ")

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
# depend on the search results, different options for output are given
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
		# output file name is based on user's taxon input
		file_name = ''.join(i for i in taxon if i.isalnum())
		# esearch in shell, taxon and protein as query  
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" -sort \"Organism Name\" "
		
		# search result count after esearch
		es_number = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" "+ \
        	"|grep -i \"count\"|awk \'{split($0,a,\"<|>\");print a[3];}\'"
		
		print("\n This is what I am going to run for you \n\n " + es + "\n\n Please wait... \n")
		
		# run es_number in shell to find search count and output is pulled as byte string
		seq_number = subprocess.check_output(es_number,shell=True)
		# convert byte string to integer and if sequence number is over 1000, script will end with warning message 
		if int(seq_number) > 1000:
			print("\n ** Warning: Over 1000 sequences found, continue is not recommended, please narrow down your search,"+ \
			"\n otherwise very slow processing speed and probably taking too much space! Thank you! \n")
			quit()
		# error trap, if no search result, error message with hint of spelling mistake 
		if int(seq_number) == 0:
			print("\n Sorry, no sequence was found! Likely spelling mistakes. Please try again. Thank you! \n")
		# otherwise carry on
		else:
			# print amount of the sequence found and start downloading 
			print("\n------\n "+ str(seq_number.decode('ascii').rstrip()) +" sequences was found! Nice choice! \n\n Downloading sequences...\n\n Please wait... \n")
			# download sequence with efetch and same in file_name based on user's taxon input
			ef = es + "|efetch -db protein -format fasta >"+ file_name +".nuc.fa"
			# call download in shell
			subprocess.call(ef,shell=True)
			
			# open the downloaded file and and confirm protein sequence number by searching ">"  
			print ("\n------\n Sequence downloaded! Checking " + file_name + ".nuc.fa content... \n"  
			file_contents = open(file_name + ".nuc.fa").read()
			count = file_contents.count('>')
			# print confirmation message
			print ("\n------\n Check completed." + str(count) + " protein sequences were successfully retrieved! Protein sequences are saved in " \
			+ file_name +".nuc.fa \n" )
			
			# count unique species number
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
					for line in lines:
						for i in range(len(spe)):
							if spe[i] in line:
								acc = str(re.findall("^>\w*..",line)).strip("['>']")
								files = ''.join(a for a in spe[i] if a.isalnum())
								sort = "seqkit grep -r -p " + acc +" " + file_name + ".nuc.fa >>" + files + ".fasta"
								subprocess.call(sort, shell=True)
				# multiple alignment within species by clustalo	and conservation plots by plotcon
					for i in range(len(spe)):
						# species name without special characters
						files = ''.join(a for a in spe[i] if a.isalnum())
						# alignment within species
						align = "clustalo -i "+ files + ".fasta -o " + files + ".align.fasta"
						subprocess.call(align, shell=True)
						# conservation plots saved in .svg and subtitle uses species name	
						plot = "plotcon -winsize 4 -graph svg -gsubtitle=\"" + files + " " + files + ".align.fasta"
						subprocess.call(plot,shell=True)  
				else:
					print("Thank you! Bye!")
					quit()
			else:
				quit()
			

	else:
		print("\n Protein sequences searching for:\n\tProtein:",protein,"\n\tTaxon:",taxon,"\n\tPartial: No")
		file_name = ''.join(i for i in taxon if i.isalnum())
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + "Not partial" + " \" " 
		es_number = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " Not partial" + " \" "+ \
        	"|grep -i \"count\"|awk \'{split($0,a,\"<|>\");print a[3];}\'"
		print("This is what I am going to run for you in a shell\n" + es)
		subprocess.call(es,shell=True)
		seq_number = subprocess.check_output(es_number,shell=True)
		if int(seq_number) > 1000:
			print("\n ** Warning: Over 1000 sequences found, continue is not recommended, please narrow down your search,"+ \
			"\n otherwise very slow processing speed and probably taking too much space! Thank you! \n")
			quit()
		if int(seq_number) == 0:
			print("\n Sorry, no sequence was found! Likely spelling mistakes. Please try again. Thank you! \n")
		else:
			ef = es + "|efetch -db protein -format fasta >"+ file_name +".nuc.fa"
			subprocess.call(ef,shell=True)
			file_contents = open(file_name + ".nuc.fa").read()
			seq = file_contents.count('>')
			if seq == 0:
				print (" Something went wrong.. No sequence was retrieved. Did you put the right taxon name? ")
			else:
				print ("\n "+str(seq) +" protein sequences successfully retrieved! Protein sequences are saved in " \
				+ file_name +".nuc.fa \n" )

# call search function and pass multiple arguments from the details library as a list 
search(*list(details.values()))
 



