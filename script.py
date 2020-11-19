#!/usr/bin/python3
import os
import sys
import subprocess,shutil
import re

details={}
details["Protein"]   = input("What protein do you want? ")
details["Taxon"]    = input("What taxon for the protein? ")
details["Partial"] = input ("Do you want to include partial proteins? y or n ")


def search(protein,taxon,partial) :
	import string
	if len(protein)==0:
        	print("no protein was chosen,please try again..")
	elif len(taxon)==0:
        	print("no taxon was chosen, please try again..")
	elif partial=='y':
		print("\n Protein sequences searching for:\n\tProtein:",protein,"\n\tTaxon:",taxon,"\n\tPartial: Yes")
		file_name = ''.join(i for i in taxon if i.isalnum())
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" "
		es_number = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" "+ \
        	"|grep -i \"count\"|awk \'{split($0,a,\"<|>\");print a[3];}\'"
		print("This is what I am going to run for you \n" + es)
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
			print ("\n "+str(seq) +" protein sequences successfully retrived! Protein sequences are saved in " \
			+ file_name +".nuc.fa \n" )

	elif partial=='n':
		print("\n Protein sequences searching for:\n\tProtein:",protein,"\n\tTaxon:",taxon,"\n\tNo partial")
		file_name = ''.join(i for i in taxon if i.isalnum())
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + "Not partial" + " \" " 
		es_number = "esearch -db protein -query \" "+ taxon +" AND "+ protein + "Not partial" + " \" "+ \
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
			print ("\n "+str(seq) +" protein sequences successfully retrived! Protein sequences are saved in " \
			+ file_name +".nuc.fa \n" )
	else :
		print("please answer y or n")

search(*list(details.values()))
 



