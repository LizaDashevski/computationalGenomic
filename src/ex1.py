import argparse
from random import choice
import timeit
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


def genRandSeq(len):
    # random sequence of the input length
    seq = ""
    for i in range(len):
        seq += choice("ATCG")
    return seq

# ----------------------- construct suffix-tree --------------------------

def buildTrees(seqList):
    # Build suffix tree for all sequence
    trees = []
    for s in seqList:
        trees.append(constructSuffixTree(s))
    return trees

def constructSuffixTree(seq):
    # This function builds a suffix tree out of a given string
    suffixTree = []
    seqLen = len(seq)
    suffixTree.append(('R', []))
    for i in range(0 , seqLen):
        suffixTree.append(None)
    for pos in range(seqLen):
        addNode(suffixTree,seq[pos:], pos + 1)
    return suffixTree

def addNode(suffixTree , seq , position):
    #Add a new string node to suffix tree
    tempStr = seq
    node = suffixTree[0]
    isChanged = True
    while len(node[1]) != 0 and isChanged and len(tempStr) != 0 :
        isChanged = False
        children = node[1]
        for child in children:
            childprefix = suffixTree[child][0]
            if childprefix[0] == tempStr[0]:
                if tempStr.startswith(childprefix):
                    node = suffixTree[child]
                    tempStr = tempStr[len(node[0]):]
                    isChanged = True
                    break
                else:
                    common = tempStr
                    for pos in range(min(len(tempStr), len(childprefix))):
                        if tempStr[pos] != childprefix[pos]:
                            common = tempStr[:pos]
                            tempStr = tempStr[pos:]
                            break
                    bNode = (common, [])
                    suffixTree.append(bNode)
                    suffixTree[child] = (childprefix[len(common):], suffixTree[child][1])
                    node[1].remove(child)
                    node[1].append(len(suffixTree) - 1)
                    bNode[1].append(child)

                    node = suffixTree[len(suffixTree) - 1]
                    isChanged = False
                    break
    if not isChanged or seq == tempStr:
        newNode = (tempStr + "$", [])
        suffixTree[position] = newNode
        node[1].append(position)

# ----------------------- Question 1 --------------------------

def qOne():
    r = [10,50,100,200,500,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000 ]
    times = []
    for length in r:
        seq = genRandSeq(length)
        times.append(timeit.timeit('constructSuffixTree(seq)', setup='from __main__ import constructSuffixTree; seq = "'+ seq + '"', number=100) / 100)
    # plot
    plt.scatter(r, times)
    plt.ylabel("time in sec")
    plt.xlabel("seq len")
    plt.title("Suffix tree construction time vs seq length and polynomial fit for deg=2")

    plt.xticks([i for i in range(0,10000, 1000)])
    plt.xlim(0,max(r))
    plt.ylim(0, max(times))

    # get the fit with deg 2
    fit = np.polyfit(r, times, 2)
    times.sort()
    r.sort()
    plt.text(r[2], times[-2], "y = " + str(fit[0]) + "x^2 \n+ (" + str(fit[1]) + ")x + " + "(" +
             str(fit[2]) + ")", horizontalalignment='left', verticalalignment='top', size = 'smaller')

    plt.plot(r, np.poly1d(fit)(r))
    plt.savefig("fig")

    # get 15000 estimation vs actual values
    seq = genRandSeq(15000)
    print("estimated val:" + str(np.polyval(fit, 15000)))

    print("actual val: " + str(timeit.timeit('constructSuffixTree(seq)', setup='from __main__ import constructSuffixTree; seq = "'
                                                 + seq + '"', number=100) / 100))

# ----------------------- Question 2 --------------------------


# ----------------------- main --------------------------

def main():
    qOne()




if __name__ == '__main__':
    main()