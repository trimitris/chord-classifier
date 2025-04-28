import sys
import subprocess

def sendFrames(frames):
    for frame in frames:
        print("<frame>")
        for sample in frame:
            print(sample[0],sample[1])
        print("</frame>")

def sendFramesSub(frames, popenObj):
    """
    writes the frames information to a subprocess's stdin
    """
    for frame in frames:
        popenObj.communicate( input=b"<frame>\n") # Might have to include "\n" at the end
        # for sample in frame:
        #     popenObj.communicate(input=str(sample[0] + " " + sample[1]))
        # popenObj.communicate(input="</frame>\n")

def readStdinUpTo(endTag, pipeline = sys.stdin):
    """
    returns the data from stdin (or a pipeline) in a list of strings (for each line), until the </endTag> is received
    """
    if (type(endTag) != str):
        raise ValueError("endTag should be a string")

    data = []
    for line in pipeline:
        line = line[:-1] #get rid of the \n character
        # Check for end of transmission
        if (line == str("</" + endTag + ">")):
            break
        data.append(line)
    return data

def listener(tag, pipeline = sys.stdin):
    """
    Used for interfacing with (or a pipeline) stdin and data transfer via stdin (or a pipeline). It stores data between an
    opening <tag> and closing </tag> into a data structure
    """
    data = []
    for line in pipeline:
        line = line[:-1]
        if (line == str("<" + tag + ">")):
            dataFragment = readStdinUpTo(tag, pipeline)
            data.append(dataFragment)
    return data

# Publish directory used by the analyseDirectory() in the src files
# directory = "../custom_recs/textfiles/"
# print(directory)
