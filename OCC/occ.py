from task import Task

def validFirstCondition(txn):
    validFirstCondition = False
    for task in lifeline:
        if task.txn != txn and validationTimestamp(txn) < validationTimestamp(task.txn):
            if startTimestamp(txn) < finishTimestamp(task.txn):
                validFirstCondition =  True
    return validFirstCondition

def validSecondCondition(txn):
    validSecondCondition = False
    for task in lifeline:
        if task.txn != txn and validationTimestamp(txn) > validationTimestamp(task.txn):
            if (finishTimestamp(txn) > startTimestamp(task.txn) and validationTimestamp(task.txn) > finishTimestamp(txn) and not isWriteReadIntersect(txn, task.txn)):
                validSecondCondition = True
    return validSecondCondition

def isWriteReadIntersect(txn1, txn2):
    isWriteReadIntersect = False
    for task1 in lifeline:
        for task2 in lifeline[::-1]:
            if task1.txn == txn1 and task2.txn == txn2:
                if task1.type== "read" and task2.type=="write" and task1.data == task2.data:
                    isWriteReadIntersect = True
    return isWriteReadIntersect

def startTimestamp(txn):
    startTimestamp = 0
    for task in lifeline:
        if task.txn == txn and task.uniqueTimestamp == "startTimestamp":
            startTimestamp = task.timestamp
    return startTimestamp

def finishTimestamp(txn):
    finishTimestamp=0
    for task in lifeline[::-1]:
        if task.txn == txn:
            finishTimestamp = task.timestamp
    return finishTimestamp

def validationTimestamp(txn):
    validationTimestamp = 0
    for task in lifeline:
        if task.txn == txn and task.type == "validate":
            validationTimestamp = task.timestamp
    return validationTimestamp


timestamp = 1
lifeline = []
txnList = []


newTask = input()
while newTask != "execute":
    attr = newTask.split()
    if ("read" in newTask.lower() or "write" in newTask.lower() or "display" in newTask.lower()):
        T = Task(attr[0], attr[1], attr[2], timestamp)
        lifeline.append(T)

    elif ("validate" in newTask.lower()):
        T = Task(attr[0], "-", attr[1], timestamp)
        lifeline.append(T)

    else:
        T = Task("modify", attr[0], attr[1], timestamp)

    if T.txn not in txnList:
        T.setUniqueTimestamp("startTimestamp")
        txnList.append(T.txn)

        
    timestamp += 1
    newTask = input()


for txn in txnList:
    if validFirstCondition(txn) or validSecondCondition(txn):
        print("Transaksi "+str(txn)+" valid")
    if not validFirstCondition(txn) and not validSecondCondition(txn):
        print("Transaksi "+str(txn)+" rollback")


