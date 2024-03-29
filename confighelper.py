# Author - Erik Nielsen
#
# This program is intended to help the user create an appropriate IndexList for config.ini

import os               # Used to get the file names and rename them
from re import split    # Used for spliting a string by multiple delimiters
import configparser     # Used for parsing config.ini

def readconfig():
    config = configparser.ConfigParser()
    config.read("config.ini")
    print("Importing configuration file...")
    if not os.path.isfile("config.ini"):
        input("Configuration file not found. Make sure config.ini is present in the same directory as this file.")
        return
    try:
        indexlist = [int(x) for x in config["Basic"]["IndexList"].split(",")]
        newdelimiter = config["Basic"]["NewDelimiter"]
        delimiters = config["Basic"]["FilenameDelimiters"]
        renamefolder = config["Advanced"]["RenameFolder"]
    except Exception as err:
        print("Configuration file error: " + err)
        print("Make sure config.ini is formatted correctly before running this helper.")
        input("If you're not sure how, use the default values.")
        raise(err)
    if not os.path.isdir(renamefolder):
        print('"' + renamefolder + '" folder not found.')
        print('Create a folder called "' + renamefolder + '" in the same directory as this file, then run ')
        input('this helper again. You may choose a different folder name in config.ini\n')
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    return indexlist, newdelimiter, delimiters, renamefolder

def helper():
    try: indexlist, newdelimiter, delimiters, renamefolder = readconfig()
    except TypeError: return
    print("This file is intended to help you create an appropriate IndexList in config.ini")
    print('Place an example file you would like to rename in the "' + renamefolder + '" folder, ')
    input("then press enter.\n")
    for startname in os.listdir(renamefolder):  # Iterates through files within the renamefolder directory
        if os.path.isdir(renamefolder + "\\" + startname): continue  # If it finds a directory instead of a file, skip it
        break  # When it does find a file, break out of the loop
    else:
        print("No files found in the " + renamefolder + " folder.")
        print("Place a file there and run this program again.")
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    print("The example file we will look at is \"" + startname + '"\n')
    print("This file will be separated into sections by the delimiters defined in the ")
    print("configuration file.")
    input("Press enter to see how the file is separated.\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    namelist = split(delimiters, startname)  # Splits filename by delimiters
    namelist += split("[.]", namelist.pop(-1))  # Splits file extension
    fileext = namelist.pop(-1)  # Removes file extension from list
    for x in range(len(namelist)):
        print("Index " + str(x) + ' is: "' + namelist[x] + '"')
    print("\nNow we will test out an IndexList that you will create.")
    print("Type in several integers separated by commas in the order that you want them.")
    print("Each integer corresponds to the index value listed above.")
    letscontinue = False
    while not letscontinue:
        includednegative = False
        try: del finalname
        except NameError: pass
        userinput = input("> ")
        if userinput == "": continue
        try:indexlist = [int(x) for x in userinput.split(",")]
        except ValueError:
            print("Remember to only use integers separated by commas.")
            continue
        for x in range(len(indexlist)):
            try: finalname = finalname + newdelimiter + (namelist[indexlist[x]])  # Sections are separated by the new delimiter
            except NameError:
                try: finalname = namelist[indexlist[x]]  # When it's the first part of the filename, don't precede it with a delimiter
                except IndexError:
                    print("You put a number in your list that is higher than the number of sections in the file name. Try again.")
                    break
            except IndexError:
                print("You put a number in your list that is higher than the number of sections in the file name. Try again.")
                break
            if indexlist[x]<0: 
                includednegative = True
            if x == len(indexlist)-1:  # If you made it to the last entry in the list without any errors
                letscontinue = True
    if includednegative:
        print("\nYou included a negative value in your index list.")
        print("Negative values work backwords, so -1 for example would give you the section nearest the end of the filename.")
        input("There's no problem with that, just make sure that you know what you're doing. \n")
    if len(indexlist) != len(set(indexlist)):
        print("\nYou have a duplicate value in your index list.")
        print("This means that the same information will show up twice in the filename.")
        input("There's no problem with that, just make sure that you know what you're doing. \n")
    for x in range(len(namelist)):
        if x not in indexlist:
            print("\nYou didn't include every index in your index list.")
            print("This means that there will be some information removed from the file name.")
            input("There's no problem with that, just make sure that you know what you're doing. \n")
            break
    finalname = finalname + "." + fileext  # Replace file extension at end
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\nGreat! You entered a valid index list.\n")
    print("If you ran your test file \"" + startname + '" through the renamer with ')
    print("that index list, it would be renamed:")
    print("\n" + finalname + "\n")
    print("If you want the delimiter between sections to be different, you can edit ")
    print("NewDelimiter in config.ini")
    print("If you're happy with the way the example file was renamed, then the line ")
    print("in config.ini file should read:\n")
    print("IndexList: " + ', '.join(map(str, indexlist)))
    print("Is that what you want? ('y' for yes, anything else for no)\n")
    if input("> ").lower() == "y":
        input("\nGreat! Now you're ready to edit config.ini and then run rename.py")
    else:
        input("\nIf that's not what you want, then re-run this helper file to try again.")

helper()
