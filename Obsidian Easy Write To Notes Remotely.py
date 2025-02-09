#-------------Obsidian: Easy Write To Notes Remotely------------#
# Author: Adrian Papineau
# Date created: November 12th, 2021

from datetime import date
import time
import glob, os

ObsidianVaultFolder = ""    # Example :"C:/Users/User/Documents/ObsidianVault/VaultName"
DailyNotesFolder = ""       # Example :"C:/Users/User/Documents/ObsidianVault/VaultName/DailyNotes"
print(DailyNotesFolder)
today = date.today()

#return current daily note file path
def CurrentDate(): 
    dateExtractMonth = today.strftime('%B')
    dateExtractDay = today.strftime('%d')
    dateExtractYear = today.strftime('%Y')
    # Get rid of the beginning 0 in day of the month. 
    if dateExtractDay[0] == "0":
        dateExtractDay = dateExtractDay[-1]
    # Add the "th" or similar
    if ((int(dateExtractDay) >= 10) and (int(dateExtractDay) <20)) or (dateExtractDay[-1] == "0") or ((int(dateExtractDay[-1]) >=4) and (int(dateExtractDay[-1]) <10)):       
        dateExtractNUM = str(dateExtractDay + "th")
    elif dateExtractDay[-1] == "1":       
        dateExtractNUM = str(dateExtractDay + "st")
    elif dateExtractDay[-1] == "2":       
        dateExtractNUM = str(dateExtractDay + "nd")
    elif dateExtractDay[-1] == "3":       
        dateExtractNUM = str(dateExtractDay + "rd")
    RoamFormat = str(dateExtractMonth + " " + dateExtractNUM + ", " + dateExtractYear)
    return RoamFormat
print(CurrentDate())

def CurrentDailyNote():
    DailyNoteName = (CurrentDate() + ".md")
    DailyNotePath = DailyNotesFolder + "/" + DailyNoteName
    return DailyNotePath
print(CurrentDailyNote())

# search the daily note
def FindLinkContent():
    try:
        searchfile = open(CurrentDailyNote(), "r", encoding="utf8")
        EntireFile = searchfile.read() 
        searchfile.close() 
        if ">[[" in EntireFile:
            indexStart = (EntireFile.index(">[["))
            #print(indexStart)
            everythingAfter = EntireFile[indexStart:]
            #print(everythingAfter)
            if "]]" in everythingAfter:
                RelIndexClosing = everythingAfter.index("]]")
                indexClosing = indexStart +RelIndexClosing
                LinkContent = EntireFile[(indexStart+3):indexClosing]   
                if "[[" in LinkContent:
                    print("another link")
                else:
                    return(LinkContent)
            
    except ValueError:
        print('ERROR FindLinkContent()')

def RemoveAlias():
    RawLinkName = str(FindLinkContent())
    if "|" in RawLinkName:
        BaseName = RawLinkName.split('|')[0]
        return(BaseName)
    else:
        return(RawLinkName)

def RemoveSymbol():
    try:
        searchfile = open(CurrentDailyNote(), "r", encoding="utf8")
        EntireFile = searchfile.read()
        searchfile.close()
        if ">[[" in EntireFile:
            searchfile = open(CurrentDailyNote(), encoding="utf8")
            SearchContent = searchfile.read()
            searchfile.seek(0)
            searchfile = open(CurrentDailyNote(), "w", encoding="utf8")   
            FixedFile = EntireFile.replace(">[[","[[")
            searchfile.write(FixedFile)
            searchfile.seek(0)
            searchfile.close()
    except ValueError:
        print('ERROR RemoveSymbol()')

# Return the path of the note that is linked
def NotePath():
    LinkName = (RemoveAlias() + ".md")
    LinkNotePath = ObsidianVaultFolder + "/" + LinkName
    return(LinkNotePath)
 
def Block():
    searchfile = open(CurrentDailyNote(), "r", encoding="utf8")
    EntireFile = searchfile.read()
    indexStart = (EntireFile.index(">[["))
    everythingBefore = EntireFile[:indexStart]
    RelIndexBullet = everythingBefore[::-1].index("\n")
    #RelIndexBullet = everythingBefore[::-1].index("- ")
    indexBullet = indexStart - RelIndexBullet
    BlockContent = EntireFile[(indexBullet+1):indexStart]
    return(BlockContent)
    searchfile.close()
  
# Paste the block from daily notes into the linked note
def AppendToNote(desiredBlock):
    Notefile = open(NotePath(), encoding="utf8")
    NoteContent = Notefile.read()
    Notefile.seek(0)
    Notefile = open(NotePath(), "w", encoding="utf8")
    Notefile.write(NoteContent + "\n" + "-" + desiredBlock + "[[" + CurrentDate() + "]]")
    Notefile.seek(0)
    Notefile.close()
 
while True:
    if FindLinkContent() != None:
        os.chdir(ObsidianVaultFolder)
        for file in glob.glob(RemoveAlias() + ".md"):
            print(FindLinkContent())
            time.sleep(1)
            AppendToNote(Block())
            RemoveSymbol()
        time.sleep(1)

