#!/usr/bin/python
import re
import sys
import os

#path ="C:\\Projects\\tt"
path ="C:\\Projects\\tt"
globalFileList = []

# Below variable holds file path of comments removed all files list
listOfRemovedCommentsFiles = path + "\\" + "CommentsRemListFile" + ".txt"

filesUpdatedCount = 0


def commentRemover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/' ):
            return " "# note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def GetListOfAllFiles():
    for root, dirs, files in os.walk(path):
        for file in files:
            if(file.endswith(".cpp") or file.endswith(".H") or file.endswith(".c")): #specify file types to update here
                globalFileList.append(os.path.join(root,file))
        #file_name = name.split("\\")[-1] # This will return only file name from path
        #oPath = '\\'.join(name.split('\\')[0:-1]) # This will return only path excluding file name which is present at last
    
def main():
    GetListOfAllFiles()
    global filesUpdatedCount #use global variable
    tempFile = "TempFile_"
    for fileName in globalFileList:
        oPath = '\\'.join(fileName.split('\\')[0:-1])
        file_name = fileName.split("\\")[-1]
        with open ( oPath + "\\" + tempFile + file_name, 'w') as tempFileHandle:
            with open(fileName, 'r') as fileHandle:
                uncmtFile = commentRemover(fileHandle.read())
                fileHandle.seek(0) # This will over write the existing same file.
                lines = uncmtFile.splitlines()
                for line in lines :
                    if ( line.isspace() ) or line == " ":
                        aa = 0# just printing nothing TO Do
                    else:
                        tempFileHandle.write(line + "\n")
            fileHandle.close()
        tempFileHandle.close()
        os.chmod(fileName, 0o777)# added this because I was getting permission error while remove
        os.remove(fileName)
        os.chmod(oPath + "\\" + tempFile + file_name, 0o777)# added this because I was getting permission error while remove
        os.rename(oPath + "\\" + tempFile + file_name, fileName)
        filesUpdatedCount +=1

if __name__ == '__main__':
    print("Removing comments from all files..")
    main()
    print("Comments Removed Files List at location :" + listOfRemovedCommentsFiles)
    print("Processed " + str(filesUpdatedCount) + "files ..")
    with open ( listOfRemovedCommentsFiles, 'w') as resultFileHandle:
        for fileName in globalFileList:
            resultFileHandle.write(fileName + "\n")
    resultFileHandle.close()
