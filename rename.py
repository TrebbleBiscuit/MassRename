# Author - Erik Nielsen
# 
# This program is used to rename files that have sections in their file names (separated by delimiters) that need to be rearranged.
# It works by separating the existing file name (by delimiters) into several sections, then
# puts the sections back in a user defined order, separating them by a user defined delimiter.

import os               # Used to get and rename file names, and to clear the screen
from re import split    # Used for spliting a string by multiple delimiters
import configparser     # Used for parsing config.ini

class Renamer():

    def __init__(self):  # Sets configuration file variables
        config = configparser.ConfigParser()
        config.read("config.ini")
        print("Importing configuration file...")
        if not os.path.isfile("config.ini"):
            input("Configuration file not found. Make sure config.ini is present in the same directory as this file.")
            raise Exception
        try:
            self.indexlist = [int(x) for x in config["Basic"]["IndexList"].split(",")]
            self.newdelimiter = config["Basic"]["NewDelimiter"]
            self.delimiters = config["Basic"]["FilenameDelimiters"]
            self.renamefolder = config["Advanced"]["RenameFolder"]
        except Exception as err:
            print("Configuration file error: " + err)
            print("Make sure config.ini is formatted correctly before running this helper.")
            input("If you're not sure how, use the default values.")
            raise(err)
        if not os.path.isdir(self.renamefolder):
            print('"' + self.renamefolder + '" folder not found.')
            print('Create a folder called "' + self.renamefolder + '" in the same directory as this file, then run ')
            input('this helper again. You may choose a different folder name in config.ini\n')
            raise Exception
        os.system('cls' if os.name == 'nt' else 'clear')

    def genfilename(self):    ### Generate list of file names ###  
        continueoperation = False
        filesfound = False
        finalnames = []
        for startname in os.listdir(self.renamefolder):  # Iterates through files within the renamefolder directory
            if os.path.isdir(self.renamefolder + "\\" + startname):
                continue  # If it finds a directory instead of a file, skip it
            filesfound = True
            namelist = split(self.delimiters, startname)  # Splits filename by delimiters
            namelist += split("[.]", namelist.pop(-1))  # Splits file extension
            fileext = namelist.pop(-1)  # Removes file extension from list
            for x in self.indexlist:  # Moves through index, adding each section to the file name
                try: finalname = finalname + self.newdelimiter + (namelist[x])  # Sections are separated by the new delimiter
                except NameError: finalname = namelist[x]  # When it's the first part of the filename, don't precede it with a delimiter
                except IndexError as err:
                    print("\nError: " + str(err))
                    print("You probably put number in indexlist that is higher than the number of sections in the file name.")
                    input("\nOperation Cancelled")
                    return
            finalname = finalname + "." + fileext  # Replace file extension at end 
            if not continueoperation:
                print("The first file will be renamed from:\n" + startname + " to " + finalname)  # Make sure that the filename looks correct before continuing
                print("Are you sure you want to rename all files according to this format?")
                print("('y' to continue, anything else to not)")
                if input("> ").lower() == "y":
                    print("")
                    continueoperation = True
                else:
                    input("\nOperation Cancelled")
                    return
            finalnames.append(finalname)  # Add the generated final name to a list of final names (renaming will be done later)
            del finalname  # delete finalname variable before moving to new file so that the earlier NameError will trigger
        if not filesfound:
            input("No files found in 'ToRename' directory.")
        return finalnames

    def rename(self, finalnames):    ### Execute rename operation ### 
        if finalnames is None: return
        elif finalnames == []: return
        ignoreerrors = False
        countindex = 0
        for startname in os.listdir(self.renamefolder):
            if os.path.isdir(self.renamefolder + "\\" + startname): continue  # If it finds a directory, skip it
            print("Renaming " + startname + " to " + finalnames[countindex] + " - ", end='')
            try:
                os.rename(self.renamefolder + "\\" + startname, self.renamefolder + "\\" + finalnames[countindex])  # Rename operation
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
        input("\nOperation Complete")

    def main(self): 
        self.rename(self.genfilename())

if __name__ == "__main__":
    renameobject = Renamer()
    renameobject.main()
