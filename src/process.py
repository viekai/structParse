#!/usr/bin/env python

import re
import os
import commands
import sys
# index for record
NAME_INDEX = 0
FILE_INDEX = 1
TYPE_INDEX = 2
STRUCT_INDEX = 3

sourceFile = "tags"
tmpFile = "../test/outdir/tmp.dot"
graphHead = "digraph {\n\trankdir=LR;\n\t" 

commandList = ["ctags --version", "dot -V"]

def checkEvn():
    for pcommand in commandList:
        (status, output) = commands.getstatusoutput(pcommand)
        if status != 0:
            print ("please apt-get " + pcommand + ",status is " + str(status))
            return False

    if os.path.exists("tags") == False :
        if len(sys.argv) != 2 or os.path.exists(sys.argv[1]) == False:
            print "No tags find, please exec ctags -R"
            return False

    return True
    
def readFile(path = ""):
    if path == "":
        print "NUll path, exit"
        return NULL

    print path
    pf = open(path)
    p = re.compile('\/\^.*\$\/;"')
    lines = {}
    for line in pf.readlines():
        line =  p.sub("", line)
        word = line.split()
        regex = ur"^.*\.[cChH]$"
        if word[FILE_INDEX][0] == "!" or re.search(regex, word[FILE_INDEX]) == None:
            continue
        if lines.has_key(word[FILE_INDEX]) == False:
            lines[word[FILE_INDEX]] = []
        lines[word[FILE_INDEX]].append(line)
    pf.close()

    return lines 
        

def buildNode(lines):
    hashNode = {}

    if 0:
        for flist in lines.keys():
            if hashNode.has_key(flist) == False:
                hashNode[flist] = {}
            for line in lines[flist]:
                words = line.split()
                fileName = words[FILE_INDEX]
                fileType = words[TYPE_INDEX]
                valueName = words[NAME_INDEX]
                if fileType == "s":
                    hashNode[fileName][valueName] = [];

    for flist in lines.keys():
        if hashNode.has_key(flist) == False:
            hashNode[flist] = {}
        for line in lines[flist]:
            words = line.split()
            fileName = words[FILE_INDEX]
            fileType = words[TYPE_INDEX]
            valueName = words[NAME_INDEX]
            if fileType == "m":
                nodeName = words[STRUCT_INDEX][7:]
                if hashNode[fileName].has_key(nodeName) == False:
                    hashNode[fileName][nodeName] = []
                hashNode[fileName][nodeName].append(valueName)

    return hashNode 

           
def createDot(hashNode):
    for file_key in hashNode.keys():
        pf = open("tmp.dot","w")
        graph_data = ""
        node = hashNode[file_key]
        if len(node.keys()) == 0:
            continue;

        graph_data = graphHead
        for node_key in node.keys():
            member = node[node_key]
            graph_data = graph_data + node_key + "[shape=record, label=\"" + "#" + node_key + "|"
            i = 0 
            for mem in member:
               label = "<v" + str(i) + ">"
               i = i + 1
               graph_data = graph_data + label + mem + "|";
            graph_data = graph_data[:-1] + "\"" + "];\n\t"

        graph_data = graph_data[:-1] + "}"
        pf.write(graph_data)
        pf.close()
        command = "dot -Tjpg tmp.dot -o ../test/outdir/" + file_key[:-2]
        os.system(command)
        os.system("rm tmp.dot -rf")
    return

if __name__ == "__main__":
    if checkEvn() == False:
       sys.exit(0)

    if len(sys.argv) == 2:
        sourceFile = sys.argv[-1]

    ret = readFile(sourceFile)
    hashNode = buildNode(ret)
    createDot(hashNode)



