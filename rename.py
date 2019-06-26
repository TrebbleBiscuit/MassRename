# Author - Erik Nielsen
# 
# This program is used to rename files with sections separated by delimiters that need to be rearranged.

import os  # Used to get the file names and rename them
import re  # Used for spliting a string by multiple delimiters

def main(): 
    dirname = "ToRename"  # Files in this folder will be renamed.
    indexlist = [2, 4, 1, 0]  # Ordered list of sections to append to the file name
    ignoreerrors = False  # Does the program continue running after a duplicate file error

    continueoperation = False
    for startname in os.listdir(dirname):
        filesfound = True
        namelist = re.split('[_.]', startname)  # Split file name by the delimiters within the brackets
        for x in indexlist:  # Moves through index, adding each section to the file name
            try:
                finalname = finalname + "_" + (namelist[x])  # Sections are separated by an underscore
            except NameError:
                finalname = namelist[x]
        finalname = finalname + "." + namelist[-1]  # Replace file extension at end 
        if not continueoperation:
            print("\nFile will be named " + finalname)  # Make sure that the filename looks correct before continuing
            print("Are you sure you want to continue? ('y' to continue or anything else to not)")
            if input("> ") == "y":
                print("")
                continueoperation = True
            else:
                print("\nOperation Cancelled")
                return
        print("Renaming " + finalname + " - ", end='')
        try:
            os.rename(dirname + "\\" + startname, dirname + "\\" + finalname)  # Execute rename operation
            print("Success")
        except FileExistsError:
            print("Error: file with that name already exists")
            if not ignoreerrors:
                print("\nOperation Cancelled")
                return
        del finalname  # delete finalname variable before moving to new file
    try:
        filesfound
        print("\nOperation Complete")
    except UnboundLocalError: print("No files found in '" + dirname + "' directory.")

main()
