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
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " \" " \
"|efetch -db protein -format fasta >"+ ''.join(i for i in taxon if i.isalnum()) +".nuc.fa"
		print("This is what I am going to run for you in a shell\n" + es)
		subprocess.call(es,shell=True)
	elif partial=='n':
		print("\n Protein sequences searching for:\n\tProtein:",protein,"\n\tTaxon:",taxon,"\n\tNo partial")
		es = "esearch -db protein -query \" "+ taxon +" AND "+ protein + " Not partial"+ " \" " + \
"|efetch -db protein -format fasta >"+ ''.join(i for i in taxon if i.isalnum()) +".nuc.fa"
		print("This is what I am going to run for you in a shell\n" + es)
		subprocess.call(es,shell=True)
	else :
		print("please answer y or n")
search(*list(details.values()))
    



