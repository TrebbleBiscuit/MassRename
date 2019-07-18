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
        self.ignoreerrors = False
        self.continueoperation = False
        self.startnames = []
        self.finalnames = []
        self.directorynames = [self.renamefolder]
        os.system('cls' if os.name == 'nt' else 'clear')

    def genfilename(self, renamefolder):    ### Generate list of file names ###  
        for startname in os.listdir(renamefolder):  # Iterates through files within the renamefolder directory
            if os.path.isdir(renamefolder + "\\" + startname):  # If it finds a directory instead of a file:
                self.directorynames.append(renamefolder + "\\" + startname)  # Add that directory to a list
                continue  # and then move on to the next item
            namelist = split(self.delimiters, startname)  # Splits filename by delimiters
            namelist += split("[.]", namelist.pop(-1))  # Splits file extension
            fileext = namelist.pop(-1)  # Removes file extension from list, store it seperately
            for x in self.indexlist:  # Moves through index, adding each section to the file name
                try: finalname = finalname + self.newdelimiter + (namelist[x])  # Sections are separated by the new delimiter
                except NameError: finalname = namelist[x]  # When it's the first part of the filename, don't precede it with a delimiter
                except IndexError as err:
                    print("\nError: " + str(err))
                    print("You probably put a number in IndexList that is higher than the number of sections in the file name.")
                    print("Run the helper file for help creating an appropriate IndexList.")
                    input("\nOperation Cancelled")
                    return False
            finalname = finalname + "." + fileext  # Replace file extension at end 
            if not self.continueoperation:
                print("The first file will be renamed from:\n" + startname + " to " + finalname)  # Make sure that the filename looks correct before continuing
                print("Are you sure you want to rename all files according to this format?")
                print("('y' to continue, anything else to not)")
                if input("> ").lower() == "y":
                    print("")
                    self.continueoperation = True
                else:
                    input("\nOperation Cancelled")
                    return False
            self.startnames.append(renamefolder + "\\" + startname)  # Add the original name to a list of original names
            self.finalnames.append(renamefolder + "\\" + finalname)  # Add the generated final name to a list of final names
            del finalname  # delete finalname variable before moving to new file so that the earlier NameError will trigger
        return True

    def rename(self, renamefolder):    ### Execute rename operation ### 
        if self.finalnames == []:  # This and genfilename could probably be in the same function but it was easier to organize this way.
            input("Error: No files found in " + renamefolder + " directory.")
            return
        assert len(self.startnames) == len(self.finalnames)  # DEBUG: Makes sure that these two lists are of equal length
        for x in range(len(self.startnames)):
            print('Renaming "' + self.startnames[x] + '" to "' + self.finalnames[x] + '" - "', end='')
            try:
                os.rename(self.startnames[x], self.finalnames[x])  # Rename operation
                print("Success")
            except FileExistsError:
                print("Error: file with that name already exists. (File not renamed)")
                if not self.ignoreerrors:
                    try:  # If this is the last file then don't ask the user if they want to continue
                        self.finalnames[x + 1]  # TODO: This could just be done with a simple len() check
                        print("Do you want to continue renaming other files? ('y' to continue, anything else to not)")
                        if input("> ").lower() == "y": self.ignoreerrors = True
                        else:
                            input("\nOperation Cancelled")
                            return
                    except IndexError: pass

    def main(self): 
        for dirname in self.directorynames:
            if self.genfilename(dirname):
                self.rename(dirname)
                self.startnames = []
                self.finalnames = []
        input("\nOperation Complete")

if __name__ == "__main__":
    renameobject = Renamer()
    renameobject.main()
