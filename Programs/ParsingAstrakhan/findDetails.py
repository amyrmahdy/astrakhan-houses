def getComposeKey(fullName,scriptlist,template,index):
    scriptlist =  scriptlist[template[index]]
    fullName += 'address'
    index += 1
    dict_address = {}
    for el in scriptlist:
        fullNameEl=fullName
        nextData=el
        i = index
        while i < len(template):
            if i  == len(template)-1:
                nextData=el[template[i]]
                fullNameEl += template[i]
                dict_address.update({fullNameEl:nextData})
            else:              
                nextData=el[template[i]]
                fullNameEl += str(nextData)
            i+=1
    return  dict_address

def noneObjects(fullName,template,index):
    i = index
    fullNameEl = fullName
    while i < len(template):
        fullNameEl += template[i]
        i += 1
    return {fullNameEl:None}

def getDictByTemplate(script,template):
    fullName = ""
    nextData=script
    i=0
    while i < len(template):
        if template[i] == "[":
            nextData=nextData[0]
        elif template[i] == "{":
            return getComposeKey(fullName,nextData,template,i+1)
        else:
            if template[i] in list(nextData.keys()):
                if nextData[template[i]] is not None:
                    nextData=nextData[template[i]]
                    fullName += template[i]
                else:
                    return noneObjects(fullName,template,i)
            else:
                return noneObjects(fullName,template,i)
        i+=1
    return {fullName:nextData}


