#This script helps you to get out orphans elements after selections
#Copy this inside of the train/valid forder and run python3 moveOrphans.py
#It will create folder 'orphans' with all elements that are not a .jpg file, or .jpg files without his corresponding .txt file


import os

dirName = 'orphans'
if not os.path.exists(dirName):
    os.mkdir(dirName)


def getout(filename):
    final = 'orphans/' + filename
    os.rename(filename, final)

    #in case of .jpeg, labelImage can create a .txt file, but not sure about darknet support it...
    filenametxt=os.path.splitext(filename)[0]+'.txt'
    if os.path.exists(filenametxt):
        finaltxt = 'orphans/' + filenametxt
        os.rename(filenametxt, finaltxt)


dir = sorted(os.listdir(os.getcwd()))
for file in dir:
    if not file == 'orphans' and \
            not file.lower().endswith('.txt') and \
            not file.lower().endswith('.jpg') and \
            file != 'moveOrphan.py':

        getout(file)

    elif file.lower().endswith('.jpg'):
        # search for his .txt
        filetxt = os.path.splitext(file)[0] + '.txt'
        if not os.path.exists(filetxt):
            getout(file)

