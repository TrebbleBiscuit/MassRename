# Author - Erik Nielsen
# 
# This program is used to rename files that have sections in their file names separated by delimiters that need to be rearranged.
# It works by separating the existing file name (by delimiters) into several sections, then
# puts the sections back in a user defined order, separating them by a user defined delimiter.

import os               # Used to get the file names and rename them
from re import split    # Used for spliting a string by multiple delimiters
import configparser     # Used for parsing config.ini

def main(): 
    ### Import configuration ###
    config = configparser.ConfigParser()
    config.read("config.ini")
    if not os.path.isfile("config.ini"):
        input("Configuration file not found. Make sure config.ini is present in the same directory as this file.")
        return
    try:
        indexlist = [int(x) for x in config["Basic"]["IndexList"].split(",")]
        newdelimiter = config["Basic"]["NewDelimiter"]
        delimiters = config["Basic"]["FilenameDelimiters"]
        renamefolder = config["Advanced"]["RenameFolder"]
    except Exception as err:
        print("Configuration file error. Make sure config.ini is formatted correctly.")
        raise(err)
        return

    ### Generate list of file names ###
    continueoperation = False
    finalnames = []
    for startname in os.listdir(renamefolder):  # Iterates through files within the renamefolder directory
        if os.path.isdir(renamefolder + "\\" + startname): continue  # If it finds a directory instead of a file, skip it
        filesfound = True
        namelist = split(delimiters, startname)  # Splits filename by delimiters
        namelist += split("[.]", namelist.pop(-1))  # Splits file extension
        for x in indexlist:  # Moves through index, adding each section to the file name
            try: finalname = finalname + newdelimiter + (namelist[x])  # Sections are separated by the new delimiter
            except NameError: finalname = namelist[x]  # When it's the first part of the filename, don't precede it with a delimiter
            except IndexError as err:
                print("\nError: " + str(err))
                print("You probably put number in indexlist that is higher than the number of sections in the file name.")
                input("\nOperation Cancelled")
                return
        finalname = finalname + "." + namelist[-1]  # Replace file extension at end 
        if not continueoperation:
            print("\nThe first file will be renamed from:\n" + startname + " to " + finalname)  # Make sure that the filename looks correct before continuing
            print("Are you sure you want to rename all files according to this format? ('y' to continue, anything else to not)")
            if input("> ").lower() == "y":
                print("")
                continueoperation = True
            else:
                input("\nOperation Cancelled")
                return
        finalnames.append(finalname)  # Add the generated final name to a list of final names (renaming will be done later)
        del finalname  # delete finalname variable before moving to new file so that the earlier NameError will trigger

    ### Execute rename operation ###
    ignoreerrors = False
    countindex = 0
    for startname in os.listdir(renamefolder):
        if os.path.isdir(renamefolder + "\\" + startname): continue  # If it finds a directory, skip it
        print("Renaming " + startname + " to " + finalnames[countindex] + " - ", end='')
        try:
            os.rename(renamefolder + "\\" + startname, renamefolder + "\\" + finalnames[countindex])  # Rename operation
            print("Success")
        except FileExistsError:
            print("Error: file with that name already exists. (File not renamed)")
            if not ignoreerrors:
                try:  # If this is the last file then don't ask the user if they want to continue
                    finalnames[countindex + 1]
                    print("Do you want to continue renaming other files? ('y' to continue, anything else to not)")
                    if input("> ").lower() == "y": ignoreerrors = True
                    else:
                        input("\nOperation Cancelled")
                        return
                except IndexError: pass
        countindex += 1
    try:  # Check if there were any files in renamefolder
        filesfound
        input("\nOperation Complete")
    except UnboundLocalError: input("No files found in '" + renamefolder + "' directory.")

main()
