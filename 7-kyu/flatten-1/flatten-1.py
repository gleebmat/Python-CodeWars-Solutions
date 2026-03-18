def flatten(lst):
    newLst=[]
    for each in lst:
        if (isinstance(each,list)):
            for every in each:
                newLst.append(every)
        else:
            newLst.append(each)
    return newLst