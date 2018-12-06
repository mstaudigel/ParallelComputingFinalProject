import os
import shutil
import time
CLASS_OF_FILE = 0
WEEK_OF_FILE = 1
FILE_EXT_OF_FILE = 3
NAME_OF_FILE = 2

classes = []
filetypes = []
weeks = []
testDir = "C:\\Workdir\\SeniorYear\\Fall Semester\\Parallel Computing\\FinalProject\\Base_Dir\\Test_Dir"
finalTestDir = "C:\\Workdir\\SeniorYear\\Fall Semester\\Parallel Computing\\FinalProject\\Base_Dir\\Final_Test_Dir"
fileSubstrings = []


def main():
    for root, dirs, files in os.walk(testDir):
        for filename in files:
            fileName = str(filename)
            testChars = []
            testFileSubStrings = []
            n = 0

            for i in range(0, len(fileName)):
                if (fileName[i] == "_"):

                    while (n < i):
                        testChars.append(fileName[n])
                        n = n+1
                    n += 1
                    testFileSubStrings.append("".join(testChars))
                    testChars = []

            fileName, file_extension = os.path.splitext(
                testDir + str(filename))
            testFileSubStrings.append(str(filename))
            testFileSubStrings.append(str(file_extension))
            fileSubstrings.append(testFileSubStrings)

    for file in fileSubstrings:
        if (len(classes) != 0):
            if file[CLASS_OF_FILE] not in classes:
                classes.append(file[CLASS_OF_FILE])
        else:
            classes.append(file[CLASS_OF_FILE])

        if (len(weeks) != 0):
            if file[WEEK_OF_FILE] not in weeks:
                weeks.append(file[WEEK_OF_FILE])
        else:
            weeks.append(file[WEEK_OF_FILE])

        if (len(filetypes) != 0):
            if file[FILE_EXT_OF_FILE] not in filetypes:
                filetypes.append(file[FILE_EXT_OF_FILE])
        else:
            filetypes.append(file[FILE_EXT_OF_FILE])

    print("--- Time to determine directory hierarchy:  %s seconds ---" %
          (time.time() - start_time))

    for currentClass in classes:
        classDir = finalTestDir + "\\" + currentClass
        if not os.path.isdir(classDir):
            os.mkdir(classDir)

        for week in weeks:
            weekDir = classDir + "\\" + week
            if not os.path.isdir(weekDir):
                os.mkdir(weekDir)

            for classFile in fileSubstrings:
                if (currentClass in classFile) and (week in classFile):
                    for root, dirs, files in os.walk(testDir):
                        if (classFile[NAME_OF_FILE] in files):
                            oldFileLocation = str(
                                root) + "\\" + classFile[NAME_OF_FILE]
                            newFileLocation = weekDir + \
                                "\\" + classFile[NAME_OF_FILE]
                            shutil.move(oldFileLocation, newFileLocation)


start_time = time.time()
main()
print("--- Time to move files and complete directory: %s seconds ---" %
      (time.time() - start_time))
