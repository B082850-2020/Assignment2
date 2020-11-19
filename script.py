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

search(*list(details.values()))
    
        query = input("do you want to continue? y or n")
        if query == "n":
            exit()
        elif query != "y":
            print("please enter yes or no") 
print ("\n\nImported os\n\n")


