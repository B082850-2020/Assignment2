#!/usr/bin/python3
import os
import sys
import subprocess,shutil
import re

details={}
details["Protein"]   = input("What protein do you want? ")
details["Taxon"]    = input("What taxon for the protein? ")
details["Partial"] = input ("Do you want to include partial proteins? yes or no ")

def yes_no(answer):
	yes = set(['yes','y'])
	no = set(['no','n']) 
	choice = answer.lower()
	while True:
		if choice in yes:
			return True
		elif choice in no:
			return False
		else:
			print ("\n Please respond with 'yes' or 'no' \n")
			choice = input(" yes or no?").lower()


def search(protein,taxon,partial) :
	import string
	if len(protein)==0 or str.isspace(protein):
        	print("\n Sorry, no protein was chosen, please try again..\n")
        	
	elif len(taxon)==0 or str.isspace(taxon):
        	print("\n Sorry, no taxon was chosen, please try again..\n")
        	
	elif yes_no(partial):
		print("\n Protein sequences searching for:\n\tProtein:",protein,"\n\tTaxon:",taxon,"\n\tPartial: Yes")
		file_name = ''.join(i for i in taxon if i.isalnum())
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" -sort \"Organism Name\" "
		es_number = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" "+ \
        	"|grep -i \"count\"|awk \'{split($0,a,\"<|>\");print a[3];}\'"
		print("\n This is what I am going to run for you \n\n " + es + "\n\n Please wait... \n")
		seq_number = subprocess.check_output(es_number,shell=True)
		
		if int(seq_number) > 1000:
			print("\n ** Warning: Over 1000 sequences found, continue is not recommanded, please narrow down your search,"+ \
			"\n otherwise very slow processing speed and probably taking too much space! Thank you! \n")
			quit()
		if int(seq_number) == 0:
			print("\n Sorry, no sequence was found! Likely spelling mistakes. Please try again. Thank you! \n")
		else:
			print("\n "+ str(seq_number.decode('ascii').rstrip()) +" sequences was found! Nice choice! Downloading sequences...\n\n Please wait... \n")
			ef = es + "|efetch -db protein -format fasta >"+ file_name +".nuc.fa"
			subprocess.call(ef,shell=True)
			file_contents = open(file_name + ".nuc.fa").read()
			count = file_contents.count('>')

			spe = set(re.findall('\[.*?\]',file_contents))
			print ("\n " + str(count) + " protein sequences successfully retrived! Protein sequences are saved in " \
			+ file_name +".nuc.fa \n" )

			if len(spe) >1:
				print("\n Sequences are from " + str(len(spe)) + " different species. Do you really wish to continue? \n")
				answer = input(" yes or no?")
				if yes_no(answer):
					quit()	
				elif yes_no(answer)==False:
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
			print("\n ** Warning: Over 1000 sequences found, continue is not recommanded, please narrow down your search,"+ \
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
				print (" Something went wrong.. No sequence was retrived. Did you put the right taxon name? ")
			else:
				print ("\n "+str(seq) +" protein sequences successfully retrived! Protein sequences are saved in " \
				+ file_name +".nuc.fa \n" )

search(*list(details.values()))
 



