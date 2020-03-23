##########################################################################
# Tomasulo Simulator
# Author: Nicholas Denu
# Last Editted: 3/22/2020
#
# Description: This program is meant to read in a list of simple MIPS
#               instructions and perform their actions in the method
#               as decribed in Tomasulo's Algorithm. The status of every
#               instruction is to be documented.
##########################################################################


# Global Variable Column Name Definitions

# Instruction Status List
ISSUE = 0
BEGIN = 1
EXECCOMP = 2
WRITE = 3

# Load/Store List
BUSY = 0
ADDR = 1
DEST = 2
LOADCOUNTDOWN = 3
LOADINSTRINDEX = 4

# Reservation Station List
OP = 1
VJ = 2
VK = 3
QJ = 4
QK = 5
RSCOUNTDOWN = 6
RSINSTRINDEX = 7

# Clock Cycles Per Instruction Type
LOADCYCLES = 3
STORECYCLES = 3
MULTCYCLES = 11
ADDCYCLES = 2
SUBCYCLES = 2
DIVCYCLES = 40

# Write List
VALUE = 0
TAG = 1
WINSTRINDEX = 2


def loadInstrFile(instrFile):
    retInstrList = list()
    
    fileObject = open(instrFile, "r")
    for x in fileObject:
        retInstrList.append(x.rstrip())
    
    return retInstrList
    
def initInstrStatusList():
    # instrStatusList is to hold status for all instructions in three columns
    instrStatusList = list()
    instrStatusList.append(list()) # Issue Cycle
    instrStatusList.append(list()) # Begin Cycle
    instrStatusList.append(list()) # Execution Complete Cycle
    instrStatusList.append(list()) # Write Cycle
    return instrStatusList

def initLoadList():
    loadList = list()
    loadList.append(list())
    loadList.append(list())
    loadList.append(list())
    loadList.append(list())
    loadList.append(list())
    loadList[BUSY].append("No")
    loadList[BUSY].append("No")
    loadList[BUSY].append("No")
    loadList[ADDR].append(" ")
    loadList[ADDR].append(" ")
    loadList[ADDR].append(" ")
    loadList[DEST].append(" ")
    loadList[DEST].append(" ")
    loadList[DEST].append(" ")
    loadList[LOADCOUNTDOWN].append(0)
    loadList[LOADCOUNTDOWN].append(0)
    loadList[LOADCOUNTDOWN].append(0)
    loadList[LOADINSTRINDEX].append(0)
    loadList[LOADINSTRINDEX].append(0)
    loadList[LOADINSTRINDEX].append(0)
    
    return loadList

def initStoreList():
    storeList = list()
    storeList.append(list())
    storeList.append(list())
    storeList.append(list())
    storeList.append(list())
    storeList.append(list())
    storeList[BUSY].append("No")
    storeList[BUSY].append("No")
    storeList[BUSY].append("No")
    storeList[ADDR].append(" ")
    storeList[ADDR].append(" ")
    storeList[ADDR].append(" ")
    storeList[DEST].append(" ")
    storeList[DEST].append(" ")
    storeList[DEST].append(" ")
    storeList[LOADCOUNTDOWN].append(0)
    storeList[LOADCOUNTDOWN].append(0)
    storeList[LOADCOUNTDOWN].append(0)
    storeList[LOADINSTRINDEX].append(0)
    storeList[LOADINSTRINDEX].append(0)
    storeList[LOADINSTRINDEX].append(0)
    
    return storeList

def initResStatList():
    resStatList = list()
    resStatList.append(list())
    resStatList.append(list())
    resStatList.append(list())
    resStatList.append(list())
    resStatList.append(list())
    resStatList.append(list())
    resStatList.append(list())
    resStatList.append(list())
    resStatList[BUSY].append("No")
    resStatList[BUSY].append("No")
    resStatList[BUSY].append("No")
    resStatList[BUSY].append("No")
    resStatList[BUSY].append("No")
    resStatList[OP].append(" ")
    resStatList[OP].append(" ")
    resStatList[OP].append(" ")
    resStatList[OP].append(" ")
    resStatList[OP].append(" ")
    resStatList[VJ].append(" ")
    resStatList[VJ].append(" ")
    resStatList[VJ].append(" ")
    resStatList[VJ].append(" ")
    resStatList[VJ].append(" ")
    resStatList[VK].append(" ")
    resStatList[VK].append(" ")
    resStatList[VK].append(" ")
    resStatList[VK].append(" ")
    resStatList[VK].append(" ")
    resStatList[QJ].append(" ")
    resStatList[QJ].append(" ")
    resStatList[QJ].append(" ")
    resStatList[QJ].append(" ")
    resStatList[QJ].append(" ")
    resStatList[QK].append(" ")
    resStatList[QK].append(" ")
    resStatList[QK].append(" ")
    resStatList[QK].append(" ")
    resStatList[QK].append(" ")
    resStatList[RSCOUNTDOWN].append(" ")
    resStatList[RSCOUNTDOWN].append(" ")
    resStatList[RSCOUNTDOWN].append(" ")
    resStatList[RSCOUNTDOWN].append(" ")
    resStatList[RSCOUNTDOWN].append(" ")
    resStatList[RSINSTRINDEX].append(0)
    resStatList[RSINSTRINDEX].append(0)
    resStatList[RSINSTRINDEX].append(0)
    resStatList[RSINSTRINDEX].append(0)
    resStatList[RSINSTRINDEX].append(0)
    
    return resStatList

def initRList():
    rList = list()
    rList.append(0)
    rList.append(0)
    rList.append(0)
    rList.append(0)
    rList.append(0)
    rList.append(0)
    rList.append(0)
    rList.append(0)
    rList.append(0)
    return rList

def initFList():
    fList = list()
    fList.append("0")
    fList.append("0")
    fList.append("0")
    fList.append("0")
    fList.append("0")
    fList.append("0")
    fList.append("0")
    fList.append("0")
    fList.append("0")
    fList.append("0")
    return fList

def initMemList():
    memList = list()
    for i in range(100):
        memList.append(0)
    return memList

def initWriteItem():
    writeList = list()
    writeList.append(0)
    writeList.append("")
    writeList.append(0)
    return writeList

def main():
    instrFile = "instrFile.txt"
    
    instrList = loadInstrFile(instrFile)
    instrStatusList = initInstrStatusList()
    loadList = initLoadList()
    storeList = initStoreList()
    resStatList = initResStatList()
    rList = initRList()
    fList = initFList()
    memList = initMemList()
    
    cdb = initWriteItem()
    
    instrIssueCounter = 0
    clockCycle = 0
    while(instrIssueCounter < len(instrList)):
# Issue
        instr = instrList[instrIssueCounter]
        instrArray = instr.split(" ", 5)
        if instrArray[0] == "LD": # 3 Cycles
            if loadList[BUSY].index("No") >= 0:
                index = loadList[BUSY].index("No")
                loadList[BUSY][index] = "Yes"
                loadList[ADDR][index] = str(instrArray[2]) + (instrArray[3])
                loadList[DEST][index] = instrArray[1]
                loadList[LOADCOUNTDOWN][index] = LOADCYCLES + 1
                loadList[LOADINSTRINDEX][index] = instrIssueCounter
                
                regIndex = int(instrArray[1].split('F', 1)[1])
                fList[regIndex] = "Load" + str(index)
                
                instrStatusList[ISSUE].append(clockCycle)
                instrStatusList[BEGIN].append(0)
                instrStatusList[EXECCOMP].append(0)
                instrStatusList[WRITE].append(0)
                
                instrIssueCounter += 1
            else:
                print("Trouble in LD")
        elif instr.split(" ")[0] == "SD": # 3 Cycles
            if storeList[BUSY].index("No") >= 0:
                index = storeList[BUSY].index("No")
                storeList[BUSY][index] = "Yes"
                storeList[DEST][index] = instrArray[2] + instrArray[3]
                storeList[ADDR][index] = instrArray[1]
                storeList[LOADCOUNTDOWN][index] = STORECYCLES + 1
                
                instrStatusList[ISSUE].append(clockCycle)
                instrStatusList[BEGIN].append(0)
                instrStatusList[EXECCOMP].append(0)
                instrStatusList[WRITE].append(0)
                
                instrIssueCounter += 1
            else:
                print("Trouble in SD")
        elif instr.split(" ")[0] == "ADDD": # 2 Cycles
            if resStatList[BUSY].index("No") >= 0 and resStatList[BUSY].index("No") < 3:
                index = resStatList[BUSY].index("No")
                resStatList[BUSY][index] = "Yes"
                resStatList[OP][index] = "ADDD"
                destinationIndex = int(instrArray[1].split('F', 1)[1])
                sourceIndex1 = int(instrArray[2].split('F', 1)[1])
                sourceIndex2 = int(instrArray[3].split('F', 1)[1])
                if fList[sourceIndex1].isnumeric() == 1:
                    resStatList[VJ][index] = fList[sourceIndex1]
                elif fList[sourceIndex1][0] == "M":
                    resStatList[VJ][index] = fList[sourceIndex1]
                else:
                    resStatList[QJ][index] = fList[sourceIndex1]
                if fList[sourceIndex2].isnumeric() == 1:
                    resStatList[VK][index] = fList[sourceIndex2]
                elif fList[sourceIndex2][0] == "M":
                    resStatList[VK][index] = fList[sourceIndex2]
                else:
                    resStatList[QK][index] = fList[sourceIndex2]
                instrStatusList[ISSUE].append(clockCycle)
                instrStatusList[BEGIN].append(0)
                instrStatusList[EXECCOMP].append(0)
                instrStatusList[WRITE].append(0)
                resStatList[RSCOUNTDOWN][index] = ADDCYCLES + 1
                fList[int(instrArray[1].split('F', 1)[1])] = "Add" + str(index + 1)
                
                instrIssueCounter += 1
            else:
                print("Trouble in ADDD")
        elif instr.split(" ")[0] == "SUBD": # 2 Cycles
            if resStatList[BUSY].index("No") >= 0 and resStatList[BUSY].index("No") < 3:
                index = resStatList[BUSY].index("No")
                resStatList[BUSY][index] = "Yes"
                resStatList[OP][index] = "SUBD"
                destinationIndex = int(instrArray[1].split('F', 1)[1])
                sourceIndex1 = int(instrArray[2].split('F', 1)[1])
                sourceIndex2 = int(instrArray[3].split('F', 1)[1])
                if fList[sourceIndex1].isnumeric() == 1:
                    resStatList[VJ][index] = fList[sourceIndex1]
                elif fList[sourceIndex1][0] == "M":
                    resStatList[VJ][index] = fList[sourceIndex1]
                else:
                    resStatList[QJ][index] = fList[sourceIndex1]
                if fList[sourceIndex2].isnumeric() == 1:
                    resStatList[VK][index] = fList[sourceIndex2]
                elif fList[sourceIndex2][0] == "M":
                    resStatList[VK][index] = fList[sourceIndex2]
                else:
                    resStatList[QK][index] = fList[sourceIndex2]
                instrStatusList[ISSUE].append(clockCycle)
                instrStatusList[BEGIN].append(0)
                instrStatusList[EXECCOMP].append(0)
                instrStatusList[WRITE].append(0)
                
                resStatList[RSCOUNTDOWN][index] = SUBCYCLES + 1
                fList[int(instrArray[1].split('F', 1)[1])] = "Add" + str(index + 1)
                
                instrIssueCounter += 1
            else:
                print("Trouble in SUBD")
        elif instr.split(" ")[0] == "MULTD": # 10 Cycles
            if resStatList[BUSY][3] == "No":
                index = 3
                resStatList[BUSY][index] = "Yes"
                resStatList[OP][index] = "MULTD"
                destinationIndex = int(instrArray[1].split('F', 1)[1])
                sourceIndex1 = int(instrArray[2].split('F', 1)[1])
                sourceIndex2 = int(instrArray[3].split('F', 1)[1])
                if fList[sourceIndex1].isnumeric() == 1:
                    resStatList[VJ][index] = fList[sourceIndex1]
                elif fList[sourceIndex1][0] == "M":
                    resStatList[VJ][index] = fList[sourceIndex1]
                else:
                    resStatList[QJ][index] = fList[sourceIndex1]
                if fList[sourceIndex2].isnumeric() == 1:
                    resStatList[VK][index] = fList[sourceIndex2]
                elif fList[sourceIndex2][0] == "M":
                    resStatList[VK][index] = fList[sourceIndex2]
                else:
                    resStatList[QK][index] = fList[sourceIndex2]
                instrStatusList[ISSUE].append(clockCycle)
                instrStatusList[BEGIN].append(0)
                instrStatusList[EXECCOMP].append(0)
                instrStatusList[WRITE].append(0)
                
                resStatList[RSCOUNTDOWN][index] = MULTCYCLES + 1
                fList[int(instrArray[1].split('F', 1)[1])] = "Add" + str(index + 1)
                
                instrIssueCounter += 1
            elif resStatList[BUSY][4] == "No":
                index = 4 
                resStatList[BUSY][index] = "Yes"
                resStatList[OP][index] = "MULTD"
                destinationIndex = int(instrArray[1].split('F', 1)[1])
                sourceIndex1 = int(instrArray[2].split('F', 1)[1])
                sourceIndex2 = int(instrArray[3].split('F', 1)[1])
                if fList[sourceIndex1].isnumeric() == 1:
                    resStatList[VJ][index] = fList[sourceIndex1]
                elif fList[sourceIndex1][0] == "M":
                    resStatList[VJ][index] = fList[sourceIndex1]
                else:
                    resStatList[QJ][index] = fList[sourceIndex1]
                if fList[sourceIndex2].isnumeric() == 1:
                    resStatList[VK][index] = fList[sourceIndex2]
                elif fList[sourceIndex2][0] == "M":
                    resStatList[VK][index] = fList[sourceIndex2]
                else:
                    resStatList[QK][index] = fList[sourceIndex2]
                instrStatusList[ISSUE].append(clockCycle)
                instrStatusList[BEGIN].append(0)
                instrStatusList[EXECCOMP].append(0)
                instrStatusList[WRITE].append(0)
                
                resStatList[RSCOUNTDOWN][index] = MULTCYCLES + 1
                fList[int(instrArray[1].split('F', 1)[1])] = "Add" + str(index + 1)
                
                instrIssueCounter += 1
            else:
                print("Trouble in MULTD")
        elif instr.split(" ")[0] == "DIVD": # 40 Cycles
            if resStatList[BUSY][3] == "No":
                index = 3
                resStatList[BUSY][index] = "Yes"
                resStatList[OP][index] = "DIVD"
                destinationIndex = int(instrArray[1].split('F', 1)[1])
                sourceIndex1 = int(instrArray[2].split('F', 1)[1])
                sourceIndex2 = int(instrArray[3].split('F', 1)[1])
                if fList[sourceIndex1].isnumeric() == 1:
                    resStatList[VJ][index] = fList[sourceIndex1]
                elif fList[sourceIndex1][0] == "M":
                    resStatList[VJ][index] = fList[sourceIndex1]
                else:
                    resStatList[QJ][index] = fList[sourceIndex1]
                if fList[sourceIndex2].isnumeric() == 1:
                    resStatList[VK][index] = fList[sourceIndex2]
                elif fList[sourceIndex2][0] == "M":
                    resStatList[VK][index] = fList[sourceIndex2]
                else:
                    resStatList[QK][index] = fList[sourceIndex2]
                instrStatusList[ISSUE].append(clockCycle)
                instrStatusList[BEGIN].append(0)
                instrStatusList[EXECCOMP].append(0)
                instrStatusList[WRITE].append(0)
                
                resStatList[RSCOUNTDOWN][index] = DIVCYCLES + 1
                fList[int(instrArray[1].split('F', 1)[1])] = "Add" + str(index + 1)
                
                instrIssueCounter += 1
            elif resStatList[BUSY][4] == "No":
                index = 4
                resStatList[BUSY][index] = "Yes"
                resStatList[OP][index] = "DIVD"
                destinationIndex = int(instrArray[1].split('F', 1)[1])
                sourceIndex1 = int(instrArray[2].split('F', 1)[1])
                sourceIndex2 = int(instrArray[3].split('F', 1)[1])
                if fList[sourceIndex1].isnumeric() == 1:
                    resStatList[VJ][index] = fList[sourceIndex1]
                elif fList[sourceIndex1][0] == "M":
                    resStatList[VJ][index] = fList[sourceIndex1]
                else:
                    resStatList[QJ][index] = fList[sourceIndex1]
                if fList[sourceIndex2].isnumeric() == 1:
                    resStatList[VK][index] = fList[sourceIndex2]
                elif fList[sourceIndex2][0] == "M":
                    resStatList[VK][index] = fList[sourceIndex2]
                else:
                    resStatList[QK][index] = fList[sourceIndex2]
                instrStatusList[ISSUE].append(clockCycle)
                instrStatusList[BEGIN].append(0)
                instrStatusList[EXECCOMP].append(0)
                instrStatusList[WRITE].append(0)
                
                resStatList[RSCOUNTDOWN][index] = DIVCYCLES + 1
                fList[int(instrArray[1].split('F', 1)[1])] = "Add" + str(index + 1)
                
                instrIssueCounter += 1
            else:
                print("Trouble in DIVD")
        else:
            print("We've got problems in the instruction file")
        
    
# Execute
        priorityIndex = -1
        lowestCountdown = 2
        
        # Execute Loads
        for i in range(len(loadList[BUSY])):
            if(loadList[BUSY][i] == "Yes"):
                if(loadList[ADDR][i].isnumeric() == 1):
                    if(loadList[LOADCOUNTDOWN][i] == 4):
                        instrStatusList[BEGIN][loadList[LOADINSTRINDEX][i]] = clockCycle
                    elif(loadList[LOADCOUNTDOWN][i] <= 1):
                        if(loadList[LOADCOUNTDOWN][i] < lowestCountdown):
                            lowestCountdown = loadList[LOADCOUNTDOWN][i]
                            priorityIndex = i
                        
                    loadList[LOADCOUNTDOWN][i] -= 1
                        
                elif (loadList[ADDR][i].split("R", 3)[1].isnumeric() == 1):
                    loadList[ADDR][i] = str(rList[int(loadList[ADDR][i].split("R", 3)[1])] + int(loadList[ADDR][i].split("+", 3)[0]))
        if(priorityIndex != -1):
            if(cdb[TAG] == ""):
                cdb[VALUE] = memList[int(loadList[ADDR][priorityIndex])]
                cdb[TAG] = "LOAD" + str(priorityIndex + 1)
                cdb[WINSTRINDEX] = loadList[LOADINSTRINDEX][priorityIndex]
                loadList[BUSY][priorityIndex] = "No"
                loadList[ADDR][priorityIndex] = ""
                loadList[LOADINSTRINDEX][priorityIndex] = 0
    
        print(loadList)
        # Execute Stores
        for i in range(len(storeList[BUSY])):
            if(storeList[BUSY][i] == "Yes"):
                if(storeList[ADDR][i].isnumeric() == 1):
                    if(storeList[LOADCOUNTDOWN][i] == 4):
                        instrStatusList[BEGIN][storeList[LOADINSTRINDEX]] = clockCycle
                    elif(storeList[LOADCOUNTDOWN][i] <= 1):
                        if(storeList[LOADCOUNTDOWN][i] < lowestCountdown):
                            lowestCountdown = storeList[storeCOLOADCOUNTDOWNUNTDOWN][i]
                            priorityIndex = i
                        
                    storeList[LOADCOUNTDOWN][i] -= 1
                        
                elif (storeList[DEST][i].split("R", 3)[1].isnumeric() == 1):
                    storeList[DEST][i] = str(rList[int(storeList[DEST][i].split("R", 3)[1])] + int(storeList[DEST][i].split("+", 3)[0]))
        if(priorityIndex != -1):
            if(cdb[TAG] == ""):
                cdb[VALUE] = memList[int(storeList[ADDR][priorityIndex])]
                cdb[TAG] = "STORE" + str(priorityIndex + 1)
                cdb[WINSTRINDEX] = storeList[LOADINSTRINDEX][priorityIndex]
                storeList[BUSY][priorityIndex] = "No"
                storeList[ADDR][priorityIndex] = ""
                storeList[LOADINSTRINDEX][priorityIndex] = 0

        # Execute MATH OPS
        isReadyToBegin
        for i in range(3):
            if(resStatList[BUSY][i] == "Yes"):
                
# Write Result
    
    
    
    
if __name__ == '__main__':
    main()