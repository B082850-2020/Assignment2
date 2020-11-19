#!/usr/bin/python3
import os
import sys
import subprocess,shutil
import re

details={}
details["Protein"]   = input("What protein do you want? ")
details["Taxon"]    = input("What taxon for the protein? ")


def search(protein,taxon) :
	import string
	if len(protein)==0:
        	print("no protein was chosen")
	elif len(taxon)==0:
        	print("no taxon was chosen, please try again..")
	else:
        	print("\nYou have provided the following keywords for sequence searching:		\n\tProtein:",protein,"\n\tTaxon:",taxon)
	es = "esearch -db protein -query \" "+ taxon +" AND "+ protein +" \" " + \
	"|efetch -db protein -format fasta >"+ ''.join(i for i in taxon if i.isalnum()) +".nuc.fa"
	print("This is what I am going to run for you in a shell\n" + es)
	subprocess.call(es,shell=True)

search(*list(details.values()))
    



