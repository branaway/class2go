import sys
import os

import math
import operator
import Image            # this is PIL

def createManifest(keepList, keepIndicies, frameRate):
    outfile = "jpegs/manifest.txt"
    FILE = open(outfile, "w")
    timeBetweenFrames = 1.0/float(frameRate)
    index = 0
    FILE.write("{")
    print len(keepList)
    print len(keepIndicies)

    while(index < len(keepList)):
        FILE.write("\"")
        toWrite = str(keepIndicies[index] * timeBetweenFrames)
        FILE.write(toWrite)
        FILE.write("\":{\"imgsrc\":\"")
        FILE.write(keepList[index])
        FILE.write("\"}")
        if index < len(keepList)-1:
            FILE.write(",")
        index += 1

    FILE.write("}")


def main():
    #Set the threshold for diff from argument passed
    threshold = float(sys.argv[1])
    #Read in all the files names in jpegs folders as a list of strings
    imageList = os.listdir("./jpegs")
    imageList.sort()
    keepList = []
    keepIndicies = []
    deleteList = []
    outfile = "toDelete.txt"
    index = 0
    #The first image is always kept
    keepList.append(imageList[index])
    keepIndicies.append(0)
    #If a large enough difference is recognized between frames, the next frame is kept, otherwise it is deleted
    while index < len(imageList)-1:
    	  diff = computeDiff("./jpegs/"+imageList[index], "./jpegs/"+imageList[index+1])
    	  print diff
    	  if diff > threshold:
    	      keepList.append(imageList[index+1])
              keepIndicies.append(index+1)
    	  else:
    	      deleteList.append(imageList[index+1])
    	  index += 1

    #Write out to the list of images that should be deleted
    FILE = open(outfile, "w")
    for image in deleteList:
    	  FILE.write(image)
    	  FILE.write("\n")

    createManifest(keepList, keepIndicies, sys.argv[2])
    print keepList

# from http://mail.python.org/pipermail/image-sig/1997-March/000223.html
def computeDiff(file1, file2):
    h1 = Image.open(file1).histogram()
    h2 = Image.open(file2).histogram()
    rms = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    return rms

if __name__ == "__main__":
    main()





