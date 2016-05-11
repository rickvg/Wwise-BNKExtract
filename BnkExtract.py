from struct import *
import os
import binascii
import sys

if len(sys.argv) > 1:
    print("Opening file... This may take a while depending on the size.")
    if os.path.isfile(sys.argv[1]):
        file = open(sys.argv[1], "rb")
        arrHeader = []
        # Header Info
        arrHeader.append(unpack("<I", file.read(4))[0])  # magicNumber
        arrHeader.append(unpack("<I", file.read(4))[0])  # headerLength
        arrHeader.append(unpack("<I", file.read(4))[0])  # version
        arrHeader.append(unpack("<I", file.read(4))[0])  # soundbankid
        print(arrHeader[2])

        currentPos = 8
        while (currentPos < arrHeader[1]):
            arrHeader.append(unpack("<I", file.read(4))[0])  # Unknown
            currentPos = currentPos + 4

        arrDIDX = []
        # DIDX Header
        arrDIDX.append(unpack("<I", file.read(4))[0])  # magicNumber
        arrDIDX.append(unpack("<I", file.read(4))[0])  # chunkLength

        arrWEMFileDef = []
        if arrDIDX[1] > 0:
            intWemCount = int(arrDIDX[1] / 12)
            for i in range(0, intWemCount):
                arrWEMFileDef.append([])
                arrWEMFileDef[i].append([file.tell(), unpack("<I", file.read(4))[0]])  # fileID
                arrWEMFileDef[i].append([file.tell(), unpack("<I", file.read(4))[0]])  # offsetData
                arrWEMFileDef[i].append([file.tell(), unpack("<I", file.read(4))[0]])  # fileLength

        arrDATA = []
        # DATA Header
        arrDATA.append(unpack("<I", file.read(4))[0])  # magicNumber
        dataChunkLenPos = file.tell()
        arrDATA.append(unpack("<I", file.read(4))[0])  # chunkLength

        currentPos = file.tell()

        intChoice = 0
        while intChoice != 1 or intChoice != 2:
            intChoice = int(input("Choose from options:\n1. Extract sounds from a bank\n2. Replace files in a bank\n3. Exit\n"))
            if intChoice == 1:
                print("\nExtracting files from " + sys.argv[1] + "...\n")
                arrWEMFILES = []
                arrWEMFILES.append(file.read(arrWEMFileDef[0][2][1]))

                for i in range(1, intWemCount):
                    file.seek(currentPos + arrWEMFileDef[i][1][1])
                    arrWEMFILES.append(file.read(arrWEMFileDef[i][2][1]))

                for i in range(0, len(arrWEMFILES)):
                    strFileName = str(arrWEMFileDef[i][0][1]) + ".wem"
                    f = open(strFileName, "wb")
                    f.write(arrWEMFILES[i])
                    f.close()
            elif intChoice == 2:
                print("\nThis option will be introduced soon. This way you will be able to replace WEM files in a WWiSe Audio Bank.\n")

            elif intChoice == 3:
                break
            else:
                print("Wrong choice. Try again.\n")

        file.close()
    else:
        print("\nError while opening file. This file might not exist.\nUsage instructions: python WEMExtract.py [path + name of file]\n")
else:
    print("Usage instructions: python WEMExtract.py [path + name of file]\n")

