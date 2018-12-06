import pycuda.driver as cuda
import pycuda.autoinit
import pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule
import numpy
import os
import time
import shutil
import math

CLASS_OF_FILE = 0
WEEK_OF_FILE = 1
FILE_EXT_OF_FILE = 3
NAME_OF_FILE = 2

classes = ""
filetypes = []
weeks = []
testDir = "C:\\Workdir\\SeniorYear\\Fall Semester\\Parallel Computing\\FinalProject\\Base_Dir\\Test_Dir"
finalTestDir = "C:\\Workdir\\SeniorYear\\Fall Semester\\Parallel Computing\\FinalProject\\Base_Dir\\Final_Test_Dir"
fileSubstrings = []
lengths = []


def GetFilenames():
    filenames = []

    for root, dirs, files in os.walk(testDir):
        for filename in files:
            filenames.append(str(filename))
            lengths.append(len(filename))
    return filenames


def main():
    start_time = time.time()
    list_of_filenames = GetFilenames()
    string_list_lines = numpy.array(list_of_filenames, dtype=str)
    length = numpy.array(lengths, dtype=int)

    threadsPerBlock = len(string_list_lines)
    if (threadsPerBlock > 1024):
        threadsPerBlock = 1024

    # Define amount of blocks
    blocks = math.ceil(len(string_list_lines))

    # Allocalte mem  to list of strings on the GPU device
    string_list_linesGPU = gpuarray.to_gpu(string_list_lines)
    d_length = gpuarray.to_gpu(length)
    destination_strings = ["            ", "            ", "            ",
                           "            ", "            ", "            ", "            ", "            "]
    destination_strings2 = ["     ", "     ", "     ",
                            "     ", "     ", "     ", "     ", "     ", "     ", "     ", "     ", "     ", "     ", "     ", "     "]

    classGPU = numpy.array(destination_strings, dtype=str)
    d_classGPU = gpuarray.to_gpu(classGPU)
    weekGPU = numpy.array(destination_strings2, dtype=str)
    d_weekGPU = gpuarray.to_gpu(weekGPU)

    # Kernel Function to determine classes, weeks
    DetermineFileCharacteristics = SourceModule("""
        # include <stdio.h>
        # include <string.h>
        __global__ void DetermineCharacteristics(char* File, char* length, char* className, char* week)
        {
            // Define variables and counters for the kernel to use
            int idx = blockIdx.x * blockDim.x + threadIdx.x;
            int stringCounter = 0;
            char* str = new char[*length];
            int i = 0;
            bool isClass = true;

            // Iterate through the string in order to find the file's characteristics
            for(int j=0; j < (*length)*4; j = j+4) {
                
                if (File[j] == '_')
                { 
                    while (stringCounter < j)
                    {
                        str[i] = File[stringCounter];
                        if (isClass)
                        {
                            className[stringCounter] = str[i];
                        }
                        else
                        {
                            week[stringCounter] = str[i];
                        }
                        i++;
                        stringCounter += 4;
                    }
                    stringCounter += 4;
                    isClass = false;
                    
                }
                
            }
        }
        """)

    gpusin = DetermineFileCharacteristics.get_function(
        "DetermineCharacteristics")
    gpusin(string_list_linesGPU.gpudata, d_length.gpudata, d_classGPU.gpudata, d_weekGPU.gpudata, grid=(blocks, 1),
           block=(threadsPerBlock, 1, 1))
    classes = (d_classGPU.get()).tolist()
    weeks = (d_weekGPU.get()).tolist()

    for currentClass in classes:
        currentClass = currentClass.replace(' ', '')
        classDir = finalTestDir + "\\" + currentClass
        if not os.path.isdir(classDir):
            os.mkdir(classDir)

        for week in weeks:

            week = week.replace(' ', '')
            weekDir = classDir + "\\" + week
            if not os.path.isdir(weekDir):
                os.mkdir(weekDir)

            for classFile in GetFilenames():
                if (currentClass in classFile) and (week in classFile):
                    for root, dirs, files in os.walk(testDir):
                        if (classFile in files):
                            oldFileLocation = str(
                                root) + "\\" + classFile
                            newFileLocation = weekDir + "\\" + classFile
                            shutil.move(oldFileLocation, newFileLocation)
                        else:
                            print("No files found")

    print("--- Time to move files and complete directory: %s seconds ---" %
          (time.time() - start_time))


main()
