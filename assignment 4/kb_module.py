def readPredicateFile(fileObj):

    opList = []
    varsList = []
    descList = []

    for line in fileObj:
        pred, desc = line.split(':')

        desc = " ".join(desc.split())
        descList.append(desc)
        
        op , Vars = pred.split('(')
        op = "".join(op.split())
        opList.append(op)
        
        Vars = Vars.split(')')[0]
        Vars = "".join(Vars.split())
        Vars = Vars.split(',')
        varsList.append(Vars)

    print opList
    print varsList
    print descList

    return opList, varsList, descList

def makeExecClassStrings(opList, varsList, descList):

    execClassStrings = []

    for i in range(len(opList)):
        op = opList[i]
        varr = varsList[i]
        desc = descList[i]

        strr = strr + "class " + op + ":\n\tdef __init__(self,op,*args):\n\t\tself.op=op"

        for i in range(len(varr)):
            strr = strr + "\n\t\t" + "self." + varr[i] + " = " + "args[" + str(i) + "]"


predFile = open('predicateFile1.txt')
readPredicateFile(predFile)